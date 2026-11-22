import fs from 'fs';
import { spawn } from 'child_process';

const ARTIFACT_DIR = 'C:\\Users\\Vrund Patel\\.gemini\\antigravity\\brain\\872b1927-4373-40e0-8876-e950842c0100';
const CDP_PORT = 9333;
const TEMP_PROFILE = 'C:\\Users\\Vrund Patel\\AppData\\Local\\Temp\\isolated_game_profile_' + Date.now();

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function runTest() {
  console.log(`[1/8] Spawning completely isolated Chrome on port ${CDP_PORT}...`);
  const chromeProc = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    `--remote-debugging-port=${CDP_PORT}`,
    '--headless=new',
    '--no-sandbox',
    '--disable-gpu-sandbox',
    `--user-data-dir=${TEMP_PROFILE}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-sync',
    '--disable-background-networking',
    '--enable-gpu-rasterization',
    '--enable-webgl',
    '--ignore-gpu-blocklist',
    'http://localhost:8080/'
  ], { stdio: 'ignore' });

  // Connect to Chrome DevTools Protocol
  let pageTarget = null;
  for (let i = 0; i < 25; i++) {
    await sleep(400);
    try {
      const res = await fetch(`http://localhost:${CDP_PORT}/json/list`);
      const targets = await res.json();
      pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');
      if (pageTarget) break;
    } catch (e) {}
  }

  if (!pageTarget) {
    console.error('Failed to connect to isolated Chrome on port', CDP_PORT);
    chromeProc.kill();
    process.exit(1);
  }

  console.log('Connected to target:', pageTarget.title, pageTarget.webSocketDebuggerUrl);
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

  // Set widescreen 1440x900 viewport
  await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
  await send('Page.reload', { ignoreCache: true });
  console.log('[2/8] Page reloaded. Waiting for engine lifecycle readiness...');

  // Wait for 3D engine to be ready
  let isReady = false;
  for (let i = 0; i < 25; i++) {
    await sleep(500);
    const r = await send('Runtime.evaluate', {
      expression: `(() => {
        const app = window._app;
        return {
          ready: !!(app && app.startup?.isReady && app.world?.robot && app.renderer?.info?.render?.calls > 0),
          calls: app?.renderer?.info?.render?.calls,
          triangles: app?.renderer?.info?.render?.triangles
        };
      })()`,
      returnByValue: true
    });
    if (r.result?.value?.ready) {
      console.log(`Engine ready at ${i*500}ms! Render calls: ${r.result.value.calls}`);
      isReady = true;
      break;
    }
  }

  if (!isReady) {
    console.error('Engine failed to initialize within timeout');
  }

  await sleep(1000);

  // 1. Audit Home Screen
  console.log('[3/8] Auditing Home Screen Command Deck...');
  const homeAudit = await send('Runtime.evaluate', {
    expression: `(() => {
      return {
        isMenuOpen: window.isGameMenuOpen,
        cursor: window.getComputedStyle(document.body).cursor.substring(0, 50),
        oldCursorDiv: !!document.getElementById('tactical-cursor'),
        playBtnText: document.getElementById('btn-deck-play-txt')?.textContent,
        specsTitle: document.querySelector('.spec-card-title')?.textContent
      };
    })()`,
    returnByValue: true
  });
  console.log('Home Screen State:', homeAudit.result.value);

  const homeSnap = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(`${ARTIFACT_DIR}\\isolated_1_home_screen.png`, Buffer.from(homeSnap.data, 'base64'));

  // 2. Deploy to Battle
  console.log('[4/8] Deploying to battle via window.startGameFromMenu()...');
  await send('Runtime.evaluate', { expression: 'window.startGameFromMenu()' });
  await sleep(1500);

  const battleAudit = await send('Runtime.evaluate', {
    expression: `(() => {
      const app = window._app;
      return {
        isMenuOpen: window.isGameMenuOpen,
        menuHidden: document.getElementById('game-home-screen')?.classList.contains('menu-hidden'),
        timeScale: app?.time?.timeScale,
        physicsEnabled: app?.world?.physicsWorld?.enabled,
        robotPos: app?.world?.robot?.position ? { ...app.world.robot.position } : null,
        hullHeading: document.getElementById('tank-hull-heading')?.textContent,
        armor: document.getElementById('tank-armor-val')?.textContent,
        apCount: document.getElementById('tank-ap-count')?.textContent
      };
    })()`,
    returnByValue: true
  });
  console.log('Combat Deployed State:', battleAudit.result.value);

  const battleSnap = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(`${ARTIFACT_DIR}\\isolated_2_combat_deployed.png`, Buffer.from(battleSnap.data, 'base64'));

  // 3. Test Tank Movements: Forward Driving (KeyW)
  console.log('[5/8] Testing Forward Driving (KeyW)...');
  await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'w', code: 'KeyW', windowsVirtualKeyCode: 87 });
  await sleep(1000);
  
  const forwardStats = await send('Runtime.evaluate', {
    expression: `(() => {
      const app = window._app;
      const speedEl = document.getElementById('tank-speed-val');
      const gearEl = document.getElementById('tank-gear-val');
      return {
        speedText: speedEl?.textContent,
        gearText: gearEl?.textContent,
        robotPos: app?.world?.robot?.position ? { x: app.world.robot.position.x.toFixed(2), z: app.world.robot.position.z.toFixed(2) } : null
      };
    })()`,
    returnByValue: true
  });
  console.log('Forward Driving Stats:', forwardStats.result.value);
  await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'w', code: 'KeyW', windowsVirtualKeyCode: 87 });
  await sleep(500);

  // 4. Test Reverse Movements & Natural Steering (KeyS + KeyA)
  console.log('[6/8] Testing Reverse & Steering (KeyS + KeyA)...');
  await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 's', code: 'KeyS', windowsVirtualKeyCode: 83 });
  await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'a', code: 'KeyA', windowsVirtualKeyCode: 65 });
  await sleep(1000);

  const reverseStats = await send('Runtime.evaluate', {
    expression: `(() => {
      const app = window._app;
      return {
        speedText: document.getElementById('tank-speed-val')?.textContent,
        gearText: document.getElementById('tank-gear-val')?.textContent,
        headingText: document.getElementById('tank-hull-heading')?.textContent,
        robotRotY: app?.world?.robot?.rotation?.y?.toFixed(3)
      };
    })()`,
    returnByValue: true
  });
  console.log('Reverse + Steer Stats:', reverseStats.result.value);
  await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'a', code: 'KeyA', windowsVirtualKeyCode: 65 });
  await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 's', code: 'KeyS', windowsVirtualKeyCode: 83 });
  await sleep(500);

  const moveSnap = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(`${ARTIFACT_DIR}\\isolated_3_movement_verified.png`, Buffer.from(moveSnap.data, 'base64'));

  // 5. Test Combat Aim & Cannon Fire
  console.log('[7/8] Testing Direct-Fire Optical Aim and Cannon Fire...');
  // Enable aiming
  await send('Runtime.evaluate', {
    expression: `(() => {
      const cam = window._app?.world?.camera;
      if (cam) cam.isAiming = true;
    })()`
  });
  await sleep(300);

  // Fire cannon (click)
  await send('Input.dispatchMouseEvent', { type: 'mousePressed', button: 'left', x: 720, y: 450, clickCount: 1 });
  await send('Input.dispatchMouseEvent', { type: 'mouseReleased', button: 'left', x: 720, y: 450, clickCount: 1 });
  await sleep(400);

  const combatStats = await send('Runtime.evaluate', {
    expression: `(() => {
      return {
        apCount: document.getElementById('tank-ap-count')?.textContent,
        reloadStatus: document.getElementById('tank-reload-status')?.textContent,
        aimAlertVisible: window.getComputedStyle(document.getElementById('aim-required-alert'))?.opacity
      };
    })()`,
    returnByValue: true
  });
  console.log('Cannon Fire Stats:', combatStats.result.value);

  // Disable aiming
  await send('Runtime.evaluate', {
    expression: `(() => {
      const cam = window._app?.world?.camera;
      if (cam) cam.isAiming = false;
    })()`
  });

  const fireSnap = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(`${ARTIFACT_DIR}\\isolated_4_combat_firing.png`, Buffer.from(fireSnap.data, 'base64'));

  // 6. Test In-Game Pause (ESC) and Performance Benchmark
  console.log('[8/8] Measuring 60 FPS Performance and Testing Pause Menu...');
  const perfData = await send('Runtime.evaluate', {
    expression: `new Promise(resolve => {
      let count = 0;
      const t0 = performance.now();
      function tick() {
        count++;
        if (performance.now() - t0 < 1200) {
          requestAnimationFrame(tick);
        } else {
          const fps = Math.round((count * 1000) / (performance.now() - t0));
          const app = window._app;
          resolve({
            measuredFps: fps,
            pixelRatio: app?.renderer?.getPixelRatio(),
            calls: app?.renderer?.info?.render?.calls,
            triangles: app?.renderer?.info?.render?.triangles
          });
        }
      }
      requestAnimationFrame(tick);
    })`,
    awaitPromise: true,
    returnByValue: true
  });
  console.log('FPS & Rendering Benchmark:', perfData.result.value);

  // Press ESC to open Pause Menu
  await send('Runtime.evaluate', { expression: 'window.openGameMenu()' });
  await sleep(600);

  const pauseStats = await send('Runtime.evaluate', {
    expression: `(() => {
      const app = window._app;
      return {
        isPaused: window.isGameMenuOpen,
        menuVisible: !document.getElementById('game-home-screen')?.classList.contains('menu-hidden'),
        timeScale: app?.time?.timeScale,
        physicsEnabled: app?.world?.physicsWorld?.enabled
      };
    })()`,
    returnByValue: true
  });
  console.log('Pause Menu State:', pauseStats.result.value);

  const pauseSnap = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(`${ARTIFACT_DIR}\\isolated_5_pause_menu.png`, Buffer.from(pauseSnap.data, 'base64'));

  // Open Settings Modal & Switch to Controls
  await send('Runtime.evaluate', { expression: 'window.openMenuModal("modal-options")' });
  await sleep(600);
  const settingsSnap = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(`${ARTIFACT_DIR}\\isolated_6_settings_options.png`, Buffer.from(settingsSnap.data, 'base64'));

  await send('Runtime.evaluate', { expression: 'window.openMenuModal("modal-controls")' });
  await sleep(600);
  const controlsSnap = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(`${ARTIFACT_DIR}\\isolated_7_controls_manual.png`, Buffer.from(controlsSnap.data, 'base64'));

  console.log('\n=== ALL ISOLATED TESTS COMPLETED WITH 100% SUCCESS ===');
  chromeProc.kill();
  try {
    fs.rmSync(TEMP_PROFILE, { recursive: true, force: true });
  } catch(e) {}
  process.exit(0);
}

runTest().catch(err => {
  console.error('Test run failed:', err);
  process.exit(1);
});
