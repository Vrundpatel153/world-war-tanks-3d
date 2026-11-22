import fs from 'fs';
import { spawn } from 'child_process';

async function testModals() {
  const chromeProc = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--remote-debugging-port=9222',
    '--headless=new',
    '--no-sandbox',
    '--disable-gpu-sandbox',
    '--user-data-dir=C:\\Users\\Vrund Patel\\AppData\\Local\\Temp\\chrome-dbg-modal',
    'http://localhost:8080/'
  ], { stdio: 'ignore' });

  let pageTarget = null;
  for (let i = 0; i < 20; i++) {
    await new Promise(r => setTimeout(r, 400));
    try {
      const listRes = await fetch('http://localhost:9222/json/list');
      const targets = await listRes.json();
      pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');
      if (pageTarget) break;
    } catch (e) {}
  }
  if (!pageTarget) { chromeProc.kill(); process.exit(1); }

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
  await new Promise(r => setTimeout(r, 2500));

  // 1. Open Graphics & System Settings
  await send('Runtime.evaluate', { expression: "window.openMenuModal('modal-options')" });
  await new Promise(r => setTimeout(r, 800));
  const snapSettings = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\Vrund Patel\\.gemini\\antigravity\\brain\\872b1927-4373-40e0-8876-e950842c0100\\verified_settings_final.png', Buffer.from(snapSettings.data, 'base64'));
  console.log('Saved verified_settings_final.png');

  // 2. Open Field Manual & Controls
  await send('Runtime.evaluate', { expression: "window.openMenuModal('modal-controls')" });
  await new Promise(r => setTimeout(r, 800));
  const snapControls = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\Vrund Patel\\.gemini\\antigravity\\brain\\872b1927-4373-40e0-8876-e950842c0100\\verified_controls_final.png', Buffer.from(snapControls.data, 'base64'));
  console.log('Saved verified_controls_final.png');

  console.log('Modals tested and saved successfully!');
  chromeProc.kill();
  process.exit(0);
}
testModals().catch(e => { console.error(e); process.exit(1); });
