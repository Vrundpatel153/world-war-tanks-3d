import fs from 'fs';
import { spawn } from 'child_process';

const ARTIFACT_DIR = 'C:\\Users\\Vrund Patel\\.gemini\\antigravity\\brain\\872b1927-4373-40e0-8876-e950842c0100';
const CDP_PORT = 9342;
const TEMP_PROFILE = 'C:\\Users\\Vrund Patel\\AppData\\Local\\Temp\\isolated_verify_60fps_' + Date.now();

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function verify() {
  console.log('[1/4] Spawning isolated Chrome on port ' + CDP_PORT + '...');
  const chromeProc = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--remote-debugging-port=' + CDP_PORT,
    '--headless=new',
    '--no-sandbox',
    '--disable-gpu-sandbox',
    '--use-gl=angle',
    '--use-angle=d3d11',
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
  console.log('[2/4] Deploying to battlefield...');
  await send('Runtime.evaluate', { expression: 'window.startGameFromMenu();' });
  await sleep(1500);

  // Measure 120 frames while actively driving and turning
  console.log('[3/4] Measuring frame-times across 120 active gameplay frames...');
  const frameMetrics = await send('Runtime.evaluate', {
    expression: `new Promise(resolve => {
      const deltas = [];
      let lastTime = performance.now();
      let frames = 0;
      
      // Simulate continuous driving
      if (window._app && window._app.world && window._app.world.controller) {
        window._app.world.controller.keyPressed = new Set(['KeyW']);
      }

      function step() {
        frames++;
        const now = performance.now();
        deltas.push(now - lastTime);
        lastTime = now;

        if (frames < 120) {
          requestAnimationFrame(step);
        } else {
          // Process stats
          deltas.shift(); // Remove first frame warmup
          const totalMs = deltas.reduce((a, b) => a + b, 0);
          const avgFps = Math.round((deltas.length / totalMs) * 1000);
          const maxDelta = Math.max(...deltas);
          const minDelta = Math.min(...deltas);
          deltas.sort((a, b) => a - b);
          const p99Delta = deltas[Math.floor(deltas.length * 0.99)];
          const onePercentLow = Math.round(1000 / p99Delta);
          const hudFps = document.getElementById('live-fps-val')?.textContent || 'none';
          
          resolve({
            avgFps,
            onePercentLow,
            maxFrameTimeMs: maxDelta.toFixed(1),
            minFrameTimeMs: minDelta.toFixed(1),
            p99FrameTimeMs: p99Delta.toFixed(1),
            hudFps
          });
        }
      }
      requestAnimationFrame(step);
    })`,
    awaitPromise: true,
    returnByValue: true
  });

  console.log('\n=== REAL-TIME 120-FRAME PERFORMANCE METRICS ===');
  console.log(JSON.stringify(frameMetrics.result.value, null, 2));

  // Take screenshot
  console.log('[4/4] Capturing final verified battle screenshot...');
  const snap = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(ARTIFACT_DIR + '/verified_smooth_60fps_gameplay.png', Buffer.from(snap.data, 'base64'));

  ws.close();
  chromeProc.kill();
  try { fs.rmSync(TEMP_PROFILE, { recursive: true, force: true }); } catch(e) {}
  console.log('Verification finished! Artifact saved.');
}

verify().catch(e => { console.error('Error:', e); process.exit(1); });
