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

  await send('DOM.enable');
  await send('CSS.enable');

  const doc = await send('DOM.getDocument');
  const node = await send('DOM.querySelector', { nodeId: doc.root.nodeId, selector: '#webgl' });
  console.log('NodeId:', node.nodeId);

  const matched = await send('CSS.getMatchedStylesForNode', { nodeId: node.nodeId });
  console.log('Inline style:');
  if (matched.inlineStyle) {
    console.log(matched.inlineStyle.cssProperties.filter(p => p.name === 'opacity'));
  }
  console.log('\nMatched rules with opacity:');
  for (const m of matched.matchedCSSRules) {
    const op = m.rule.style.cssProperties.filter(p => p.name === 'opacity');
    if (op.length) {
      console.log('Selector:', m.rule.selectorList.text);
      console.log('Opacity props:', op);
      console.log('Origin:', m.rule.origin, m.rule.styleSheetId);
    }
  }

  process.exit(0);
}
main().catch(err => { console.error(err); process.exit(1); });
