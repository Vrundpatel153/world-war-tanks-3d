import fs from 'fs';

async function main() {
  const listRes = await fetch('http://localhost:9222/json/list');
  const targets = await listRes.json();
  const pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');
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

  // Set 1440x900 viewport
  await send('Emulation.setDeviceMetricsOverride', {
    width: 1440,
    height: 900,
    deviceScaleFactor: 1,
    mobile: false
  });

  // Start game from menu
  console.log('Calling window.startGameFromMenu()...');
  await send('Runtime.evaluate', { expression: "window.startGameFromMenu()" });
  await new Promise(r => setTimeout(r, 2000));

  const stats = await send('Runtime.evaluate', {
    expression: `(() => {
      const app = window._app;
      return {
        isMenuOpen: window.isGameMenuOpen,
        calls: app?.renderer?.info?.render?.calls,
        triangles: app?.renderer?.info?.render?.triangles,
        timeScale: app?.time?.timeScale,
        physicsEnabled: app?.world?.physicsWorld?.enabled,
        fpsText: document.getElementById('live-fps-val')?.textContent
      };
    })()`,
    returnByValue: true
  });
  console.log('Gameplay Stats:', JSON.stringify(stats.result.value, null, 2));

  const snap = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\Vrund Patel\\.gemini\\antigravity\\brain\\872b1927-4373-40e0-8876-e950842c0100\\test_gameplay_live.png', Buffer.from(snap.data, 'base64'));
  console.log('Saved test_gameplay_live.png');
  process.exit(0);
}
main().catch(err => { console.error(err); process.exit(1); });
