import re, os, shutil

BASE_DIR = r"C:\Users\Vrund Patel\Desktop\clone-game"

# -------------------------------------------------------------
# 1. PATCH B1Nq4Kq6.js
# -------------------------------------------------------------
path_b1 = os.path.join(BASE_DIR, "assets", "B1Nq4Kq6.js")
with open(path_b1, "r", encoding="utf-8") as f:
    b1 = f.read()

print("Original B1Nq4Kq6.js length:", len(b1))

# A. Fix Mn stroke definitions: disable vertex displacement for scenery props
old_mn_area = "area:{name:`AreaStrokeMaterial`,side:1,transparent:!0,alphaTest:null,positionNode:On,colorNode:En}"
new_mn_area = "area:{name:`AreaStrokeMaterial`,side:1,transparent:!0,alphaTest:null,positionNode:()=>O,colorNode:En}"

old_mn_inst = "instanced_area:{name:`InstancedAreaStrokeMaterial`,side:1,transparent:!0,alphaTest:null,positionNode:kn,colorNode:En}"
new_mn_inst = "instanced_area:{name:`InstancedAreaStrokeMaterial`,side:1,transparent:!0,alphaTest:null,positionNode:()=>O,colorNode:En}"

old_mn_fence = "instanced_concrete_fence:{name:`InstancedConcreteFenceStrokeMaterial`,side:1,transparent:!0,alphaTest:.001,positionNode:kn,colorNode:En"
new_mn_fence = "instanced_concrete_fence:{name:`InstancedConcreteFenceStrokeMaterial`,side:1,transparent:!0,alphaTest:.001,positionNode:()=>O,colorNode:En"

if old_mn_area in b1:
    b1 = b1.replace(old_mn_area, new_mn_area)
    print("1a. B1Nq4Kq6: Mn.area positionNode set to zero displacement.")
else:
    print("WARNING: old_mn_area not found")

if old_mn_inst in b1:
    b1 = b1.replace(old_mn_inst, new_mn_inst)
    print("1b. B1Nq4Kq6: Mn.instanced_area positionNode set to zero displacement.")
else:
    print("WARNING: old_mn_inst not found")

if old_mn_fence in b1:
    b1 = b1.replace(old_mn_fence, new_mn_fence)
    print("1c. B1Nq4Kq6: Mn.instanced_concrete_fence positionNode set to zero displacement.")
else:
    print("WARNING: old_mn_fence not found")

# B. StrokeMaterial constructor: hide scenery stroke materials completely
old_ctor_start = "constructor(t,n={}){super();let r=Mn[t];this.visibleState=!0,e.instances.add(new WeakRef(this)),this.map=null,this.name=n.name||r.name;"
new_ctor_start = "constructor(t,n={}){super();let r=Mn[t];let isScenery=(t==='area'||t==='instanced_area'||t==='instanced_concrete_fence');this.visibleState=!isScenery;this.visible=!isScenery;e.instances.add(new WeakRef(this)),this.map=null,this.name=n.name||r.name;"

if old_ctor_start in b1:
    b1 = b1.replace(old_ctor_start, new_ctor_start)
    print("1d. B1Nq4Kq6: StrokeMaterial constructor hides scenery strokes.")
else:
    print("WARNING: old_ctor_start not found")

# C. attachModelStroke: disable scenery stroke attachment
old_attach = "attachModelStroke(e){if(!e)return;this.initStrokeSystem();"
new_attach = "attachModelStroke(e){return;if(!e)return;this.initStrokeSystem();"
if old_attach in b1:
    b1 = b1.replace(old_attach, new_attach)
    print("1e. B1Nq4Kq6: attachModelStroke disabled for scenery models.")
else:
    print("WARNING: old_attach not found")

# D. Instanced stroke mesh creation: force visible = false
old_inst_stroke = "if(t&&o){let e=new nt(t,o,n);e.name=`${r}_Stroke`,e.castShadow=!1,e.receiveShadow=!1"
new_inst_stroke = "if(t&&o){let e=new nt(t,o,n);e.name=`${r}_Stroke`,e.visible=!1,e.castShadow=!1,e.receiveShadow=!1"
if old_inst_stroke in b1:
    b1 = b1.replace(old_inst_stroke, new_inst_stroke)
    print("1f. B1Nq4Kq6: instanced stroke mesh visible forced false.")
else:
    print("WARNING: old_inst_stroke not found")

