import cp from 'child_process';

const CDP_PORT = 9338;
const TEMP_PROFILE = 'C:\\Users\\Vrund Patel\\AppData\\Local\\Temp\\perf_diag_' + Date.now();
const chromeProc = cp.spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
  '--remote-debugging-port=' + CDP_PORT,
  '--headless=new',
  '--no-sandbox',
  '--disable-gpu-sandbox',
  '--user-data-dir=' + TEMP_PROFILE,
  '--enable-gpu-rasterization',
  '--enable-webgl',
  '--ignore-gpu-blocklist',
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
        await new Promise(r => setTimeout(r, 1000));

        const perfDiag = await send('Runtime.evaluate', {
          expression: `new Promise(resolve => {
            const app = window._app;
            let frame = 0;
            function step() {
              frame++;
              if (frame < 60) {
                requestAnimationFrame(step);
              } else {
                resolve({
                  fps: document.getElementById('live-fps-val')?.textContent,
                  calls: app.renderer?.info?.render?.calls,
                  pixelRatio: app.renderer?.getPixelRatio(),
                  viewport: { w: window.innerWidth, h: window.innerHeight },
                  devicePixelRatio: window.devicePixelRatio,
                  hasPostProcessing: !!app.postProcessing,
                  bloomEnabled: !!app.bloomPass,
                  shadowMapEnabled: !!app.renderer?.shadowMap?.enabled,
                  shadowMapAutoUpdate: !!app.renderer?.shadowMap?.autoUpdate,
                  shadowMapNeedsUpdate: !!app.renderer?.shadowMap?.needsUpdate,
                  settings: window.currentSettings || JSON.parse(localStorage.getItem('world_war_tanks_settings_v2') || '{}')
                });
              }
            }
            requestAnimationFrame(step);
          })`,
          awaitPromise: true,
          returnByValue: true
        });

        console.log('Subsystem diagnostic:', JSON.stringify(perfDiag.result.value, null, 2));

        // Now measure execution times per frame
        const timingDiag = await send('Runtime.evaluate', {
          expression: `new Promise(resolve => {
            const app = window._app;
            const world = app.world;

            let frames = 0;
            let tTotal = 0;
            let tRender = 0;
            let tPhysics = 0;

            const origRender = app.postProcessing.render.bind(app.postProcessing);
            app.postProcessing.render = function() {
              const t0 = performance.now();
              origRender();
              tRender += (performance.now() - t0);
            };

            const startTime = performance.now();
            function measureStep() {
              frames++;
              if (frames < 30) {
                requestAnimationFrame(measureStep);
              } else {
                const totalElapsed = performance.now() - startTime;
                app.postProcessing.render = origRender;
                resolve({
                  totalElapsedMs: totalElapsed.toFixed(2),
                  avgFrameTimeMs: (totalElapsed / frames).toFixed(2),
                  avgRenderPassMs: (tRender / frames).toFixed(2),
                  frames
                });
              }
            }
            requestAnimationFrame(measureStep);
          })`,
          awaitPromise: true,
          returnByValue: true
        });

        console.log('Timing breakdown:', JSON.stringify(timingDiag.result.value, null, 2));

        ws.close();
        chromeProc.kill();
        process.exit(0);
      }
    } catch(e) {}
  }
}

run();
