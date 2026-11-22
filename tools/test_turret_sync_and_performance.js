import fs from 'fs';
import { spawn } from 'child_process';

const ARTIFACT_DIR = 'C:\\Users\\Vrund Patel\\.gemini\\antigravity\\brain\\872b1927-4373-40e0-8876-e950842c0100';
const CDP_PORT = 9338;
const TEMP_PROFILE = 'C:\\Users\\Vrund Patel\\AppData\\Local\\Temp\\isolated_turret_test_' + Date.now();

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function run() {
  console.log('[1/7] Spawning isolated Chrome on port ' + CDP_PORT + '...');
  const chromeProc = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--remote-debugging-port=' + CDP_PORT,
    '--headless=new',
    '--no-sandbox',
    '--disable-gpu-sandbox',
    '--user-data-dir=' + TEMP_PROFILE,
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-sync',
    '--disable-background-networking',
    '--enable-gpu-rasterization',
    '--enable-webgl',
    '--ignore-gpu-blocklist',
    'http://localhost:8080/'
  ], { stdio: 'ignore' });

  let pageTarget = null;
  for (let i = 0; i < 25; i++) {
    await sleep(400);
    try {
      const res = await fetch('http://localhost:' + CDP_PORT + '/json/list');
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

  await send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false });
  await send('Page.reload', { ignoreCache: true });
  console.log('[2/7] Page reloaded. Waiting for engine lifecycle...');

  // Wait for window._app and world
  for (let i = 0; i < 30; i++) {
    await sleep(250);
    const r = await send('Runtime.evaluate', {
      expression: '!!(window._app && window._app.world && window._app.world.renderer)'
    });
    if (r.result?.value) {
      console.log('Engine ready at ' + (i * 250) + 'ms');
      break;
    }
  }

  await sleep(1000);

  // Deploy to battle
  console.log('[3/7] Deploying to battle...');
  await send('Runtime.evaluate', {
    expression: 'window.startGameFromMenu();'
  });
  await sleep(1000);

  // Take screenshot 1: Deployed
  const snap1 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(ARTIFACT_DIR + '/turret_test_1_deployed.png', Buffer.from(snap1.data, 'base64'));

  // Test Camera & Turret Look Sync at multiple angles
  console.log('[4/7] Testing 360 Camera & Turret Sync...');
  const anglesToTest = [0, 0.8, 1.6, 2.5, 3.14, 4.2, 5.5];
  const syncResults = [];

  for (const yaw of anglesToTest) {
    // Set orbit yaw
    await send('Runtime.evaluate', {
      expression: `
        if (window._app && window._app.world && window._app.world.camera) {
          const cam = window._app.world.camera;
          cam._targetOrbitYaw = ${yaw};
          cam._orbitYaw = ${yaw};
        }
      `
    });

    // Wait a couple frames for visual update
    await sleep(100);

    const check = await send('Runtime.evaluate', {
      expression: `
        (() => {
          const cam = window._app.world.camera;
          const robot = window._app.world.robot;
          const turret = robot && robot.model && robot.model.turret;
          if (!turret || !cam) return { error: 'No turret or cam' };
          
          return {
            targetYaw: cam._orbitYaw.toFixed(2),
            turretRotY: turret.rotation.y.toFixed(3),
            turretQuat: { x: turret.quaternion.x.toFixed(2), y: turret.quaternion.y.toFixed(2), z: turret.quaternion.z.toFixed(2), w: turret.quaternion.w.toFixed(2) }
          };
        })()
      `,
      returnByValue: true
    });
    syncResults.push(check.result.value);
  }
  console.log('Sync Results across 7 angles:', JSON.stringify(syncResults, null, 2));

  // Take screenshot 2: After Turret Rotation
  const snap2 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(ARTIFACT_DIR + '/turret_test_2_rotated.png', Buffer.from(snap2.data, 'base64'));

  // Test Left Click Firing (unblocked)
  console.log('[5/7] Testing Manual Cannon Firing...');
  const beforeShot = await send('Runtime.evaluate', {
    expression: 'document.querySelector(".tactical-hud__spec-value")?.textContent',
    returnByValue: true
  });
  console.log('AP before shot:', beforeShot.result?.value);

  // Trigger manual cannon fire directly or via space/mouse
  await send('Runtime.evaluate', {
    expression: 'window._app.world.bulletSystem.handleBurstShot();'
  });
  await sleep(400);

  const afterShot = await send('Runtime.evaluate', {
    expression: `(() => {
      const el = document.querySelector('#aim-required-alert');
      const alertDisplay = el ? window.getComputedStyle(el).display : 'none';
      const ap = document.querySelector(".tactical-hud__spec-value")?.textContent;
      return { ap, alertDisplay };
    })()`,
    returnByValue: true
  });
  console.log('Shot Result:', afterShot.result.value);

  // Take screenshot 3: Firing
  const snap3 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(ARTIFACT_DIR + '/turret_test_3_fired.png', Buffer.from(snap3.data, 'base64'));

  // Measure 60 FPS Performance
  console.log('[6/7] Benchmarking FPS performance over 90 frames...');
  const perfData = await send('Runtime.evaluate', {
    expression: `new Promise(resolve => {
      let frames = 0;
      let start = performance.now();
      function count() {
        frames++;
        if (frames < 90) {
          requestAnimationFrame(count);
        } else {
          let elapsed = performance.now() - start;
          let fps = Math.round((frames / elapsed) * 1000);
          resolve({ fps, elapsedMs: elapsed.toFixed(1), frameCount: frames });
        }
      }
      requestAnimationFrame(count);
    })`,
    awaitPromise: true,
    returnByValue: true
  });
  console.log('Performance Benchmark:', perfData.result.value);

  // Pause menu test
  console.log('[7/7] Testing Pause Menu and ESC...');
  await send('Runtime.evaluate', { expression: 'window.openGameMenu();' });
  await sleep(400);

  const snap4 = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync(ARTIFACT_DIR + '/turret_test_4_pause_menu.png', Buffer.from(snap4.data, 'base64'));

  ws.close();
  chromeProc.kill();
  try { fs.rmSync(TEMP_PROFILE, { recursive: true, force: true }); } catch(e) {}

  console.log('=== TEST COMPLETED SUCCESSFULLY ===');
}

run().catch(err => {
  console.error('Test error:', err);
  process.exit(1);
});
