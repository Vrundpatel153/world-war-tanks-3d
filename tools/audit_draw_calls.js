import { spawn } from 'child_process';

const proc = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
  '--remote-debugging-port=9338',
  '--headless=new',
  '--no-sandbox',
  '--disable-gpu-sandbox',
  '--user-data-dir=C:\\Users\\Vrund Patel\\AppData\\Local\\Temp\\test_draw_calls2',
  'http://localhost:8080/'
]);

setTimeout(async () => {
  try {
    const res = await fetch('http://localhost:9338/json/list');
    const targets = await res.json();
    const t = targets.find(x => x.type === 'page' && x.url.includes('8080'));
    const ws = new WebSocket(t.webSocketDebuggerUrl);
    ws.onopen = async () => {
      ws.send(JSON.stringify({ id: 1, method: 'Runtime.evaluate', params: {
        expression: `new Promise(resolve => {
          window.startGameFromMenu();
          setTimeout(() => {
            requestAnimationFrame(() => {
              const app = window._app;
              resolve({
                calls: app?.renderer?.info?.render?.calls,
                triangles: app?.renderer?.info?.render?.triangles,
                pixelRatio: app?.renderer?.getPixelRatio(),
                shadows: app?.renderer?.shadowMap?.enabled
              });
            });
          }, 1500);
        })`,
        awaitPromise: true,
        returnByValue: true
      }}));
    };
    ws.onmessage = (e) => {
      const d = JSON.parse(e.data);
      if (d.id === 1) {
        console.log('Frame render stats:', d.result.result.value);
        proc.kill();
        process.exit(0);
      }
    };
  } catch(err) {
    console.error(err);
    proc.kill();
    process.exit(1);
  }
}, 3000);
