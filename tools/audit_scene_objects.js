import cp from 'child_process';

const CDP_PORT = 9338;
const TEMP_PROFILE = 'C:\\Users\\Vrund Patel\\AppData\\Local\\Temp\\perf_diag_' + Date.now();
const chromeProc = cp.spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
  '--remote-debugging-port=' + CDP_PORT,
  '--headless=new',
  '--no-sandbox',
  '--disable-gpu-sandbox',
  '--user-data-dir=' + TEMP_PROFILE,
  'http://localhost:8080/'
], { stdio: 'ignore' });

async function run() {
  for (let i = 0; i < 20; i++) {
    await new Promise(r => setTimeout(r, 400));
    try {
      const res = await fetch('http://localhost:' + CDP_PORT + '/json/list');
      const targets = await res.json();
      const t = targets.find(x => x.type === 'page' && x.url.includes('8080'));
      if (t) {
        const ws = new WebSocket(t.webSocketDebuggerUrl);
        let id = 1;
        const send = (m, p = {}) => new Promise((resolve, reject) => {
          const curId = id++;
          const h = (e) => {
            const d = JSON.parse(e.data);
            if (d.id === curId) {
              ws.removeEventListener('message', h);
              if (d.error) reject(d.error); else resolve(d.result);
            }
          };
          ws.addEventListener('message', h);
          ws.send(JSON.stringify({ id: curId, method: m, params: p }));
        });
        await new Promise(r => ws.onopen = r);
        await new Promise(r => setTimeout(r, 2000));

        // Start game
        await send('Runtime.evaluate', { expression: 'window.startGameFromMenu();' });
        await new Promise(r => setTimeout(r, 1200));

        const sceneAudit = await send('Runtime.evaluate', {
          expression: `(() => {
            const app = window._app;
            const scene = app.world?.scene || app.scene;
            const breakdown = {};
            let totalMeshes = 0;
            let visibleMeshes = 0;
            let shadowCasters = 0;
            let strokeMeshes = 0;

            scene.traverse(obj => {
              if (obj.isMesh || obj.isLine || obj.isPoints) {
                totalMeshes++;
                if (obj.visible) visibleMeshes++;
                if (obj.castShadow) shadowCasters++;
                if (obj.name && (obj.name.toLowerCase().includes('stroke') || obj.name.toLowerCase().includes('outline'))) {
                  strokeMeshes++;
                }
                const rootName = obj.parent ? (obj.parent.name || obj.parent.type) : 'root';
                breakdown[rootName] = (breakdown[rootName] || 0) + 1;
              }
            });

            return {
              totalMeshes,
              visibleMeshes,
              shadowCasters,
              strokeMeshes,
              renderCalls: app.renderer?.info?.render?.calls,
              breakdown: Object.entries(breakdown).sort((a,b) => b[1] - a[1]).slice(0, 20)
            };
          })()`,
          returnByValue: true
        });

        console.log('Scene Audit:', JSON.stringify(sceneAudit.result.value, null, 2));

        ws.close();
        chromeProc.kill();
        process.exit(0);
      }
    } catch(e) {}
  }
}

run();
