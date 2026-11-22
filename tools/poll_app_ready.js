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

  // Poll until app is ready
  console.log('Polling window._app state...');
  for (let i = 0; i < 20; i++) {
    const r = await send('Runtime.evaluate', {
      expression: `(() => {
        const app = window._app;
        return {
          exists: !!app,
          isStartupReady: app?.startup?.isReady,
          hasWorld: !!app?.world,
          hasRobot: !!app?.world?.robot,
          hasCamera: !!app?.camera,
          renderCalls: app?.renderer?.info?.render?.calls,
          triangles: app?.renderer?.info?.render?.triangles
        };
      })()`,
      returnByValue: true
    });
    console.log(`Poll ${i} (${i*500}ms):`, r.result.value);
    if (r.result.value?.hasRobot && r.result.value?.renderCalls > 0) {
      console.log('App is fully ready!');
      break;
    }
    await new Promise(res => setTimeout(res, 500));
  }
  process.exit(0);
}
main().catch(err => { console.error(err); process.exit(1); });
