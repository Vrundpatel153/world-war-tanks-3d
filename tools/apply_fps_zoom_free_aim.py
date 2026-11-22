import os

game_dir = r"C:\Users\Vrund Patel\Desktop\clone-game"

# ==============================================================================
# 1. Patch CQl67Veh.js: Add FPS Turret Zoom on Scroll Click (Button 1 / MMB)
# ==============================================================================
cq_path = os.path.join(game_dir, "assets", "CQl67Veh.js")
with open(cq_path, "r", encoding="utf-8") as f:
    cq = f.read()

# A. Add toggleFpsZoom & handle scroll wheel click (ev.button === 1) in onDown
old_on_down = """const onDown = ev => {
            if(ev.target && ev.target.closest && ev.target.closest(".about-page, .statue-page, .case-study-page, .hanzii-page, .email-popup, .submit-item-popup, [role='dialog'], textarea, input, select, button")) return;
            this._isDragging = true;
            this._lastPointerX = ev.clientX;
            this._lastPointerY = ev.clientY;
        };"""

new_on_down = """this.toggleFpsZoom = () => {
            this.isFpsZoom = !this.isFpsZoom;
            if(this.isFpsZoom){
                document.body.classList.add("fps-mode-active");
                const b = document.querySelector("#fps-mode-badge");
                if(b) b.style.display = "block";
            } else {
                document.body.classList.remove("fps-mode-active");
                const b = document.querySelector("#fps-mode-badge");
                if(b) b.style.display = "none";
            }
        };
        window.toggleFpsTurretZoom = this.toggleFpsZoom;
        window.addEventListener("auxclick", ev => {
            if(ev.button === 1){
                ev.preventDefault();
                this.toggleFpsZoom();
            }
        });

        const onDown = ev => {
            if(ev.target && ev.target.closest && ev.target.closest(".about-page, .statue-page, .case-study-page, .hanzii-page, .email-popup, .submit-item-popup, [role='dialog'], textarea, input, select, button")) return;
            if(ev.button === 1 || ev.button === 2){
                ev.preventDefault();
                this.toggleFpsZoom();
                return;
            }
            this._isDragging = true;
            this._lastPointerX = ev.clientX;
            this._lastPointerY = ev.clientY;
        };"""

if old_on_down in cq:
    cq = cq.replace(old_on_down, new_on_down)
    print("1a. CQl67Veh.js: Added toggleFpsZoom and scroll wheel click handler.")
else:
    print("Warning: old_on_down not found in CQl67Veh.js")

# B. In frame camera position update: support FPS view
old_cam_pos = "this.instance.position.copy(this.viewAPosition),this.instance.lookAt(this.viewAFocus),this.instance.updateMatrixWorld(!0),this.updateOptimalArea()"

