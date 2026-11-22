import fs from 'fs';
import { spawn } from 'child_process';

const ARTIFACT_DIR = 'C:\\Users\\Vrund Patel\\.gemini\\antigravity\\brain\\872b1927-4373-40e0-8876-e950842c0100';
const CDP_PORT = 9339;
const TEMP_PROFILE = 'C:\\Users\\Vrund Patel\\AppData\\Local\\Temp\\isolated_final_verify_' + Date.now();

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function verify() {
  console.log('Spawning isolated Chrome on port ' + CDP_PORT + '...');
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
  await sleep(1500);

  // Check live HUD FPS value and settings
  const hudCheck = await send('Runtime.evaluate', {
    expression: `(() => {
      const fpsEl = document.getElementById("live-fps-val");
      const fpsBadge = document.getElementById("live-fps-badge");
      const settings = window._gameSettings;
      const isPostProcessingBypassed = !(window._app && window._app.bloomPass && window._app.bloomPass.strength > 0.05);
      return {
        hudFpsText: fpsEl ? fpsEl.textContent : "none",
        badgeDisplay: fpsBadge ? window.getComputedStyle(fpsBadge).display : "none",
        bloomStrength: settings ? settings.bloomStrength : null,
        renderScale: settings ? settings.renderScale : null,
        isPostProcessingBypassed
      };
    })()`,
    returnByValue: true
  });
  console.log('HUD and Engine State:', JSON.stringify(hudCheck.result.value, null, 2));

  // Take final verified screenshot
  const finalSnap = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(ARTIFACT_DIR + '/final_hd_60fps_battlefield.png', Buffer.from(finalSnap.data, 'base64'));

  ws.close();
  chromeProc.kill();
  try { fs.rmSync(TEMP_PROFILE, { recursive: true, force: true }); } catch(e) {}
  console.log('Verification completed successfully! Screenshot saved as final_hd_60fps_battlefield.png');
}

verify().catch(e => { console.error('Error:', e); process.exit(1); });
