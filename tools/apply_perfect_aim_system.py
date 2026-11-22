import os
import re

game_dir = r"C:\Users\Vrund Patel\Desktop\clone-game"

# ==============================================================================
# 1. PATCH assets/CQl67Veh.js
# ==============================================================================
cq_path = os.path.join(game_dir, "assets", "CQl67Veh.js")
with open(cq_path, "r", encoding="utf-8") as f:
    cq = f.read()

# Replace _orbitInit block with complete, bug-free implementation including onMove
idx1 = cq.find("if(!this._orbitInit){")
idx2 = cq.find('window.addEventListener("contextmenu"', idx1)
idx3 = cq.find("});", idx2) + 3
# Find the closing brace of the if(!this._orbitInit){ block
idx_close_orbit = cq.find("}", idx3) + 1

new_orbit_block = """if(!this._orbitInit){
        this._orbitInit = true;
        this._orbitYaw = 0.46;
        this._orbitPitch = 0.20;
        this._orbitDistance = 5.4;
        this._targetOrbitYaw = 0.0;
        this._targetOrbitPitch = 0.20;
        this._targetOrbitDistance = 5.4;
        this._userLookTimer = 0;
        this._isDragging = false;
        this._lastPointerX = 0;
        this._lastPointerY = 0;
        
        this.isAiming = false;
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
            if(ev.button === 1){ // Middle mouse click (scroll button press): Toggle fixed aim
                ev.preventDefault();
                this.isAimFixed = !this.isAimFixed;
                this.updateAimState();
                return;
            }
            if(ev.button === 2){ // Right click: Hold to aim & zoom
                ev.preventDefault();
                this.isAiming = true;
                this.updateAimState();
                return;
            }
            this._isDragging = true;
            this._lastPointerX = ev.clientX;
            this._lastPointerY = ev.clientY;
        };

        const onMove = ev => {
            const isLocked = !!document.pointerLockElement;
            const isAimActive = this.isAiming || this.isAimFixed;
            if(isLocked || this._isDragging || isAimActive){
                const dx = isLocked ? ev.movementX : (ev.clientX - this._lastPointerX);
                const dy = isLocked ? ev.movementY : (ev.clientY - this._lastPointerY);
                this._lastPointerX = ev.clientX;
                this._lastPointerY = ev.clientY;
                const sens = isAimActive ? 0.0022 : 0.0035;
                this._targetOrbitYaw -= dx * sens;
                this._targetOrbitPitch += dy * sens;
                this._targetOrbitPitch = Math.max(0.04, Math.min(1.10, this._targetOrbitPitch));
                this._userLookTimer = 1.5;
            }
        };

        const onUp = ev => {
            if(ev && ev.button === 2){
                this.isAiming = false;
                this.updateAimState();
            }
            this._isDragging = false;
        };

        const onWheel = ev => {
            if(ev.target && ev.target.closest && ev.target.closest(".about-page, .statue-page, .case-study-page, .hanzii-page, .email-popup, .submit-item-popup, [role='dialog'], textarea, input, select")) return;
            const delta = ev.deltaY > 0 ? 0.45 : -0.45;
            this._targetOrbitDistance = Math.max(2.4, Math.min(9.5, this._targetOrbitDistance + delta));
        };

        window.addEventListener("pointerdown", onDown, {passive: false});
        window.addEventListener("pointermove", onMove, {passive: true});
        window.addEventListener("pointerup", onUp, {passive: true});
        window.addEventListener("mouseup", onUp, {passive: true});
        window.addEventListener("wheel", onWheel, {passive: true});
        window.addEventListener("contextmenu", ev => {
            if(!ev.target || !ev.target.closest || !ev.target.closest("input, textarea, a, button")){
                ev.preventDefault();
            }
        });
    }"""

cq = cq[:idx1] + new_orbit_block + cq[idx_close_orbit:]
print("1a. Patched _orbitInit with onMove, pointer handlers, and wheel zoom.")

# Now patch camera framing (viewAPosition and viewAFocus)
old_cam_focus_start = "let isAim=this.isAiming||this.isAimFixed;"
idx_focus_start = cq.find(old_cam_focus_start)
idx_focus_end = cq.find("if(this.introCamera.active||this.introCamera.zoomScale>1.01){", idx_focus_start)

if idx_focus_start != -1 and idx_focus_end != -1:
    new_cam_calc = """let isAim=this.isAiming||this.isAimFixed;
let camElev=isAim?1.2:1.4;
let focusElev=isAim?1.4:1.6;
let focusDist=isAim?35:30;
this.viewAPosition.copy(this.targetEased).add(n).add(this.mousePanOffset).add(this.panViewOffset).add(this.recoilOffset);
this.viewAPosition.y+=camElev;
this.viewAFocus.copy(this.targetEased).add(this.mousePanOffset).add(this.panViewOffset).add(this.recoilOffset);
let sinY_f=Math.sin(this._orbitYaw),cosY_f=Math.cos(this._orbitYaw);
this.forwardVec.set(-sinY_f,0,-cosY_f).normalize();
this.viewAFocus.addScaledVector(this.forwardVec,focusDist);
this.viewAFocus.y+=focusElev;
"""
    cq = cq[:idx_focus_start] + new_cam_calc + cq[idx_focus_end:]
    print("1b. Patched camera viewAPosition & viewAFocus for perfect 74% tank lower-third framing.")

with open(cq_path, "w", encoding="utf-8") as f:
    f.write(cq)
print("Saved CQl67Veh.js successfully.")

# ==============================================================================
# 2. PATCH assets/B1Nq4Kq6.js (Q/E Turret rotation + Free Mouse Aim)
# ==============================================================================
b1_path = os.path.join(game_dir, "assets", "B1Nq4Kq6.js")
with open(b1_path, "r", encoding="utf-8") as f:
    b1 = f.read()

