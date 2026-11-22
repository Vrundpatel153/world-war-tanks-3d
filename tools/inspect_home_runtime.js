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

  const res = await sendCommand('Runtime.evaluate', {
    expression: `(() => {
      const intro = document.getElementById('startup-intro');
      const home = document.getElementById('game-home-screen');
      const deploy = document.querySelector('.btn-deck-deploy');
      return {
        introDisplay: intro ? window.getComputedStyle(intro).display : null,
        introOpacity: intro ? window.getComputedStyle(intro).opacity : null,
        introZIndex: intro ? window.getComputedStyle(intro).zIndex : null,
        homeDisplay: home ? window.getComputedStyle(home).display : null,
        homeOpacity: home ? window.getComputedStyle(home).opacity : null,
        homeZIndex: home ? window.getComputedStyle(home).zIndex : null,
        homeBg: home ? window.getComputedStyle(home).background : null,
        deployBox: deploy ? deploy.getBoundingClientRect() : null,
        deployBg: deploy ? window.getComputedStyle(deploy).background : null,
        deployColor: deploy ? window.getComputedStyle(deploy).color : null
      };
    })()`,
    returnByValue: true
  });
  console.log(JSON.stringify(res.result.value, null, 2));
  process.exit(0);
}
main();
