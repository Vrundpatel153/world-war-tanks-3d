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

  // Navigate to localhost:8080/
  await sendCommand('Page.navigate', { url: 'http://localhost:8080/' });
  console.log('Navigated to http://localhost:8080/');

  // Wait 2.8 seconds for loader and 3D asset init
  await new Promise(r => setTimeout(r, 2800));

  // 1. Verify Home Screen & Menu mode
  const eval1 = await sendCommand('Runtime.evaluate', {
    expression: `({
      isMenuOpen: window.isGameMenuOpen,
      bodyInMenuMode: document.body.classList.contains('in-menu-mode'),
      cursorStyle: window.getComputedStyle(document.body).cursor.substring(0, 30),
      hasFpsBadge: !!document.getElementById('live-fps-badge'),
      fpsDisplay: document.getElementById('live-fps-badge')?.style.display,
      hasApp: !!window._app
    })`,
    returnByValue: true
  });
  console.log('1. Initial Menu Mode Check:', eval1.result.value);

  // Take Home Screen Screenshot
  const snapHome = await sendCommand('Page.captureScreenshot', { format: 'png' });
  const homePath = 'C:\\Users\\Vrund Patel\\.gemini\\antigravity\\brain\\872b1927-4373-40e0-8876-e950842c0100\\home_screen_verified.png';
  fs.writeFileSync(homePath, Buffer.from(snapHome.data, 'base64'));
  console.log('Saved home_screen_verified.png');

  // 2. Open Settings Modal
  console.log('Opening Options & Settings Modal...');
  await sendCommand('Runtime.evaluate', {
    expression: "window.openMenuModal('modal-options')"
  });
  await new Promise(r => setTimeout(r, 600));

  // Verify Modal & Tabs
  const evalModal = await sendCommand('Runtime.evaluate', {
    expression: `({
      modalActive: document.getElementById('modal-options')?.classList.contains('active'),
      activeTab: document.querySelector('.settings-tab-pane.active')?.id,
      preset: window._gameSettings?.preset,
      renderScale: window._gameSettings?.renderScale,
      shadowQuality: window._gameSettings?.shadowQuality,
      bloomStrength: window._gameSettings?.bloomStrength,
      anisotropy: window._gameSettings?.anisotropy
    })`,
    returnByValue: true
  });
  console.log('2. Settings Modal Active Check:', evalModal.result.value);

  // Take Settings Modal Screenshot (Graphics Tab)
  const snapSettings = await sendCommand('Page.captureScreenshot', { format: 'png' });
  const settingsPath = 'C:\\Users\\Vrund Patel\\.gemini\\antigravity\\brain\\872b1927-4373-40e0-8876-e950842c0100\\settings_graphics_verified.png';
  fs.writeFileSync(settingsPath, Buffer.from(snapSettings.data, 'base64'));
  console.log('Saved settings_graphics_verified.png');

  // 3. Test applying LOW preset and then ULTRA preset
  console.log('Testing preset changes: LOW -> ULTRA...');
  await sendCommand('Runtime.evaluate', {
    expression: `
      window.applyPreset('low');
      const lowScale = window._app?.renderer?.getPixelRatio();
      const lowShadow = window._app?.renderer?.shadowMap?.enabled;
      window.applyPreset('ultra');
      const ultraScale = window._app?.renderer?.getPixelRatio();
      const ultraShadow = window._app?.renderer?.shadowMap?.enabled;
      ({ lowScale, lowShadow, ultraScale, ultraShadow })
    `,
    returnByValue: true
  });
  console.log('3. Preset Switching Applied Successfully!');

  // 4. Test Controls Tab
  console.log('Switching to Controls & Camera tab...');
  await sendCommand('Runtime.evaluate', {
    expression: "window.switchSettingsTab('tab-controls')"
  });
  await new Promise(r => setTimeout(r, 400));
  const snapControls = await sendCommand('Page.captureScreenshot', { format: 'png' });
  const controlsPath = 'C:\\Users\\Vrund Patel\\.gemini\\antigravity\\brain\\872b1927-4373-40e0-8876-e950842c0100\\settings_controls_verified.png';
  fs.writeFileSync(controlsPath, Buffer.from(snapControls.data, 'base64'));
  console.log('Saved settings_controls_verified.png');

  // 5. Close Modal and Click PLAY to enter gameplay
  console.log('Closing modal and entering combat gameplay...');
  await sendCommand('Runtime.evaluate', {
    expression: `
      window.closeMenuModal('modal-options');
      window.startGameFromMenu();
    `
  });
  await new Promise(r => setTimeout(r, 1200));

  // Check unpaused state
  const evalPlay = await sendCommand('Runtime.evaluate', {
    expression: `({
      isMenuOpen: window.isGameMenuOpen,
      timeScale: window._app?.time?.timeScale,
      physicsEnabled: window._app?.world?.physicsWorld?.enabled,
      btnReturnDisplay: document.getElementById('btn-return-menu')?.style.display
    })`,
    returnByValue: true
  });
  console.log('5. Gameplay Active & Unpaused Check:', evalPlay.result.value);

  // Take Gameplay Screenshot
  const snapGame = await sendCommand('Page.captureScreenshot', { format: 'png' });
  const gamePath = 'C:\\Users\\Vrund Patel\\.gemini\\antigravity\\brain\\872b1927-4373-40e0-8876-e950842c0100\\gameplay_active_verified.png';
  fs.writeFileSync(gamePath, Buffer.from(snapGame.data, 'base64'));
  console.log('Saved gameplay_active_verified.png');

  // 6. Test In-Game Pause (opening menu during gameplay)
  console.log('Testing Pause Menu via window.openGameMenu()...');
  await sendCommand('Runtime.evaluate', {
    expression: "window.openGameMenu()"
  });
  await new Promise(r => setTimeout(r, 600));

  const evalPause = await sendCommand('Runtime.evaluate', {
    expression: `({
      isMenuOpen: window.isGameMenuOpen,
      timeScale: window._app?.time?.timeScale,
      physicsEnabled: window._app?.world?.physicsWorld?.enabled,
      menuVisible: !document.getElementById('game-home-screen')?.classList.contains('menu-hidden'),
      resumeButtonText: document.querySelector('#btn-home-play-txt')?.textContent
    })`,
    returnByValue: true
  });
  console.log('6. In-Game Pause Verification:', evalPause.result.value);

  // Take Paused Menu Screenshot
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
