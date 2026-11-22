async function main() {
  const listRes = await fetch('http://localhost:9222/json/list');
  const targets = await listRes.json();
  const pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');
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
  await new Promise(r => ws.onopen = r);

  // Enter combat gameplay
  await sendCommand('Runtime.evaluate', { expression: "window.startGameFromMenu()" });
  await new Promise(r => setTimeout(r, 2000));

  // Measure draw calls and triangles in Three.js renderer during gameplay
  const res = await sendCommand('Runtime.evaluate', {
    expression: `(() => {
      const app = window._app;
      if (!app || !app.renderer) return { error: 'no app' };
      const info = app.renderer.info;
      return {
        calls: info.render.calls,
        triangles: info.render.triangles,
        lines: info.render.lines,
        points: info.render.points,
        geometries: info.memory.geometries,
        textures: info.memory.textures,
        pixelRatio: app.renderer.getPixelRatio(),
        shadowMapEnabled: app.renderer.shadowMap.enabled,
        fpsBadgeVal: document.getElementById('live-fps-val')?.textContent,
        postProcessing: !!app.postProcessing,
        bloomPass: !!app.bloomPass
      };
    })()`,
    returnByValue: true
  });
  console.log('Gameplay Renderer Info:', JSON.stringify(res.result.value, null, 2));
  process.exit(0);
}
main();
