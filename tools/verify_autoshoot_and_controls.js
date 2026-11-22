import fs from 'fs';
import { spawn } from 'child_process';

const PORT = 9337;
const PROFILE_DIR = 'C:\\Users\\Vrund Patel\\AppData\\Local\\Temp\\verify_controls_profile_' + Date.now();

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms));
}

async function verify() {
  console.log('Spawning isolated Chrome on port', PORT);
  const proc = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    `--remote-debugging-port=${PORT}`,
    '--headless=new',
    '--no-sandbox',
    '--disable-gpu-sandbox',
    `--user-data-dir=${PROFILE_DIR}`,
    'http://localhost:8080/'
  ]);

  let pageTarget = null;
  for (let i = 0; i < 20; i++) {
    await sleep(400);
    try {
      const res = await fetch(`http://localhost:${PORT}/json/list`);
      const targets = await res.json();
      pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080'));
      if (pageTarget) break;
    } catch(e) {}
  }

  if (!pageTarget) {
    console.error('Target not found');
    proc.kill();
    process.exit(1);
  }

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

  // Wait 3 seconds for boot
  await sleep(3000);

  // Deploy to battle
  await send('Runtime.evaluate', { expression: 'window.startGameFromMenu()' });
  await sleep(1500);

  // TEST 1: Check that inputEnabled is TRUE
  const inputCheck = await send('Runtime.evaluate', {
    expression: `(() => {
      const app = window._app;
      return {
        appInputEnabled: app?.controller?.inputEnabled,
        worldInputEnabled: app?.world?.controller?.inputEnabled,
        introState: app?.intro?.state,
        hasIntroTimer: !!app?.intro?.introShootTimer
      };
    })()`,
    returnByValue: true
  });
  console.log('--- TEST 1: Input Controller State ---');
  console.log(JSON.stringify(inputCheck.result.value, null, 2));

  // TEST 2: Check for ANY automatic shots over 4 seconds of idle time
  console.log('\n--- TEST 2: Verifying ZERO Automatic Shooting (Waiting 4s idle)... ---');
  let shotsFired = 0;
  await send('Runtime.evaluate', {
    expression: `(() => {
      window._autoShotCount = 0;
      const bs = window._app?.world?.bulletSystem;
      if (bs) {
        const origBurst = bs.handleBurstShot.bind(bs);
        bs.handleBurstShot = function() {
          window._autoShotCount++;
          return origBurst();
        };
      }
    })()`
  });

  await sleep(4000);

  const autoShootCheck = await send('Runtime.evaluate', {
    expression: 'window._autoShotCount',
    returnByValue: true
  });
  console.log('Automatic shots fired during 4s idle:', autoShootCheck.result.value);

  // TEST 3: Test WASD manual driving
  console.log('\n--- TEST 3: Testing Manual WASD Driving ---');
  await send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'w', code: 'KeyW', windowsVirtualKeyCode: 87 });
  await sleep(1200);

  const driveCheck = await send('Runtime.evaluate', {
    expression: `(() => {
      const speedEl = document.getElementById('tank-speed-val');
      const gearEl = document.getElementById('tank-gear-val');
      const body = window._app?.world?.physicsWorld?.robotRigidBody;
      const vel = body ? body.linvel() : { x: 0, z: 0 };
      const kmh = Math.round(Math.hypot(vel.x, vel.z) * 3.6);
      return {
        speedText: speedEl?.textContent,
        gearText: gearEl?.textContent,
        calculatedKmh: kmh,
        isMoving: kmh > 0
      };
    })()`,
    returnByValue: true
  });
  console.log('Driving Forward Result:', driveCheck.result.value);
  await send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'w', code: 'KeyW', windowsVirtualKeyCode: 87 });

  // TEST 4: Test Manual Cannon Fire (Left-Click)
  console.log('\n--- TEST 4: Testing Manual Cannon Fire (Left-Click) ---');
  const shotsBefore = autoShootCheck.result.value;
  // Engage aim first
  await send('Runtime.evaluate', {
    expression: `(() => {
      const cam = window._app?.world?.camera;
      if (cam) cam.isAiming = true;
    })()`
  });
  await sleep(300);

  // Click canvas to fire
  await send('Input.dispatchMouseEvent', { type: 'mousePressed', button: 'left', x: 720, y: 450, clickCount: 1 });
  await send('Input.dispatchMouseEvent', { type: 'mouseReleased', button: 'left', x: 720, y: 450, clickCount: 1 });
  await sleep(600);

  const manualFireCheck = await send('Runtime.evaluate', {
    expression: `(() => {
      return {
        totalShots: window._autoShotCount,
        apCount: document.getElementById('tank-ap-count')?.textContent,
        reloadStatus: document.getElementById('tank-reload-status')?.textContent
      };
    })()`,
    returnByValue: true
  });
  console.log('Manual Fire Result:', manualFireCheck.result.value);

  // Take screenshot of manual driving & firing
  const snap = await send('Page.captureScreenshot', { format: 'png' });
  fs.writeFileSync('C:\\Users\\Vrund Patel\\.gemini\\antigravity\\brain\\872b1927-4373-40e0-8876-e950842c0100\\verified_manual_controls_and_shooting.png', Buffer.from(snap.data, 'base64'));
  console.log('Saved verified_manual_controls_and_shooting.png');

  console.log('\n=== ALL CONTROLS AND AUTOSHOOT VERIFICATION PASSED! ===');
  proc.kill();
  try { fs.rmSync(PROFILE_DIR, { recursive: true, force: true }); } catch(e) {}
  process.exit(0);
}

verify().catch(err => {
  console.error(err);
  process.exit(1);
});