# E. Q/E Turret manual rotation offset applied in getTurretTargetQuat
old_quat = "getTurretTargetQuat(e){(this.turret.parent||this.robotInstance.model.object3D).getWorldQuaternion(this.rootWorldQuat),this.rootInverse.copy(this.rootWorldQuat).invert(),this.localAimDir.copy(e).applyQuaternion(this.rootInverse);let t=Math.atan2(-this.localAimDir.z,this.localAimDir.x);return this.targetTurretQuat.setFromAxisAngle(this.yAxis,t),this.targetTurretQuat}"
new_quat = "getTurretTargetQuat(e){(this.turret.parent||this.robotInstance.model.object3D).getWorldQuaternion(this.rootWorldQuat),this.rootInverse.copy(this.rootWorldQuat).invert(),this.localAimDir.copy(e).applyQuaternion(this.rootInverse);let t=Math.atan2(-this.localAimDir.z,this.localAimDir.x);if(this.turretManualOffset){t+=this.turretManualOffset}return this.targetTurretQuat.setFromAxisAngle(this.yAxis,t),this.targetTurretQuat}"

if old_quat in b1:
    b1 = b1.replace(old_quat, new_quat)
    print("1g. B1Nq4Kq6: getTurretTargetQuat applies turretManualOffset (Q/E).")
else:
    print("WARNING: old_quat not found")

# F. Smooth turret damping and aim-mode snap back
old_damp_aim = "let cam = this.camera;\n  let isAimActive = cam && (cam.isAiming || cam.isAimFixed);\n\n  // Manual turret rotation override with Q and E buttons:"
new_damp_aim = "let cam = this.camera;\n  let isAimActive = cam && (cam.isAiming || cam.isAimFixed);\n  if(isAimActive && this.turretManualOffset){ this.turretManualOffset *= Math.exp(-6.0 * t); }\n\n  // Manual turret rotation override with Q and E buttons:"

if old_damp_aim in b1:
    b1 = b1.replace(old_damp_aim, new_damp_aim)
    print("1h. B1Nq4Kq6: turretManualOffset smooth centering during Aim Mode.")
else:
    print("WARNING: old_damp_aim not found")

# G. Realistic tank steering speed (1.85 rad/s instead of hyper 3.12 rad/s)
old_rot_speed = "this.speed=8,this.boostSpeed=1.9,this.rotationSpeed=3.12,this.boostRotationMultiplier=1.2"
new_rot_speed = "this.speed=8,this.boostSpeed=1.9,this.rotationSpeed=1.85,this.boostRotationMultiplier=1.2"
if old_rot_speed in b1:
    b1 = b1.replace(old_rot_speed, new_rot_speed)
    print("1i. B1Nq4Kq6: rotationSpeed set to smooth 1.85 rad/s for GTA-style driving.")
else:
    print("WARNING: old_rot_speed not found")

with open(path_b1, "w", encoding="utf-8") as f:
    f.write(b1)
print("B1Nq4Kq6.js saved successfully.")

# -------------------------------------------------------------
# 2. PATCH CQl67Veh.js (Camera Framing & No Sky Inversion)
# -------------------------------------------------------------
path_cq = os.path.join(BASE_DIR, "assets", "CQl67Veh.js")
with open(path_cq, "r", encoding="utf-8") as f:
    cq = f.read()

print("Original CQl67Veh.js length:", len(cq))

# Replace the camera calculation block
idx_start = cq.find("let isAim=this.isAiming||this.isAimFixed;")
idx_end = cq.find("this.instance.position.copy(this.viewAPosition);")

if idx_start != -1 and idx_end != -1:
    old_cam_block = cq[idx_start:idx_end]
    new_cam_block = """let isAim = this.isAiming || this.isAimFixed;
let camDist = this._orbitDistance || (isAim ? 4.8 : 7.0);
let pivotY = 0.5;
let camH = isAim ? 1.4 : 1.9;
let focusDist = 45.0;

let cosP = Math.cos(this._orbitPitch);
let sinP = Math.sin(this._orbitPitch);
let sinY = Math.sin(this._orbitYaw);
let cosY = Math.cos(this._orbitYaw);

let rx = camDist * cosP * sinY;
let ry = camDist * sinP + camH;
let rz = camDist * cosP * cosY;

this.angle.value.set(rx, ry, rz);
this.forwardVec.set(-sinY * cosP, -sinP, -cosY * cosP).normalize();

this.viewAPosition.copy(this.targetEased).add(this.mousePanOffset).add(this.panViewOffset).add(this.recoilOffset);
this.viewAPosition.x += rx;
this.viewAPosition.y += pivotY + ry;
this.viewAPosition.z += rz;

this.viewAFocus.copy(this.viewAPosition).addScaledVector(this.forwardVec, focusDist);

// Disable all cinematic sequences
if(this.introCamera){ this.introCamera.active = false; this.introCamera.zoomScale = 1.0; }
if(this.revealCamera) this.revealCamera.active = false;
if(this.powerCoreSequence) this.powerCoreSequence.active = false;
if(this.pipeGameSequence) this.pipeGameSequence.active = false;
if(this.tourSequence){ this.tourSequence.active = false; this.tourSequence.restoring = false; }
if(this.previewSequence){ this.previewSequence.active = false; this.previewSequence.restoring = false; }
if(this.aboutProjectSequence){ this.aboutProjectSequence.active = false; this.aboutProjectSequence.reversing = false; }
if(this.cinematic) this.cinematic.weight = 0;
"""
    cq = cq[:idx_start] + new_cam_block + cq[idx_end:]
    print("2a. CQl67Veh: camera positioning and focus replaced with pure forward vector & disabled cinematic sequences.")