new_cam_pos = """if(this.isFpsZoom && this.robot && this.robot.model && (this.robot.model.turret || this.robot.model.default)){
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

if old_cam_pos in cq:
    cq = cq.replace(old_cam_pos, new_cam_pos)
    print("1b. CQl67Veh.js: Added outward FPS turret view positioning.")
else:
    print("Warning: old_cam_pos not found in CQl67Veh.js")

with open(cq_path, "w", encoding="utf-8") as f:
    f.write(cq)

# ==============================================================================
# 2. Patch B1Nq4Kq6.js: Free Aim Turret tracking in FPS mode
# ==============================================================================
b1_path = os.path.join(game_dir, "assets", "B1Nq4Kq6.js")
with open(b1_path, "r", encoding="utf-8") as f:
    b1 = f.read()

old_pointer_vis = "handlePointerVisual(e,t){this.turretManualAngle=this.turretManualAngle||0;let r=2.6;if(this.controller&&this.controller.keyPressed){(this.controller.keyPressed.has(`KeyQ`)||this.controller.keyPressed.has(`ArrowLeft`))&&(this.turretManualAngle+=r*t);(this.controller.keyPressed.has(`KeyE`)||this.controller.keyPressed.has(`ArrowRight`))&&(this.turretManualAngle-=r*t);(this.controller.keyPressed.has(`KeyC`)||this.controller.keyPressed.has(`KeyX`))&&(this.turretManualAngle=0)}let n=this.targetTurretQuat.setFromAxisAngle(this.yAxis,this.turretManualAngle);this.applyTurretAim(n,t),this.aimRaycastAccumulator+=t,this.aimRaycastAccumulator>=.02&&(this.aimRaycastAccumulator=0,this.handleAiming(this.rayCaster))}"

new_pointer_vis = """handlePointerVisual(e,t){
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

if old_pointer_vis in b1:
    b1 = b1.replace(old_pointer_vis, new_pointer_vis)
    print("2. B1Nq4Kq6.js: Added Free Aim turret tracking for FPS zoom mode.")
else:
    print("Warning: old_pointer_vis not found in B1Nq4Kq6.js")

with open(b1_path, "w", encoding="utf-8") as f:
    f.write(b1)

# ==============================================================================
# 3. Patch index.html: Add FPS Mode badge, sniper crosshair styling & controls hint
# ==============================================================================
index_path = os.path.join(game_dir, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Add sniper CSS when body has .fps-mode-active
sniper_css = """
      /* FPS Turret Sniper Scope Styling */
      body.fps-mode-active #aim-circle {
        width: 48px !important;
        height: 48px !important;
        transition: width 0.15s ease, height 0.15s ease;
      }
      body.fps-mode-active #aim-circle .aim-dot {
        background: #ff3344 !important;
        box-shadow: 0 0 8px rgba(255, 51, 68, 0.95) !important;
        width: 5px !important;
        height: 5px !important;
      }
      body.fps-mode-active #aim-circle .aim-part {
        background: rgba(0, 255, 170, 0.95) !important;
        box-shadow: 0 0 5px rgba(0, 255, 170, 0.8) !important;
      }
      body.fps-mode-active #aim-circle .aim-top { height: 14px !important; }
      body.fps-mode-active #aim-circle .aim-bottom { height: 14px !important; }
      body.fps-mode-active #aim-circle .aim-left { width: 14px !important; }
      body.fps-mode-active #aim-circle .aim-right { width: 14px !important; }
"""

if "/* FPS Turret Sniper Scope Styling */" not in html:
    css_insert_point = "</style>"
    html = html.replace(css_insert_point, sniper_css + "\n    " + css_insert_point, 1)
    print("3a. index.html: Added FPS mode sniper scope crosshair CSS.")

# Add FPS mode badge into #tank-hud
badge_html = """      <!-- FPS Sniper Mode Indicator Badge -->
      <div id="fps-mode-badge" style="display: none; position: absolute; top: 64px; left: 50%; transform: translateX(-50%); background: rgba(10, 20, 28, 0.85); border: 1.5px solid #00ffaa; color: #00ffaa; font-size: 11px; font-weight: 800; padding: 4px 16px; border-radius: 4px; letter-spacing: 0.12em; box-shadow: 0 0 16px rgba(0, 255, 170, 0.4); backdrop-filter: blur(8px); pointer-events: none;">
        ● FPS TURRET GUNNER &middot; FREE AIM ACTIVE
      </div>
"""

if 'id="fps-mode-badge"' not in html:
    hud_point = '<div id="tank-hud">'
    html = html.replace(hud_point, hud_point + "\n" + badge_html, 1)
    print("3b. index.html: Added FPS mode badge.")

# Update controls text
old_controls_bar = """<div class="tank-controls-bar">
        <span>WASD</span> TANK DRIVE &middot; <span>MOUSE</span> LOOK AROUND &middot; <span>Q / E</span> ROTATE CANNON &middot; <span>C</span> RE-CENTER &middot; <span>L-CLICK / SPACE</span> FIRE &middot; <span>SHIFT</span> BOOST &middot; <span>SCROLL</span> ZOOM
      </div>"""

new_controls_bar = """<div class="tank-controls-bar">
        <span>WASD</span> DRIVE (GTA CAR) &middot; <span>SCROLL PRESS / R-CLICK</span> FPS ZOOM FREE AIM &middot; <span>MOUSE</span> LOOK / AIM &middot; <span>Q / E</span> ROTATE CANNON &middot; <span>L-CLICK / SPACE</span> FIRE &middot; <span>SHIFT</span> BOOST
      </div>"""

if old_controls_bar in html:
    html = html.replace(old_controls_bar, new_controls_bar)
    print("3c. index.html: Updated controls bar hint.")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

print("=== ALL FPS TURRET ZOOM & FREE AIM MODIFICATIONS APPLIED ===")
