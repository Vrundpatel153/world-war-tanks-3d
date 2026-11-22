import fs from 'fs';
import { spawn } from 'child_process';

const CDP_PORT = 9340;
const TEMP_PROFILE = 'C:\\Users\\Vrund Patel\\AppData\\Local\\Temp\\isolated_profile_test_' + Date.now();

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function runProfile() {
  console.log('[1/4] Spawning Chrome for CPU profiling on port ' + CDP_PORT + '...');
  const chromeProc = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--remote-debugging-port=' + CDP_PORT,
    '--headless=new',
    '--no-sandbox',
    '--disable-gpu-sandbox',
    '--user-data-dir=' + TEMP_PROFILE,
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-sync',
    '--disable-background-networking',
    '--enable-gpu-rasterization',
    '--enable-webgl',
    '--ignore-gpu-blocklist',
    'http://localhost:8080/'
  ], { stdio: 'ignore' });

  let pageTarget = null;
  for (let i = 0; i < 25; i++) {
    await sleep(400);
    try {
      const res = await fetch('http://localhost:' + CDP_PORT + '/json/list');
      const targets = await res.json();
      pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');
      if (pageTarget) break;
    } catch (e) {}
  }

  if (!pageTarget) {
    console.error('Failed to connect to isolated Chrome');
    chromeProc.kill();
    process.exit(1);
  }

  const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);
  let id = 1;
  const send = (method, params = {}) => new Promise((resolve, reject) => {
    const curId = id++;
    const handler = (e) => {
      const d = JSON.parse(e.data);
      if (d.id === curId) {
        ws.removeEventListener('message', handler);
        if (d.error) reject(d.error);
        else resolve(d.result);
      }
    };
    ws.addEventListener('message', handler);
    ws.send(JSON.stringify({ id: curId, method, params }));
  });
  await new Promise(r => ws.onopen = r);

  await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
  await send('Page.reload', { ignoreCache: true });

  for (let i = 0; i < 30; i++) {
    await sleep(250);
    const r = await send('Runtime.evaluate', {
      expression: '!!(window._app && window._app.world && window._app.world.renderer)'
    });
    if (r.result?.value) break;
  }
  await sleep(1500);

  // Deploy to battle
  await send('Runtime.evaluate', { expression: 'window.startGameFromMenu();' });
  await sleep(1000);

  console.log('[2/4] Starting V8 CPU Profiler for 3 seconds of active gameplay...');
  await send('Profiler.enable');
  await send('Profiler.start');

  // Simulate WASD driving & mouse movements during the 3 seconds
  for (let t = 0; t < 30; t++) {
    await send('Runtime.evaluate', {
      expression: `
        if (window._app && window._app.world) {
          const w = window._app.world;
          if (w.controller) {
            w.controller.keyPressed = w.controller.keyPressed || new Set();
            w.controller.keyPressed.add('KeyW');
          }
          if (w.camera) {
            w.camera._targetOrbitYaw = (w.camera._targetOrbitYaw || 0) + 0.05;
          }
        }
      `
    });
    await sleep(100);
  }

  console.log('[3/4] Stopping CPU Profiler and analyzing top hot spots...');
  const profileRes = await send('Profiler.stop');
  const profile = profileRes.profile;

  // Aggregate time by function name
  const functionTimes = {};
  const nodes = profile.nodes;
  const timeDeltas = profile.timeDeltas || [];
  const samples = profile.samples || [];

  for (let i = 0; i < samples.length; i++) {
    const nodeId = samples[i];
    const delta = timeDeltas[i] || 0;
    const node = nodes.find(n => n.id === nodeId);
    const name = (node ? node.callFrame.functionName : 'unknown') || '(anonymous)';
    const url = node ? (node.callFrame.url.split('/').pop() || '') : '';
    const key = name + ' [' + url + ':' + (node ? node.callFrame.lineNumber : '') + ']';
    functionTimes[key] = (functionTimes[key] || 0) + delta;
  }

  const sorted = Object.entries(functionTimes).sort((a, b) => b[1] - a[1]);
  console.log('\n=== TOP 20 HOTTEST CPU FUNCTIONS (microseconds) ===');
  for (let i = 0; i < Math.min(20, sorted.length); i++) {
    console.log(`${(sorted[i][1] / 1000).toFixed(1)} ms : ${sorted[i][0]}`);
  }

  // Also check console messages/errors
  const logs = await send('Runtime.evaluate', {
    expression: 'window.__errors || []',
    returnByValue: true
  });
  console.log('\nCaptured JS Errors:', logs.result?.value);

  ws.close();
  chromeProc.kill();
  try { fs.rmSync(TEMP_PROFILE, { recursive: true, force: true }); } catch(e) {}
}

runProfile().catch(e => { console.error('Error:', e); process.exit(1); });
