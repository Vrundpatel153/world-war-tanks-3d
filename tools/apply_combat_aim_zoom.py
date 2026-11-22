import os

game_dir = r"C:\Users\Vrund Patel\Desktop\clone-game"

# ==============================================================================
# 1. Patch CQl67Veh.js:
# - Hold Right Click to Aim & Zoom
# - Scroll Press (Button 1) to Lock Aim & Zoom (Fixed)
# - Scroll wheel to Zoom In/Out
# - Camera elevated and projected forward so crosshair sits cleanly above tank
# ==============================================================================
cq_path = os.path.join(game_dir, "assets", "CQl67Veh.js")
with open(cq_path, "r", encoding="utf-8") as f:
    cq = f.read()

# Replace onDown and wheel handlers
target_down_block_start = "this.toggleFpsZoom = () => {"
target_down_block_end = "const onWheel = ev => {"

start_idx = cq.find(target_down_block_start)
end_idx = cq.find(target_down_block_end)

if start_idx != -1 and end_idx != -1:
    new_mouse_block = """this.isAiming = false;
        this.isAimFixed = false;

        this.updateAimState = () => {
            const active = this.isAiming || this.isAimFixed;
            if(active){
                document.body.classList.add("aim-mode-active");
                const b = document.querySelector("#fps-mode-badge");
                if(b){
                    b.textContent = this.isAimFixed ? "● COMBAT AIM [LOCKED - PRESS SCROLL TO EXIT]" : "● COMBAT AIM [HOLDING RIGHT CLICK]";
                    b.style.display = "block";
                }
            } else {
                document.body.classList.remove("aim-mode-active");
                const b = document.querySelector("#fps-mode-badge");
                if(b) b.style.display = "none";
            }
        };

        window.toggleCombatAim = () => {
            this.isAimFixed = !this.isAimFixed;
            this.updateAimState();
        };

        window.addEventListener("auxclick", ev => {
            if(ev.button === 1){
                ev.preventDefault();
                this.isAimFixed = !this.isAimFixed;
                this.updateAimState();
            }
        });

        const onDown = ev => {
            if(ev.target && ev.target.closest && ev.target.closest(".about-page, .statue-page, .case-study-page, .hanzii-page, .email-popup, .submit-item-popup, [role='dialog'], textarea, input, select, button")) return;
            if(ev.button === 1){ // Mouse scroll button click (MMB): Fixed toggle aim
                ev.preventDefault();
                this.isAimFixed = !this.isAimFixed;
                this.updateAimState();
                return;
            }
            if(ev.button === 2){ // Right click: Hold to aim
                ev.preventDefault();
                this.isAiming = true;
                this.updateAimState();
                return;
            }
            this._isDragging = true;
            this._lastPointerX = ev.clientX;
            this._lastPointerY = ev.clientY;
        };

        const onUp = ev => {
            if(ev && ev.button === 2){ // Release right click
                this.isAiming = false;
                this.updateAimState();
            }
            this._isDragging = false;
        };

        window.addEventListener("pointerup", onUp);
        window.addEventListener("mouseup", onUp);
        """
    cq = cq[:start_idx] + new_mouse_block + cq[end_idx:]
    print("1a. CQl67Veh.js: Added Right-Click hold to aim, Scroll click fixed toggle, and onUp handlers.")

# Replace onWheel with smooth continuous zoom
old_wheel = """const onWheel = ev => {
            if(ev.target && ev.target.closest && ev.target.closest(".about-page, .statue-page, .case-study-page, .hanzii-page, .email-popup, .submit-item-popup, [role='dialog'], textarea, input, select")) return;
            const delta = Math.sign(ev.deltaY) * 2.0;
            this._targetOrbitDistance = Math.max(3.0, Math.min(8.5, this._targetOrbitDistance + delta * 0.8));
        };"""

new_wheel = """const onWheel = ev => {
            if(ev.target && ev.target.closest && ev.target.closest(".about-page, .statue-page, .case-study-page, .hanzii-page, .email-popup, .submit-item-popup, [role='dialog'], textarea, input, select")) return;
            const delta = ev.deltaY > 0 ? 0.45 : -0.45;
            this._targetOrbitDistance = Math.max(2.4, Math.min(9.5, this._targetOrbitDistance + delta));
        };"""

if old_wheel in cq:
    cq = cq.replace(old_wheel, new_wheel)
    print("1b. CQl67Veh.js: Updated mouse wheel zoom to smooth 0.45m steps.")

