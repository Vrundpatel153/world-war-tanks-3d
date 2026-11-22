with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Replace the loader interval with rock-solid isEngineFullyReady & onEngineReady architecture
old_loader_logic = """      // Check when 3D engine is initialized, then dismiss loader & apply settings
      let _loaderCheckInterval = setInterval(function() {
        if (window._app && window._app.world && window._app.world.camera) {
          clearInterval(_loaderCheckInterval);
          setTimeout(dismissLoaderAndShowMenu, 350);
          window.applyAllSettings();
        }
      }, 100);

      setTimeout(function() {
        clearInterval(_loaderCheckInterval);
        dismissLoaderAndShowMenu();
      }, 2200);"""

new_loader_logic = """      // PROPER ROBUST ENGINE LIFECYCLE COORDINATOR
      function isEngineFullyReady() {
        const app = window._app;
        if (!app) return false;
        if (app.startup && !app.startup.isReady) return false;
        if (!app.world || !app.world.robot || !app.world.camera) return false;
        const info = app.renderer ? app.renderer.info : null;
        if (!info || info.render.calls === 0) return false;
        return true;
      }

      function onEngineReady() {
        if (window._hasEngineInitialized) return;
        window._hasEngineInitialized = true;
        clearInterval(_loaderCheckInterval);

        // Ensure WebGL Canvas is 100% visible
        const canvas = document.querySelector('#webgl');
        if (canvas) {
          canvas.style.opacity = '1';
          canvas.style.visibility = 'visible';
        }

        // Apply balanced 60 FPS graphics settings
        window.applyAllSettings();

        // Smoothly dismiss loader and open home deck
        dismissLoaderAndShowMenu();
      }

      let _loaderCheckInterval = setInterval(function() {
        if (isEngineFullyReady()) {
          onEngineReady();
        }
      }, 60);

      // Safe timeout (10 seconds) ensuring engine has plenty of time for shaders
      setTimeout(function() {
        if (!window._hasEngineInitialized && window._app && window._app.world) {
          onEngineReady();
        }
      }, 10000);"""

if old_loader_logic in html:
    html = html.replace(old_loader_logic, new_loader_logic)
    print("Replaced loader logic with proper engine lifecycle coordinator")
else:
    print("Warning: old_loader_logic not found")

# Guard startGameFromMenu against unready engine
old_start = """      window.startGameFromMenu = function() {
        window.isGameMenuOpen = false;
        window._hasStartedGame = true;"""

new_start = """      window.startGameFromMenu = function() {
        if (!isEngineFullyReady()) {
          const playTxt = document.querySelector('#btn-deck-play-txt');
          if (playTxt) playTxt.textContent = 'INITIALIZING BATTLEFIELD...';
          const waitTimer = setInterval(() => {
            if (isEngineFullyReady()) {
              clearInterval(waitTimer);
              window.startGameFromMenu();
            }
          }, 80);
          return;
        }

        window.isGameMenuOpen = false;
        window._hasStartedGame = true;"""

if old_start in html:
    html = html.replace(old_start, new_start)
    print("Added isEngineFullyReady guard to startGameFromMenu")
else:
    print("Warning: old_start not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html successfully updated with consistent architecture.")
