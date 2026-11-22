import fs from 'fs';

async function main() {
  // 1. Fetch active targets from Chrome DevTools
  const listRes = await fetch('http://localhost:9222/json/list');
  const targets = await listRes.json();
  const pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');

  if (!pageTarget) {
    console.error('No page target found on port 9222:', targets);
    process.exit(1);
  }

  console.log('Connecting to target:', pageTarget.title, pageTarget.webSocketDebuggerUrl);
  const ws = new WebSocket(pageTarget.webSocketDebuggerUrl);

  let idCounter = 1;
  const pending = new Map();

  function sendCommand(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = idCounter++;
      pending.set(id, { resolve, reject });
      ws.send(JSON.stringify({ id, method, params }));
    });
  }

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.id && pending.has(data.id)) {
      const { resolve, reject } = pending.get(data.id);
      pending.delete(data.id);
      if (data.error) reject(data.error);
      else resolve(data.result);
    }
  };

  await new Promise((resolve) => ws.onopen = resolve);
  console.log('Connected to Chrome DevTools WebSocket!');

  // Navigate to localhost:8080/
  await sendCommand('Page.navigate', { url: 'http://localhost:8080/' });
  console.log('Navigated to http://localhost:8080/');

  // Wait 2.5 seconds for loader to transition to Home Screen
  await new Promise(r => setTimeout(r, 2600));

  // Take screenshot of Home Screen
  const snap1 = await sendCommand('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\Vrund Patel\\Desktop\\clone-game\\home_screen_cdp.png', Buffer.from(snap1.data, 'base64'));
  console.log('Saved home_screen_cdp.png');

  // Click PLAY button
  console.log('Clicking PLAY button...');
  await sendCommand('Runtime.evaluate', {
    expression: "document.querySelector('.btn-home-play') ? document.querySelector('.btn-home-play').click() : window.startGameFromMenu()"
  });

  // Wait 2 seconds in-game for 3D world to render
  await new Promise(r => setTimeout(r, 2000));

  // Take screenshot of in-game battlefield
  const snap2 = await sendCommand('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\Vrund Patel\\Desktop\\clone-game\\gameplay_cdp.png', Buffer.from(snap2.data, 'base64'));
  console.log('Saved gameplay_cdp.png');

  // Now turn camera to look at the wind turbine and check rendering stability
  console.log('Rotating camera and checking scene objects...');
  const evalResult = await sendCommand('Runtime.evaluate', {
    expression: `(() => {
      const app = window._app;
      if (!app || !app.world) return { error: 'No world' };
      const instanced = Object.keys(app.world.areaManager.instancedObjects || {});
      const cullingEnabled = app.world.areaManager.cullingManager.enabled;
      const fanVisible = app.world.areaManager.fan ? app.world.areaManager.fan.instancedWindFans.length : 0;
      return {
        cullingEnabled,
        instancedCount: instanced.length,
        instancedKeys: instanced,
        windFanBatches: fanVisible
      };
    })()`,
    returnByValue: true
  });
  console.log('Engine status:', JSON.stringify(evalResult.result.value, null, 2));

  // Take third screenshot after rotating / moving slightly
  await sendCommand('Runtime.evaluate', {
    expression: `(() => {
      const cam = window._app.world.camera;
      if (cam) {
        cam._targetOrbitPitch = 0.22;
        cam._targetOrbitHeading = (cam._targetOrbitHeading || 0) + 0.8;
      }
    })()`
  });
  await new Promise(r => setTimeout(r, 1200));

  const snap3 = await sendCommand('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\Vrund Patel\\Desktop\\clone-game\\gameplay_windturbine_cdp.png', Buffer.from(snap3.data, 'base64'));
  console.log('Saved gameplay_windturbine_cdp.png');

  ws.close();
  console.log('Testing completed successfully!');
}

main().catch(err => {
  console.error('CDP Error:', err);
  process.exit(1);
});