# Update camera focus and position to elevate and project forward
# Find: this.viewAFocus.copy(this.targetEased).add(this.mousePanOffset)...
old_cam_focus = "this.viewAPosition.copy(this.targetEased).add(n).add(this.mousePanOffset).add(this.panViewOffset).add(this.recoilOffset),this.viewAFocus.copy(this.targetEased).add(this.mousePanOffset).add(this.panViewOffset).add(this.recoilOffset),this.viewAFocus.y+=1.4,this.viewAPosition.y+=1.4"

new_cam_focus = """let isAim=this.isAiming||this.isAimFixed;
let camElev=isAim?2.2:1.9;
let focusElev=isAim?1.5:1.2;
this.viewAPosition.copy(this.targetEased).add(n).add(this.mousePanOffset).add(this.panViewOffset).add(this.recoilOffset);
this.viewAPosition.y+=camElev;
this.viewAFocus.copy(this.targetEased).add(this.mousePanOffset).add(this.panViewOffset).add(this.recoilOffset);
let sinY_f=Math.sin(this._orbitYaw),cosY_f=Math.cos(this._orbitYaw);
this.forwardVec.set(-sinY_f,0,-cosY_f).normalize();
this.viewAFocus.addScaledVector(this.forwardVec,22);
this.viewAFocus.y+=focusElev"""

if old_cam_focus in cq:
    cq = cq.replace(old_cam_focus, new_cam_focus)
    print("1c. CQl67Veh.js: Elevated camera and projected focus 22m ahead to completely clear crosshair from tank.")

# Update instance.position and FOV in CQl67Veh.js
old_cam_pos_block = """if(this.isFpsZoom && this.robot && this.robot.model && (this.robot.model.turret || this.robot.model.default)){
    let trt = this.robot.model.turret || this.robot.model.default;
    trt.updateWorldMatrix(!0, !1);
    let tPos = trt.getWorldPosition(this.forwardVec);
    let camY = tPos.y + 0.46;
    let cosP = Math.cos(this._orbitPitch);
    let sinP = Math.sin(this._orbitPitch);
    let sinY = Math.sin(this._orbitYaw);
    let cosY = Math.cos(this._orbitYaw);
    let lkX = -sinY * cosP;
    let lkY = sinP;
    let lkZ = -cosY * cosP;
    this.instance.position.set(tPos.x, camY, tPos.z);
    this.instance.lookAt(tPos.x + lkX * 100, camY + lkY * 100, tPos.z + lkZ * 100);
    this.instance.fov = 20;
    this.instance.updateProjectionMatrix();
} else {
    this.instance.position.copy(this.viewAPosition);
    this.instance.lookAt(this.viewAFocus);
    if(this.instance.fov !== 35){
        this.instance.fov = 35;
        this.instance.updateProjectionMatrix();
    }
}
this.instance.updateMatrixWorld(!0),this.updateOptimalArea()"""

new_cam_pos_block = """this.instance.position.copy(this.viewAPosition);
this.instance.lookAt(this.viewAFocus);
let isAimActive=this.isAiming||this.isAimFixed;
let targetFov=isAimActive?26:35;
if(Math.abs(this.instance.fov-targetFov)>0.1){
    this.instance.fov+=(targetFov-this.instance.fov)*0.18;
    this.instance.updateProjectionMatrix();
}
this.instance.updateMatrixWorld(!0),this.updateOptimalArea()"""

if old_cam_pos_block in cq:
    cq = cq.replace(old_cam_pos_block, new_cam_pos_block)
    print("1d. CQl67Veh.js: Smooth combat aim positioning & FOV transition.")

with open(cq_path, "w", encoding="utf-8") as f:
    f.write(cq)

# ==============================================================================
# 2. Patch B1Nq4Kq6.js:
# - Free mouse aim when aiming (Right Click or Fixed Middle Click)
# - Turret locked forward when casual driving
# ==============================================================================
b1_path = os.path.join(game_dir, "assets", "B1Nq4Kq6.js")
with open(b1_path, "r", encoding="utf-8") as f:
    b1 = f.read()

old_b1_vis = """handlePointerVisual(e,t){
  if(this.camera && this.camera.isFpsZoom){
    this.camera.instance.getWorldDirection(this.aimDir);
    this.aimDir.y = 0;
    if(this.aimDir.lengthSq() > this.aimLengthEpsilon){
      this.aimDir.normalize();
      let n = this.getTurretTargetQuat(this.aimDir);
      this.applyTurretAim(n, t);
    }
    this.aimRaycastAccumulator += t;
    this.aimRaycastAccumulator >= .02 && (this.aimRaycastAccumulator = 0, this.handleAiming(this.rayCaster));
    return;
  }
  this.turretManualAngle=this.turretManualAngle||0;
  let r=2.6;
  if(this.controller&&this.controller.keyPressed){
    (this.controller.keyPressed.has(`KeyQ`)||this.controller.keyPressed.has(`ArrowLeft`))&&(this.turretManualAngle+=r*t);
    (this.controller.keyPressed.has(`KeyE`)||this.controller.keyPressed.has(`ArrowRight`))&&(this.turretManualAngle-=r*t);
    (this.controller.keyPressed.has(`KeyC`)||this.controller.keyPressed.has(`KeyX`)||this.controller.keyPressed.has(`KeyR`))&&(this.turretManualAngle=0);
  }
  let n=this.targetTurretQuat.setFromAxisAngle(this.yAxis,this.turretManualAngle);
  this.applyTurretAim(n,t),this.aimRaycastAccumulator+=t,this.aimRaycastAccumulator>=.02&&(this.aimRaycastAccumulator=0,this.handleAiming(this.rayCaster))
}"""

