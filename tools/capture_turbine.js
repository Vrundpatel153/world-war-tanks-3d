import fs from 'fs';

async function main() {
  const listRes = await fetch('http://localhost:9222/json/list');
  const targets = await listRes.json();
  const pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');

  if (!pageTarget) {
    console.error('No page target found on port 9222');
    process.exit(1);
  }

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

  // Start game from menu first
  await sendCommand('Runtime.evaluate', { expression: 'window.startGameFromMenu()' });
  await new Promise(r => setTimeout(r, 1000));

  // 1. Move the tank / camera to the wind turbine view
  console.log('Positioning camera at wind turbine and grassy plain...');
  const turbineInfo = await sendCommand('Runtime.evaluate', {
    expression: `(() => {
      const app = window._app;
      if (!app || !app.world) return null;
      const turbineObj = app.world.areaManager.instancedObjects['Turbine'];
      let pos = null;
      if (turbineObj && turbineObj.transforms && turbineObj.transforms[0]) {
        pos = turbineObj.transforms[0].position;
      } else if (turbineObj && turbineObj.batches && turbineObj.batches[0]) {
        pos = turbineObj.batches[0].transforms[0].position;
      }
      const robotBody = app.world.physicsWorld.robotRigidBody;
      const cam = app.world.camera;
      if (pos && robotBody) {
        // Place tank near turbine
        robotBody.setTranslation({ x: pos.x - 18, y: pos.y + 1, z: pos.z - 15 }, true);
        if (cam) {
          cam._targetOrbitPitch = 0.28;
          cam._targetOrbitHeading = -1.2;
          cam._targetOrbitDistance = 9.0;
        }
      }
      return { turbinePos: pos, fanActive: app.world.areaManager.fan != null };
    })()`,
    returnByValue: true
  });
  console.log('Turbine info:', turbineInfo.result.value);

  // Wait 1 second for physics and rendering to settle
  await new Promise(r => setTimeout(r, 1200));

  // 2. Capture screenshot of the wind turbine area
  const snap = await sendCommand('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\Vrund Patel\\Desktop\\clone-game\\turbine_verified.png', Buffer.from(snap.data, 'base64'));
  console.log('Saved turbine_verified.png successfully!');

  ws.close();
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
