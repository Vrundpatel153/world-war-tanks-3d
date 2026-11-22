import fs from 'fs';

async function main() {
  const listRes = await fetch('http://localhost:9222/json/list');
  const targets = await listRes.json();
  const pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');

  if (!pageTarget) {
    console.error('No page target found');
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

  await sendCommand('Runtime.evaluate', { expression: 'window.startGameFromMenu()' });
  await new Promise(r => setTimeout(r, 600));

  // Rotate camera to look across the grass towards the turbines and trees
  console.log('Rotating camera towards open grassy field and turbines...');
  await sendCommand('Runtime.evaluate', {
    expression: `(() => {
      const app = window._app;
      const cam = app.world.camera;
      if (cam) {
        cam._targetOrbitPitch = 0.02;
        cam._targetOrbitHeading = 0.0; // Look North towards the open world
        cam._targetOrbitDistance = 14.0;
      }
    })()`
  });

  await new Promise(r => setTimeout(r, 1500));

  const snap = await sendCommand('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\Vrund Patel\\Desktop\\clone-game\\turbine_open_field.png', Buffer.from(snap.data, 'base64'));
  console.log('Saved turbine_open_field.png successfully!');

  ws.close();
}

main().catch(err => {
  console.error('Error:', err);
  process.exit(1);
});
