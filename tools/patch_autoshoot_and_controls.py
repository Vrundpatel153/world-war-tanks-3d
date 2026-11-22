with open('assets/CJn-Xu8f.js', 'r', encoding='utf-8') as f:
    cjn = f.read()

# 1. Eliminate automatic shooting from intro state machine
idx = cjn.find('triggerIntroShoot(){')
idx2 = cjn.find('stopIntroShooting(){')
if idx != -1 and idx2 != -1:
    target = cjn[idx:idx2]
    cjn = cjn.replace(target, 'triggerIntroShoot(){return;}')
    print('1. Patched triggerIntroShoot in CJn-Xu8f.js')

idx_slow = cjn.find('startIntroSlowTime(){')
idx_slow2 = cjn.find('triggerIntroShoot(){')
if idx_slow != -1 and idx_slow2 != -1:
    target_slow = cjn[idx_slow:idx_slow2]
    cjn = cjn.replace(target_slow, 'startIntroSlowTime(){return;}')
    print('2. Patched startIntroSlowTime in CJn-Xu8f.js')

with open('assets/CJn-Xu8f.js', 'w', encoding='utf-8') as f:
    f.write(cjn)

# 2. Enable keyboard/mouse input by default in DPqB0RfP.js
with open('assets/DPqB0RfP.js', 'r', encoding='utf-8') as f:
    dp = f.read()

dp_target = 'this.shootRequested=!1,this.inputEnabled=!1,this.world=null'
dp_replacement = 'this.shootRequested=!1,this.inputEnabled=!0,this.world=null'
if dp_target in dp:
    dp = dp.replace(dp_target, dp_replacement)
    print('3. Enabled default inputEnabled in DPqB0RfP.js constructor')
else:
    print('dp_target not found in DPqB0RfP.js')

with open('assets/DPqB0RfP.js', 'w', encoding='utf-8') as f:
    f.write(dp)

# 3. Update index.html to wire manual shooting and ensure inputEnabled on world controller
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update triggerShoot to fire the 3D tank cannon
trigger_target = """      function triggerShoot() {
        if (reloadTimer > 0) return;
        reloadTimer = 0.25;"""

trigger_replacement = """      function triggerShoot() {
        if (reloadTimer > 0) return;
        reloadTimer = 0.25;

        // FIRE 3D TANK HIGH-VELOCITY CANNON
        try {
          const bs = window._app && window._app.world ? window._app.world.bulletSystem : null;
          if (bs && typeof bs.handleBurstShot === 'function') {
            bs.handleBurstShot();
          }
        } catch(e) {}"""

if trigger_target in html:
    html = html.replace(trigger_target, trigger_replacement)
    print('4. Connected triggerShoot to 3D tank bulletSystem in index.html')
else:
    print('trigger_target not found in index.html')

# Ensure controller input is permanently enabled in startGameFromMenu
start_target = """        // UNPAUSE 3D SIMULATION & RESTORE AUDIO
        if (window._app) {"""

start_replacement = """        // STOP ANY INTRO AUTOPILOT / SHOOTING
        if (window._app && window._app.intro) {
          try {
            window._app.intro.stopIntroShooting?.();
            if (window._app.intro.introShootTimer) {
              window._app.intro.introShootTimer.kill?.();
              window._app.intro.introShootTimer = null;
            }
            window._app.intro.state = 'done';
          } catch(e) {}
        }

        // PERMANENTLY ENABLE TANK CONTROLS (WASD, MOUSE, TURRET)
        if (window._app) {
          if (window._app.controller) window._app.controller.inputEnabled = true;
          if (window._app.world && window._app.world.controller) window._app.world.controller.inputEnabled = true;
        }

        // UNPAUSE 3D SIMULATION & RESTORE AUDIO
        if (window._app) {"""

if start_target in html:
    html = html.replace(start_target, start_replacement)
    print('5. Added input enablement and intro shutdown in startGameFromMenu')
else:
    print('start_target not found in index.html')

# Also in onEngineReady
ready_target = """        // Smoothly dismiss loader and open home deck
        dismissLoaderAndShowMenu();"""

ready_replacement = """        // Ensure intro auto-shooting is neutralized immediately
        if (window._app && window._app.intro) {
          try {
            window._app.intro.stopIntroShooting?.();
            if (window._app.intro.introShootTimer) {
              window._app.intro.introShootTimer.kill?.();
              window._app.intro.introShootTimer = null;
            }
            window._app.intro.state = 'done';
          } catch(e) {}
        }
        if (window._app && window._app.controller) {
          window._app.controller.inputEnabled = true;
        }

        // Smoothly dismiss loader and open home deck
        dismissLoaderAndShowMenu();"""

if ready_target in html:
    html = html.replace(ready_target, ready_replacement)
    print('6. Added intro shutdown in onEngineReady')
else:
    print('ready_target not found in index.html')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('All patches applied successfully!')
