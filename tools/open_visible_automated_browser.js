import fs from 'fs';
import { spawn } from 'child_process';

const PORT = 9334;
const PROFILE_DIR = 'C:\\Users\\Vrund Patel\\AppData\\Local\\Temp\\tank_game_visible_profile';

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function runVisibleAutomatedTest() {
  console.log(`[1] Launching visible, separate Chrome window on port ${PORT}...`);

  // Ensure clean profile directory
  try {
    fs.mkdirSync(PROFILE_DIR, { recursive: true });
  } catch(e) {}

  const chromeProc = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    `--remote-debugging-port=${PORT}`,
    `--user-data-dir=${PROFILE_DIR}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--window-size=1280,820',
    '--window-position=80,60',
    '--enable-gpu-rasterization',
    '--enable-webgl',
    '--ignore-gpu-blocklist',
    '--disable-sync',
    'http://localhost:8080/'
  ], { detached: true, stdio: 'ignore' });
  chromeProc.unref();

  console.log('[2] Connecting to visible browser via CDP...');
  let pageTarget = null;
  for (let i = 0; i < 30; i++) {
    await sleep(400);
    try {
      const res = await fetch(`http://localhost:${PORT}/json/list`);
      const targets = await res.json();
      pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');
      if (pageTarget) break;
    } catch(e) {}
  }

  if (!pageTarget) {
    console.error('Could not connect to visible Chrome target');
    process.exit(1);
  }

  console.log('Connected to target:', pageTarget.title);
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

  console.log('[3] Waiting for 3D engine readiness...');
  for (let i = 0; i < 25; i++) {
    await sleep(500);
    const r = await send('Runtime.evaluate', {
      expression: `(() => {
        const app = window._app;
        return app && app.startup?.isReady && app.world?.robot && app.renderer?.info?.render?.calls > 0;
      })()`,
      returnByValue: true
    });
    if (r.result?.value) {
      console.log(`Engine ready at ${i*500}ms!`);
      break;
    }
  }

  // Allow user to see the Command Deck for 2 seconds
  console.log('[4] On Home Screen Command Deck: showing specifications and play button...');
  await sleep(2000);

  // Deploy to battle
  console.log('[5] Clicking DEPLOY TO BATTLE: entering 3D open-world simulation...');
  await send('Runtime.evaluate', { expression: 'window.startGameFromMenu()' });
  await sleep(2000);

  // Demonstrate Driving Forward (KeyW)
  console.log('[6] Driving forward (W) through the industrial sector...');
  await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'w', code: 'KeyW', windowsVirtualKeyCode: 87 });
  await sleep(2000);
  await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'w', code: 'KeyW', windowsVirtualKeyCode: 87 });
  await sleep(500);

  // Demonstrate Steering Left while driving (KeyW + KeyA)
  console.log('[7] Turning left (W + A)...');
  await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'w', code: 'KeyW', windowsVirtualKeyCode: 87 });
  await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'a', code: 'KeyA', windowsVirtualKeyCode: 65 });
  await sleep(1200);
  await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'a', code: 'KeyA', windowsVirtualKeyCode: 65 });
  await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'w', code: 'KeyW', windowsVirtualKeyCode: 87 });
  await sleep(500);

  // Demonstrate Natural Reverse Steering (KeyS + KeyA)
  console.log('[8] Testing natural reverse steering (S + A)...');
  await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 's', code: 'KeyS', windowsVirtualKeyCode: 83 });
  await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'a', code: 'KeyA', windowsVirtualKeyCode: 65 });
  await sleep(1500);
  await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'a', code: 'KeyA', windowsVirtualKeyCode: 65 });
  await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 's', code: 'KeyS', windowsVirtualKeyCode: 83 });
  await sleep(600);

  // Demonstrate Optical Aim & Cannon Fire
  console.log('[9] Engaging direct-fire optical zoom aim...');
  await send('Runtime.evaluate', {
    expression: `(() => {
      const cam = window._app?.world?.camera;
      if (cam) cam.isAiming = true;
    })()`
  });
  await sleep(800);

  console.log('[10] Firing 88mm KwK High-Velocity Cannon...');
  await send('Input.dispatchMouseEvent', { type: 'mousePressed', button: 'left', x: 640, y: 400, clickCount: 1 });
  await send('Input.dispatchMouseEvent', { type: 'mouseReleased', button: 'left', x: 640, y: 400, clickCount: 1 });
  await sleep(1000);

  // Release aim
  await send('Runtime.evaluate', {
    expression: `(() => {
      const cam = window._app?.world?.camera;
      if (cam) cam.isAiming = false;
    })()`
  });
  await sleep(800);

  // Demonstrate In-Game Pause (ESC)
  console.log('[11] Pausing combat simulation (ESC key)...');
  await send('Runtime.evaluate', { expression: 'window.openGameMenu()' });
  await sleep(1200);

  // Open Graphics & System Settings
  console.log('[12] Opening Graphics & System Settings modal...');
  await send('Runtime.evaluate', { expression: 'window.openMenuModal("modal-options")' });
  await sleep(1200);

  // Switch to Field Manual / Controls Tab
  console.log('[13] Switching to Field Manual & Keyboard Bindings tab...');
  await send('Runtime.evaluate', { expression: 'window.openMenuModal("modal-controls")' });
  await sleep(1500);

  // Close modal and resume battle
  console.log('[14] Closing modal and resuming battle...');
  await send('Runtime.evaluate', { expression: 'window.closeMenuModal("modal-options"); window.startGameFromMenu();' });
  await sleep(1000);

  // Disconnect CDP so the user has 100% manual control over the open browser window
  console.log('[15] Disconnecting automated CDP controller. Browser window remains open for the user to play!');
  ws.close();

  // Capture final screenshot for artifact record
  console.log('\n=== VISIBLE AUTOMATED BROWSER DEMONSTRATION COMPLETE ===');
  process.exit(0);
}

runVisibleAutomatedTest().catch(err => {
  console.error('Visible browser test error:', err);
  process.exit(1);
});