new_b1_vis = """handlePointerVisual(e,t){
  let cam = this.camera;
  let isAimActive = cam && (cam.isAiming || cam.isAimFixed);

  if(isAimActive){
    // FREE MOUSE AIM: Turret and cannon smoothly track the camera's center crosshair
    this.camera.instance.getWorldDirection(this.aimDir);
    this.aimDir.y = 0;
    if(this.aimDir.lengthSq() > this.aimLengthEpsilon){
      this.aimDir.normalize();
      let n = this.getTurretTargetQuat(this.aimDir);
      this.applyTurretAim(n, t * 2.8);
    }
    this.aimRaycastAccumulator += t;
    this.aimRaycastAccumulator >= .02 && (this.aimRaycastAccumulator = 0, this.handleAiming(this.rayCaster));
    return;
  }

  // Casual driving mode: Turret faces forward with hull heading (W)
  this.turretManualAngle = 0;
  let n = this.targetTurretQuat.setFromAxisAngle(this.yAxis, 0);
  this.applyTurretAim(n, t);
  this.aimRaycastAccumulator += t;
  this.aimRaycastAccumulator >= .02 && (this.aimRaycastAccumulator = 0, this.handleAiming(this.rayCaster));
}"""

if old_b1_vis in b1:
    b1 = b1.replace(old_b1_vis, new_b1_vis)
    print("2. B1Nq4Kq6.js: Turret free aim on Right-Click / Scroll Press aim.")
else:
    print("Warning: old_b1_vis not found in B1Nq4Kq6.js")

with open(b1_path, "w", encoding="utf-8") as f:
    f.write(b1)

# ==============================================================================
# 3. Patch DPqB0RfP.js: Block shoot unless aiming
# ==============================================================================
dp_path = os.path.join(game_dir, "assets", "DPqB0RfP.js")
with open(dp_path, "r", encoding="utf-8") as f:
    dp = f.read()

old_block_shoot = "shouldBlockShoot(){return!!("
new_block_shoot = "shouldBlockShoot(){let cam=this.world&&this.world.camera;if(cam&&!cam.isAiming&&!cam.isAimFixed)return!0;return!!("

if old_block_shoot in dp and "if(cam&&!cam.isAiming" not in dp:
    dp = dp.replace(old_block_shoot, new_block_shoot, 1)
    print("3. DPqB0RfP.js: Blocked shoot unless aiming.")

with open(dp_path, "w", encoding="utf-8") as f:
    f.write(dp)

