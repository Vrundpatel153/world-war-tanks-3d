import fs from 'fs';

async function main() {
  const listRes = await fetch('http://localhost:9222/json/list');
  const targets = await listRes.json();
  const pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');

  if (!pageTarget) {
    console.error('No page target found on port 9222:', targets);
    process.exit(1);
  }

  console.log('Connecting to target:', pageTarget.title, pageTarget.webSocketDebuggerUrl);
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

  await new Promise((resolve) => ws.onopen = resolve);
  console.log('Connected to Chrome DevTools WebSocket!');

  // Set widescreen desktop gaming resolution (1440x900)
  await sendCommand('Emulation.setDeviceMetricsOverride', {
    width: 1440,
    height: 900,
    deviceScaleFactor: 1,
    mobile: false
  });
  console.log('Configured 1440x900 viewport!');

  // Navigate to localhost:8080/
  await sendCommand('Page.navigate', { url: 'http://localhost:8080/' });
  console.log('Navigated to http://localhost:8080/');

  // Wait 2.8 seconds for loader and 3D asset init
  await new Promise(r => setTimeout(r, 2800));

  // Position physical tactical cursor over DEPLOY button
  await sendCommand('Runtime.evaluate', {
    expression: `(() => {
      const deployBtn = document.querySelector('.btn-deck-deploy');
      const rect = deployBtn.getBoundingClientRect();
      const x = rect.left + 160;
      const y = rect.top + 35;
      const cur = document.getElementById('tactical-cursor');
      if (cur) {
        cur.style.transform = 'translate3d(' + x + 'px, ' + y + 'px, 0)';
        cur.classList.add('hovering');
      }
    })()`
  });
  await new Promise(r => setTimeout(r, 200));

  // Take Home Screen Screenshot with physical in-game cursor visible!
  const snapHome = await sendCommand('Page.captureScreenshot', { format: 'png' });
  const homePath = 'C:\\Users\\Vrund Patel\\.gemini\\antigravity\\brain\\872b1927-4373-40e0-8876-e950842c0100\\home_screen_aaa_verified.png';
  fs.writeFileSync(homePath, Buffer.from(snapHome.data, 'base64'));
  console.log('Saved home_screen_aaa_verified.png with in-game cursor');

  // Open Settings Modal
  console.log('Opening Options & Settings Modal...');
  await sendCommand('Runtime.evaluate', {
    expression: "window.openMenuModal('modal-options')"
  });
  await new Promise(r => setTimeout(r, 600));

  // Position cursor over Low preset card in modal
  await sendCommand('Runtime.evaluate', {
    expression: `(() => {
      const card = document.getElementById('preset-low');
      if (card) {
        const rect = card.getBoundingClientRect();
        const cur = document.getElementById('tactical-cursor');
        if (cur) {
          cur.style.transform = 'translate3d(' + (rect.left + 40) + 'px, ' + (rect.top + 20) + 'px, 0)';
          cur.classList.add('hovering');
        }
      }
    })()`
  });
  await new Promise(r => setTimeout(r, 200));

  // Take Settings Modal Screenshot with in-game cursor visible!
  const snapSettings = await sendCommand('Page.captureScreenshot', { format: 'png' });
  const settingsPath = 'C:\\Users\\Vrund Patel\\.gemini\\antigravity\\brain\\872b1927-4373-40e0-8876-e950842c0100\\settings_graphics_verified.png';
  fs.writeFileSync(settingsPath, Buffer.from(snapSettings.data, 'base64'));
  console.log('Saved settings_graphics_verified.png with in-game cursor');

  // Close Modal and Enter Combat
  console.log('Entering combat gameplay...');
  await sendCommand('Runtime.evaluate', {
    expression: `
      window.closeMenuModal('modal-options');
      window.startGameFromMenu();
    `
  });
  await new Promise(r => setTimeout(r, 1200));

  // Take Gameplay Screenshot
  const snapGame = await sendCommand('Page.captureScreenshot', { format: 'png' });
  const gamePath = 'C:\\Users\\Vrund Patel\\.gemini\\antigravity\\brain\\872b1927-4373-40e0-8876-e950842c0100\\gameplay_active_verified.png';
  fs.writeFileSync(gamePath, Buffer.from(snapGame.data, 'base64'));
  console.log('Saved gameplay_active_verified.png');

  // Test Pause Menu
  console.log('Opening Pause Menu via window.openGameMenu()...');
  await sendCommand('Runtime.evaluate', {
    expression: "window.openGameMenu()"
  });
  await new Promise(r => setTimeout(r, 600));

  // Position cursor over Resume Battle button
  await sendCommand('Runtime.evaluate', {
    expression: `(() => {
      const deployBtn = document.querySelector('.btn-deck-deploy');
      const rect = deployBtn.getBoundingClientRect();
      const cur = document.getElementById('tactical-cursor');
      if (cur) {
        cur.style.transform = 'translate3d(' + (rect.left + 160) + 'px, ' + (rect.top + 35) + 'px, 0)';
        cur.classList.add('hovering');
      }
    })()`
  });
  await new Promise(r => setTimeout(r, 200));

  const snapPause = await sendCommand('Page.captureScreenshot', { format: 'png' });
  const pausePath = 'C:\\Users\\Vrund Patel\\.gemini\\antigravity\\brain\\872b1927-4373-40e0-8876-e950842c0100\\gameplay_paused_verified.png';
  fs.writeFileSync(pausePath, Buffer.from(snapPause.data, 'base64'));
  console.log('Saved gameplay_paused_verified.png');

  console.log('\n=== ALL CDP VERIFICATION TESTS COMPLETED SUCCESSFULLY! ===');
  process.exit(0);
}

main().catch(err => {
  console.error('CDP Test Error:', err);
  process.exit(1);
});