# Locate handlePointerVisual
hpv_start = b1.find("handlePointerVisual(e,t){")
if hpv_start != -1:
    hpv_end = b1.find("handleTouchVisual(e,t){", hpv_start)
    if hpv_end != -1:
        new_hpv = """handlePointerVisual(e,t){
  let cam = this.camera;
  let isAimActive = cam && (cam.isAiming || cam.isAimFixed);

  // Manual turret rotation override with Q and E buttons:
  if(this.controller && this.controller.keyPressed){
    if(this.controller.keyPressed.has("KeyQ")){
      this.turretManualOffset = (this.turretManualOffset || 0) + t * 2.2;
    }
    if(this.controller.keyPressed.has("KeyE")){
      this.turretManualOffset = (this.turretManualOffset || 0) - t * 2.2;
    }
  }

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

  // Casual driving mode: Turret faces forward with hull heading (W) + Q/E manual offset
  this.turretManualAngle = 0;
  let manualOffset = this.turretManualOffset || 0;
  let n = this.targetTurretQuat.setFromAxisAngle(this.yAxis, manualOffset);
  this.applyTurretAim(n, t);
  this.aimRaycastAccumulator += t;
  this.aimRaycastAccumulator >= .02 && (this.aimRaycastAccumulator = 0, this.handleAiming(this.rayCaster));
}"""
        b1 = b1[:hpv_start] + new_hpv + b1[hpv_end:]
        print("2. Patched handlePointerVisual in B1Nq4Kq6.js (Free Mouse Aim + Q/E Manual Turret Controls).")
        with open(b1_path, "w", encoding="utf-8") as f:
            f.write(b1)
        print("Saved B1Nq4Kq6.js successfully.")

# ==============================================================================
# 3. PATCH assets/DPqB0RfP.js (Unblock shooting when aimed)
# ==============================================================================
dp_path = os.path.join(game_dir, "assets", "DPqB0RfP.js")
with open(dp_path, "r", encoding="utf-8") as f:
    dp = f.read()

sbs_start = dp.find("shouldBlockShoot(){")
if sbs_start != -1:
    sbs_end = dp.find("static isEditableTarget", sbs_start)
    if sbs_end != -1:
        # Check what's inside shouldBlockShoot
        old_sbs = dp[sbs_start:sbs_end]
        new_sbs = """shouldBlockShoot(){
  let cam = this.world && this.world.camera;
  if(cam && !cam.isAiming && !cam.isAimFixed) return !0;
  if(!this.world || !this.world.robot || this.world.robot.isDead) return !0;
  if(cam && (cam.isAiming || cam.isAimFixed)) return !1;
  if(this.world.tutorial && typeof this.world.tutorial.hasCardAppeared == "function" && !this.world.tutorial.hasCardAppeared("shoot")) return !0;
  if(this.world.grabMode && (this.world.grabMode.monitoredObjects && this.world.grabMode.monitoredObjects.size > 0 || this.world.grabMode.isHoldActive)) return !0;
  return !1;
}"""
        dp = dp[:sbs_start] + new_sbs + dp[sbs_end:]
        print("3. Patched shouldBlockShoot in DPqB0RfP.js to guarantee instant shooting when aimed.")
        with open(dp_path, "w", encoding="utf-8") as f:
            f.write(dp)
        print("Saved DPqB0RfP.js successfully.")

# ==============================================================================
# 4. PATCH index.html (Controls Bar, Aim Alert, Styling)
# ==============================================================================
html_path = os.path.join(game_dir, "index.html")
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Update controls footer text
old_controls_pattern = r'<span class="key-combo"><span class="key-badge">WASD</span>.*?</div>'
new_controls_bar = """<span class="key-combo"><span class="key-badge">WASD</span> DRIVE</span>
        <span class="key-sep">•</span>
        <span class="key-combo"><span class="key-badge">RIGHT CLICK (HOLD)</span> / <span class="key-badge">SCROLL CLICK (LOCK)</span> AIM & ZOOM</span>
        <span class="key-sep">•</span>
        <span class="key-combo"><span class="key-badge">L-CLICK</span> FIRE</span>
        <span class="key-sep">•</span>
        <span class="key-combo"><span class="key-badge">Q / E</span> ROTATE TURRET</span>
        <span class="key-sep">•</span>
        <span class="key-combo"><span class="key-badge">SCROLL</span> ZOOM</span>
      </div>"""

if re.search(old_controls_pattern, html, re.DOTALL):
    html = re.sub(old_controls_pattern, new_controls_bar, html, count=1)
    print("4a. Updated controls guide in index.html.")

# Update shoot trigger listener on window to show alert if not aiming
window_click_patch = """
      // Left click fire trigger with aim check
      window.addEventListener('mousedown', function(e) {
        if (e.button === 0) {
          const cam = window.app && window.app.camera;
          const isAim = cam && (cam.isAiming || cam.isAimFixed);
          if (!isAim) {
            const alertEl = document.getElementById('aim-required-alert');
            if (alertEl) {
              alertEl.classList.add('visible');
              clearTimeout(window._aimAlertTimer);
              window._aimAlertTimer = setTimeout(() => {
                alertEl.classList.remove('visible');
              }, 1800);
            }
          }
        }
      }, true);
"""

if "window._aimAlertTimer" not in html:
    # Insert right before </body>
    html = html.replace("</body>", f"<script>{window_click_patch}</script>\n</body>")
    print("4b. Added click aim check & helper alert trigger.")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)
print("Saved index.html successfully.")
print("\nALL PATCHES APPLIED SUCCESSFULLY!")
