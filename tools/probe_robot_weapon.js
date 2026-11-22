import { spawn } from 'child_process';

const proc = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
  '--remote-debugging-port=9336',
  '--headless=new',
  '--no-sandbox',
  '--disable-gpu-sandbox',
  '--user-data-dir=C:\\Users\\Vrund Patel\\AppData\\Local\\Temp\\test_shoot_probe',
  'http://localhost:8080/'
]);

setTimeout(async () => {
  try {
    const res = await fetch('http://localhost:9336/json/list');
    const targets = await res.json();
    const t = targets.find(x => x.type === 'page' && x.url.includes('8080'));
    const ws = new WebSocket(t.webSocketDebuggerUrl);
    ws.onopen = () => {
      ws.send(JSON.stringify({
        id: 1,
        method: 'Runtime.evaluate',
        params: {
          expression: `(() => {
            const bs = window._app?.world?.bulletSystem;
            return {
              hasBulletSystem: !!bs,
              hasBurst: typeof bs?.handleBurstShot === 'function',
              hasFireSingle: typeof bs?.fireSingleShot === 'function',
              keys: bs ? Object.keys(bs).filter(k => typeof bs[k] === 'function') : []
            };
          })()`,
          returnByValue: true
        }
      }));
    };
    ws.onmessage = (e) => {
      const d = JSON.parse(e.data);
      if (d.id === 1) {
        console.log('BulletSystem probe:', d.result.result.value);
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
