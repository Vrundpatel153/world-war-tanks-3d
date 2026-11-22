async function test() {
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

  await send('Page.reload', { ignoreCache: true });
  console.log('Page reloaded, waiting 4s...');
  await new Promise(r => setTimeout(r, 4000));

  const diag = await send('Runtime.evaluate', {
    expression: `(() => {
      const canvas = document.querySelector('#webgl');
      const gl = canvas?.getContext('webgl2') || canvas?.getContext('webgl');
      const app = window._app;
      return {
        canvasStyleOpacity: canvas?.style?.opacity,
        canvasComputedOpacity: canvas ? window.getComputedStyle(canvas).opacity : null,
        canvasComputedVisibility: canvas ? window.getComputedStyle(canvas).visibility : null,
        canvasComputedZIndex: canvas ? window.getComputedStyle(canvas).zIndex : null,
        isAppReady: !!app,
        isWorldReady: !!(app && app.world),
        isScenePassReady: !!(app && app.scenePass),
        renderCalls: app?.renderer?.info?.render?.calls,
        triangles: app?.renderer?.info?.render?.triangles,
        isRenderPaused: app?.isRenderPaused,
        timeScale: app?.time?.timeScale,
        sceneChildren: app?.scene?.children?.length,
        worldChildren: app?.world?.scene?.children?.length
      };
    })()`,
    returnByValue: true
  });
  console.log('Canvas & Three.js Diag:', JSON.stringify(diag.result.value, null, 2));

  // Capture screenshot right now
  const fs = await import('fs');
  const snap = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\Vrund Patel\\.gemini\\antigravity\\brain\\872b1927-4373-40e0-8876-e950842c0100\\current_live_check.png', Buffer.from(snap.data, 'base64'));
  console.log('Saved current_live_check.png');
  process.exit(0);
}
test().catch(e => { console.error(e); process.exit(1); });