# ==============================================================================
# 4. Patch index.html: Crosshair CSS, shoot requirement check, and HUD hints
# ==============================================================================
index_path = os.path.join(game_dir, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Update aim required alert in HTML if not present
alert_html = """      <!-- Aim Required Alert Prompt -->
      <div id="aim-required-alert" style="opacity: 0; transition: opacity 0.25s ease; position: absolute; bottom: 84px; left: 50%; transform: translateX(-50%); background: rgba(220, 40, 40, 0.9); color: #ffffff; font-size: 12px; font-weight: 800; padding: 6px 18px; border-radius: 4px; pointer-events: none; letter-spacing: 0.1em; z-index: 1000; box-shadow: 0 0 16px rgba(220, 40, 40, 0.6);">
        HOLD RIGHT CLICK OR PRESS SCROLL TO AIM BEFORE FIRING
      </div>
"""

if 'id="aim-required-alert"' not in html:
    hud_point = '<div id="tank-hud">'
    html = html.replace(hud_point, hud_point + "\n" + alert_html, 1)
    print("4a. index.html: Added aim-required-alert element.")

# Update shoot listener to only shoot when aiming
old_shoot_listener = """window.addEventListener('mousedown', function(e) {
          if (e.button === 0 && reloadTimer <= 0) {
            triggerShoot();
          }
        });"""

new_shoot_listener = """window.addEventListener('mousedown', function(e) {
          if (e.button === 0) {
            const cam = window._app && window._app.world ? window._app.world.camera : null;
            const isAimActive = cam && (cam.isAiming || cam.isAimFixed);
            if (!isAimActive) {
              const alertEl = document.querySelector('#aim-required-alert');
              if (alertEl) {
                alertEl.style.opacity = '1';
                clearTimeout(alertEl._timer);
                alertEl._timer = setTimeout(() => { alertEl.style.opacity = '0'; }, 1100);
              }
              return;
            }
            if (reloadTimer <= 0) {
              triggerShoot();
            }
          }
        });"""

if old_shoot_listener in html:
    html = html.replace(old_shoot_listener, new_shoot_listener)
    print("4b. index.html: Updated mousedown shooting condition.")

# Update controls hint bar
old_controls_bar = """<div class="tank-controls-bar">
        <span>WASD</span> DRIVE (GTA CAR) &middot; <span>SCROLL PRESS / R-CLICK</span> FPS ZOOM FREE AIM &middot; <span>MOUSE</span> LOOK / AIM &middot; <span>Q / E</span> ROTATE CANNON &middot; <span>L-CLICK / SPACE</span> FIRE &middot; <span>SHIFT</span> BOOST
      </div>"""

new_controls_bar = """<div class="tank-controls-bar">
        <span>WASD</span> DRIVE (GTA CAR) &middot; <span>HOLD R-CLICK</span> AIM & ZOOM &middot; <span>PRESS SCROLL</span> LOCK AIM &middot; <span>SCROLL</span> ZOOM IN/OUT &middot; <span>L-CLICK</span> FIRE
      </div>"""

if old_controls_bar in html:
    html = html.replace(old_controls_bar, new_controls_bar)
    print("4c. index.html: Updated controls hint bar.")

# Update crosshair CSS so it is elevated, sleek, and high-visibility when aiming
old_crosshair_css_start = "/* World War Tanks Single Precision Tactical Crosshair */"
old_crosshair_css_end = "/* Top Header Banner */"

start_c = html.find(old_crosshair_css_start)
end_c = html.find(old_crosshair_css_end)

if start_c != -1 and end_c != -1:
    new_crosshair_css = """/* World War Tanks Precision Combat Crosshair */
      #aim-circle {
        position: fixed !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        width: 32px !important;
        height: 32px !important;
        pointer-events: none !important;
        display: block !important;
        z-index: 99999 !important;
        opacity: 0.38;
        transition: opacity 0.2s ease, width 0.2s ease, height 0.2s ease;
      }
      body.aim-mode-active #aim-circle {
        opacity: 1.0 !important;
        width: 36px !important;
        height: 36px !important;
      }
      #aim-circle .aim-visual {
        position: relative !important;
        width: 100% !important;
        height: 100% !important;
      }
      #aim-circle .aim-dot {
        position: absolute !important;
        top: 50% !important;
        left: 50% !important;
        width: 4px !important;
        height: 4px !important;
        background: #00ffaa !important;
        border-radius: 50% !important;
        transform: translate(-50%, -50%) !important;
        box-shadow: 0 0 6px rgba(0, 255, 170, 0.95) !important;
        border: none !important;
      }
      body.aim-mode-active #aim-circle .aim-dot {
        background: #ff3344 !important;
        box-shadow: 0 0 8px rgba(255, 51, 68, 0.95) !important;
      }
      #aim-circle .aim-part {
        position: absolute !important;
        background: rgba(255, 255, 255, 0.92) !important;
        box-shadow: 0 0 3px rgba(0, 0, 0, 0.9) !important;
        background-image: none !important;
        border-radius: 1px !important;
      }
      body.aim-mode-active #aim-circle .aim-part {
        background: rgba(0, 255, 170, 0.95) !important;
        box-shadow: 0 0 5px rgba(0, 255, 170, 0.8) !important;
      }
      #aim-circle .aim-top {
        top: 0px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 2px !important;
        height: 8px !important;
      }
      #aim-circle .aim-bottom {
        bottom: 0px !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        width: 2px !important;
        height: 8px !important;
      }
      #aim-circle .aim-left {
        left: 0px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        width: 8px !important;
        height: 2px !important;
      }
      #aim-circle .aim-right {
        right: 0px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        width: 8px !important;
        height: 2px !important;
      }
      #aim-circle .aim-kill,
      #aim-circle .aim-kill-part,
      #aim-circle .aim-grab-mode-wrapper,
      .tank-crosshair {
        display: none !important;
      }

      """
    html = html[:start_c] + new_crosshair_css + html[end_c:]
    print("4d. index.html: Updated precision crosshair CSS.")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

print("=== ALL COMBAT AIM & ZOOM ENHANCEMENTS APPLIED ===")
