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
  await new Promise(r => setTimeout(r, 2000));

  const res = await send('Runtime.evaluate', {
    expression: `(() => {
      const canvas = document.querySelector('#webgl');
      let cur = canvas;
      const chain = [];
      while (cur) {
        chain.push({
          tag: cur.tagName,
          id: cur.id,
          className: cur.className,
          inlineOpacity: cur.style ? cur.style.opacity : '',
          computedOpacity: window.getComputedStyle(cur).opacity,
          display: window.getComputedStyle(cur).display,
          visibility: window.getComputedStyle(cur).visibility,
          zIndex: window.getComputedStyle(cur).zIndex
        });
        cur = cur.parentElement;
      }
      return chain;
    })()`,
    returnByValue: true
  });
  console.log('Opacity chain:', JSON.stringify(res.result.value, null, 2));
  process.exit(0);
}
main().catch(err => { console.error(err); process.exit(1); });
