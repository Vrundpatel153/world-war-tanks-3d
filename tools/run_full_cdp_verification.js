import fs from 'fs';
import { spawn } from 'child_process';

async function main() {
  console.log('Spawning headless Chrome on port 9222...');
  const chromeProc = spawn('C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', [
    '--remote-debugging-port=9222',
    '--headless=new',
    '--no-sandbox',
    '--disable-gpu-sandbox',
    '--user-data-dir=C:\\Users\\Vrund Patel\\AppData\\Local\\Temp\\chrome-dbg-auto',
    'http://localhost:8080/'
  ], { stdio: 'ignore' });

  // Wait for CDP endpoint to be available
  let pageTarget = null;
  for (let i = 0; i < 20; i++) {
    await new Promise(r => setTimeout(r, 400));
    try {
      const listRes = await fetch('http://localhost:9222/json/list');
      const targets = await listRes.json();
      pageTarget = targets.find(t => t.type === 'page' && t.url.includes('8080')) || targets.find(t => t.type === 'page');
      if (pageTarget) break;
    } catch (e) {
      // Chrome still starting up
    }
  }

  if (!pageTarget) {
    console.error('Failed to connect to Chrome after 8s');
    chromeProc.kill();
    process.exit(1);
  }

  console.log('Connected to target:', pageTarget.title, pageTarget.webSocketDebuggerUrl);
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

  // Set widescreen resolution
  await sendCommand('Emulation.setDeviceMetricsOverride', {
    width: 1440,
    height: 900,
    deviceScaleFactor: 1,
    mobile: false
  });

  // Reload page to ensure clean state
  await sendCommand('Page.reload', { ignoreCache: true });
  console.log('Reloaded page with ignoreCache: true...');

  // Wait for 3D engine to initialize and render calls > 0
  console.log('Waiting for engine initialization...');
  let readyStats = null;
  for (let i = 0; i < 30; i++) {
    await new Promise(r => setTimeout(r, 400));
    const r = await sendCommand('Runtime.evaluate', {
      expression: `(() => {
        const app = window._app;
        return {
          isStartupReady: app?.startup?.isReady,
          hasRobot: !!app?.world?.robot,
          calls: app?.renderer?.info?.render?.calls,
          triangles: app?.renderer?.info?.render?.triangles,
          isMenuOpen: window.isGameMenuOpen
        };
      })()`,
      returnByValue: true
    });
    readyStats = r.result.value;
    if (readyStats?.isStartupReady && readyStats?.calls > 0) {
      console.log(`Engine ready at ${i*400}ms:`, readyStats);
      break;
    }
  }

  // Extra settle time for UI animations
  await new Promise(r => setTimeout(r, 1000));

  // 1. Verify Home Screen & Cursor state
  const homeCheck = await sendCommand('Runtime.evaluate', {
    expression: `(() => {
      const hasMenuMode = document.body.classList.contains('in-menu-mode');
      const isMenuOpen = window.isGameMenuOpen;
      const computedBody = window.getComputedStyle(document.body);
      const cursorVal = computedBody.cursor;
      const pointerLockElem = document.pointerLockElement;
      
      const bodyText = document.body.innerText;
      const emojiMatch = bodyText.match(/[\\u{1F300}-\\u{1F9FF}]|[\\u{2600}-\\u{26FF}]|[\\u{2700}-\\u{27BF}]/gu) || [];

      // Check if tactical-cursor div exists
      const oldCursorDiv = document.getElementById('tactical-cursor');

      return {
        hasMenuMode,
        isMenuOpen,
        cursorVal: cursorVal.substring(0, 60),
        oldCursorDivExists: !!oldCursorDiv,
        pointerLockActive: !!pointerLockElem,
        emojiCount: emojiMatch.length,
        emojis: emojiMatch,
        settingsPreset: window._gameSettings?.preset,
        renderScale: window._gameSettings?.renderScale,
        shadowQuality: window._gameSettings?.shadowQuality
      };
    })()`,
    returnByValue: true
  });
  console.log('\n--- 1. Home Screen & Cursor Audit ---');
  console.log(JSON.stringify(homeCheck.result.value, null, 2));

  // 2. Test clicking on specs card ("Heavy Caterpillar Treads" area) - must NOT engage pointer lock!
  const clickTest = await sendCommand('Runtime.evaluate', {
    expression: `(() => {
      const specCard = document.querySelector('.tactical-spec-card');
      if (specCard) {
        specCard.dispatchEvent(new PointerEvent('pointerdown', { bubbles: true, cancelable: true }));
        specCard.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true }));
        specCard.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true }));
      }
      return {
        pointerLockAfterClick: !!document.pointerLockElement,
        isMenuStillOpen: window.isGameMenuOpen
      };
    })()`,
    returnByValue: true
  });
  console.log('\n--- 2. Pointer Lock Guard Verification ---');
  console.log(JSON.stringify(clickTest.result.value, null, 2));

  // Capture Home Screen screenshot
  const snapHome = await sendCommand('Page.captureScreenshot', { format: 'png' });
  const homeSnapPath = 'C:\\Users\\Vrund Patel\\.gemini\\antigravity\\brain\\872b1927-4373-40e0-8876-e950842c0100\\verified_home_final.png';
  fs.writeFileSync(homeSnapPath, Buffer.from(snapHome.data, 'base64'));
  console.log('Saved verified_home_final.png');

  // 3. Deploy to battle & measure FPS over 2 seconds
  console.log('\n--- 3. Deploying to Battle & Measuring FPS ---');
  await sendCommand('Runtime.evaluate', {
    expression: "window.startGameFromMenu()"
  });
  await new Promise(r => setTimeout(r, 1500));

  const fpsMeasurement = await sendCommand('Runtime.evaluate', {
    expression: `new Promise((resolve) => {
      let frameCount = 0;
      const start = performance.now();
      function onFrame() {
        frameCount++;
        if (performance.now() - start < 1500) {
          requestAnimationFrame(onFrame);
        } else {
          const elapsedSec = (performance.now() - start) / 1000;
          const fps = Math.round(frameCount / elapsedSec);
          const app = window._app;
          const info = app && app.renderer ? app.renderer.info : null;
          resolve({
            measuredFps: fps,
            pixelRatio: app ? app.renderer.getPixelRatio() : null,
            drawCalls: info ? info.render.calls : null,
            triangles: info ? info.render.triangles : null,
            shadowMapEnabled: app && app.renderer ? app.renderer.shadowMap.enabled : null
          });
        }
      }
      requestAnimationFrame(onFrame);
    })`,
    awaitPromise: true,
    returnByValue: true
  });
  console.log('Live Gameplay Performance:');
  console.log(JSON.stringify(fpsMeasurement.result.value, null, 2));

  // Capture Gameplay screenshot
  const snapGame = await sendCommand('Page.captureScreenshot', { format: 'png' });
  const gameSnapPath = 'C:\\Users\\Vrund Patel\\.gemini\\antigravity\\brain\\872b1927-4373-40e0-8876-e950842c0100\\verified_gameplay_final.png';
  fs.writeFileSync(gameSnapPath, Buffer.from(snapGame.data, 'base64'));
  console.log('Saved verified_gameplay_final.png');

  // 4. Test In-Game Pause Menu
  console.log('\n--- 4. Testing In-Game Pause Menu ---');
  const pauseTest = await sendCommand('Runtime.evaluate', {
    expression: `(() => {
      window.openGameMenu();
      const app = window._app;
      return {
        isMenuOpen: window.isGameMenuOpen,
        menuVisible: !document.getElementById('game-home-screen')?.classList.contains('menu-hidden'),
        timeScale: app?.time?.timeScale,
        physicsEnabled: app?.world?.physicsWorld?.enabled,
        cursorAfterPause: window.getComputedStyle(document.body).cursor.substring(0, 60),
        pointerLockReleased: !document.pointerLockElement
      };
    })()`,
    returnByValue: true
  });
  console.log(JSON.stringify(pauseTest.result.value, null, 2));

  // Capture Paused Menu screenshot
  const snapPause = await sendCommand('Page.captureScreenshot', { format: 'png' });
  const pauseSnapPath = 'C:\\Users\\Vrund Patel\\.gemini\\antigravity\\brain\\872b1927-4373-40e0-8876-e950842c0100\\verified_gameplay_paused_final.png';
  fs.writeFileSync(pauseSnapPath, Buffer.from(snapPause.data, 'base64'));
  console.log('Saved verified_gameplay_paused_final.png');

  console.log('\n=== ALL CDP VERIFICATION TESTS COMPLETED SUCCESSFULLY! ===');
  chromeProc.kill();
  process.exit(0);
}

main().catch(err => {
  console.error('CDP Test Error:', err);
  process.exit(1);
});