else:
    print("WARNING: camera block in CQl67Veh not found")

# Fix pitch clamps and sensitivity in onMove
old_pitch_clamp = "this._targetOrbitPitch = Math.max(-0.15, Math.min(0.40, this._targetOrbitPitch));"
new_pitch_clamp = "this._targetOrbitPitch = Math.max(-0.05, Math.min(0.48, this._targetOrbitPitch));"
if old_pitch_clamp in cq:
    cq = cq.replace(old_pitch_clamp, new_pitch_clamp)
    print("2b. CQl67Veh: pitch clamp set to [-0.05, 0.48] (no sky inversion).")
else:
    print("WARNING: old_pitch_clamp not found")

# Set default orbit pitch to +0.16 (natural third-person view looking down over tank)
old_pitch_init = "this._orbitPitch = 0;"
new_pitch_init = "this._orbitPitch = 0.16; this._targetOrbitPitch = 0.16;"
if old_pitch_init in cq:
    cq = cq.replace(old_pitch_init, new_pitch_init)
    print("2c. CQl67Veh: initial pitch set to 0.16.")

# Fix target dist update in CQl67Veh
old_dist_update = "let targetDist = (this.isAiming || this.isAimFixed) ? 5.8 : 7.5;\n    this._targetOrbitDistance += (targetDist - this._targetOrbitDistance) * Math.min(1.0, 10 * e);"
new_dist_update = "let targetDist = (this.isAiming || this.isAimFixed) ? 4.8 : 7.0;\n    this._targetOrbitDistance += (targetDist - this._targetOrbitDistance) * Math.min(1.0, 10 * e);"
if old_dist_update in cq:
    cq = cq.replace(old_dist_update, new_dist_update)
    print("2d. CQl67Veh: targetDist updated to 4.8 (aim) / 7.0 (normal).")

with open(path_cq, "w", encoding="utf-8") as f:
    f.write(cq)
print("CQl67Veh.js saved successfully.")

# -------------------------------------------------------------
# 3. PATCH DPqB0RfP.js (Lock Single Crosshair to Center Screen)
# -------------------------------------------------------------
path_dp = os.path.join(BASE_DIR, "assets", "DPqB0RfP.js")
with open(path_dp, "r", encoding="utf-8") as f:
    dp = f.read()

# Never move aim-circle to click location
old_click_move = "Number.isFinite(e)&&Number.isFinite(t)&&(this.root.style.left=`${e}px`,this.root.style.top=`${t}px`),this.root.style.display=`block`"
new_click_move = 'this.root.style.left="50%",this.root.style.top="50%",this.root.style.transform="translate(-50%,-50%)",this.root.style.display="block"'

if old_click_move in dp:
    dp = dp.replace(old_click_move, new_click_move)
    print("3a. DPqB0RfP: triggerClickAnimation locked to center (50% 50%).")
else:
    print("WARNING: old_click_move not found in DPqB0RfP")

with open(path_dp, "w", encoding="utf-8") as f:
    f.write(dp)
print("DPqB0RfP.js saved successfully.")

# -------------------------------------------------------------
# 4. PATCH index.html (Single Sleek Precision Reticle & Controls)
# -------------------------------------------------------------
path_html = os.path.join(BASE_DIR, "index.html")
with open(path_html, "r", encoding="utf-8") as f:
    html = f.read()

# Update controls footer text to reflect Q and E buttons
old_controls_pattern = r'<div class="tank-controls-bar">[\s\S]*?</div>'
new_controls_text = '<div class="tank-controls-bar"><span>WASD</span> DRIVE (GTA CAR) &middot; <span>HOLD R-CLICK</span> AIM &amp; ZOOM &middot; <span>PRESS SCROLL</span> LOCK AIM &middot; <span>Q / E</span> TURRET SWIVEL &middot; <span>L-CLICK</span> FIRE &middot; <span>SCROLL</span> ZOOM</div>'

if re.search(old_controls_pattern, html):
    html = re.sub(old_controls_pattern, new_controls_text, html, count=1)
    print("4a. index.html: updated bottom controls bar with Q/E swivel and GTA drive.")

# Ensure .tank-crosshair is 100% hidden
if ".tank-crosshair { display: none !important; }" not in html:
    html = html.replace("</style>", "  .tank-crosshair { display: none !important; pointer-events: none !important; }\n    </style>")
    print("4b. index.html: ensured tank-crosshair is display: none !important.")

with open(path_html, "w", encoding="utf-8") as f:
    f.write(html)
print("index.html saved successfully.")
