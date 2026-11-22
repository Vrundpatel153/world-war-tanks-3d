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

  // Open modal
  await sendCommand('Runtime.evaluate', { expression: "window.openMenuModal('modal-options')" });
  await new Promise(r => setTimeout(r, 200));

  // Evaluate DOM for tabs
  const res = await sendCommand('Runtime.evaluate', {
    expression: `(() => {
      const bar = document.querySelector('.settings-tabs-bar');
      const b1 = document.querySelector('#tabbtn-graphics');
      const bStyle = window.getComputedStyle(b1);
      return {
        barBox: bar?.getBoundingClientRect(),
        b1Box: b1?.getBoundingClientRect(),
        b1Display: bStyle.display,
        b1Height: bStyle.height,
        b1Padding: bStyle.padding,
        b1LineHeight: bStyle.lineHeight,
        b1Overflow: bStyle.overflow,
        matchedRules: Array.from(document.styleSheets).flatMap(s => {
          try {
            return Array.from(s.cssRules).filter(r => r.selectorText && (r.selectorText.includes('settings-tab') || r.selectorText.includes('.menu-modal button'))).map(r => r.cssText);
          } catch(e) { return []; }
        })
      };
    })()`,
    returnByValue: true
  });
  console.log(JSON.stringify(res.result.value, null, 2));
  process.exit(0);
}
main();
