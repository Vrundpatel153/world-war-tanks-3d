import re

path_cq = "C:/Users/Vrund Patel/Desktop/clone-game/assets/CQl67Veh.js"
with open(path_cq, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update defaults in updatePlayerStartAngle
old_init = """        this._orbitInit = true;
        this._orbitYaw = 0.0;
        this._orbitPitch = 0.22;
        this._orbitDistance = 6.6;
        this._targetOrbitYaw = 0.0;
        this._targetOrbitPitch = 0.22;
        this._targetOrbitDistance = 6.6;"""

new_init = """        this._orbitInit = true;
        this._orbitYaw = 0.0;
        this._orbitPitch = 0.18;
        this._orbitDistance = 7.5;
        this._targetOrbitYaw = 0.0;
        this._targetOrbitPitch = 0.18;
        this._targetOrbitDistance = 7.5;"""

if old_init in text:
    text = text.replace(old_init, new_init)
    print("Updated _orbitInit defaults")
else:
    print("WARNING: old_init not found")

# 2. Update pitch clamping in onMove
old_onmove_clamp = "this._targetOrbitPitch = Math.max(0.04, Math.min(0.65, this._targetOrbitPitch));"
new_onmove_clamp = "this._targetOrbitPitch = Math.max(-0.15, Math.min(0.40, this._targetOrbitPitch));"
if old_onmove_clamp in text:
    text = text.replace(old_onmove_clamp, new_onmove_clamp)
    print("Updated onMove pitch clamping")
else:
    print("WARNING: old_onmove_clamp not found")

# 3. Update viewAPosition and viewAFocus calculation
old_calc = """let isAim=this.isAiming||this.isAimFixed;
let camElev=isAim?2.0:2.5;
let focusElev=isAim?2.2:2.6;
let focusDist=isAim?45:35;
this.viewAPosition.copy(this.targetEased).add(n).add(this.mousePanOffset).add(this.panViewOffset).add(this.recoilOffset);
this.viewAPosition.y+=camElev;
this.viewAFocus.copy(this.targetEased).add(this.mousePanOffset).add(this.panViewOffset).add(this.recoilOffset);
let sinY_f=Math.sin(this._orbitYaw),cosY_f=Math.cos(this._orbitYaw);
this.forwardVec.set(-sinY_f,0,-cosY_f).normalize();
this.viewAFocus.addScaledVector(this.forwardVec,focusDist);
this.viewAFocus.y+=focusElev;"""

new_calc = """let isAim=this.isAiming||this.isAimFixed;
let camH=isAim?0.55:0.70;
let focusH=isAim?0.55:0.70;
let focusDist=isAim?45.0:40.0;
let pivotY=0.85;

let cosP=Math.cos(this._orbitPitch);
let sinP=Math.sin(this._orbitPitch);
let sinY=Math.sin(this._orbitYaw);
let cosY=Math.cos(this._orbitYaw);

let rx=this._orbitDistance*cosP*sinY;
let ry=this._orbitDistance*sinP+camH;
let rz=this._orbitDistance*cosP*cosY;

this.angle.value.set(rx,ry,rz);
this.forwardVec.set(-sinY*cosP,-sinP,-cosY*cosP).normalize();

this.viewAPosition.copy(this.targetEased).add(this.mousePanOffset).add(this.panViewOffset).add(this.recoilOffset);
this.viewAPosition.x+=rx;
this.viewAPosition.y+=pivotY+ry;
this.viewAPosition.z+=rz;

this.viewAFocus.copy(this.targetEased).add(this.mousePanOffset).add(this.panViewOffset).add(this.recoilOffset);
this.viewAFocus.x+=this.forwardVec.x*focusDist;
this.viewAFocus.y+=pivotY+focusH+this.forwardVec.y*focusDist;
this.viewAFocus.z+=this.forwardVec.z*focusDist;"""

if old_calc in text:
    text = text.replace(old_calc, new_calc)
    print("Updated viewAPosition and viewAFocus camera math")
else:
    print("WARNING: old_calc not found")

# 4. In updatePlayerStartAngle: update distance dynamically based on aim
old_angle_set = """    let rx = this._orbitDistance * cosP * sinY;
    let ry = this._orbitDistance * sinP;
    let rz = this._orbitDistance * cosP * cosY;

    this.angle.value.set(rx, ry, rz);"""

new_angle_set = """    let targetDist = (this.isAiming || this.isAimFixed) ? 5.8 : 7.5;
    this._targetOrbitDistance += (targetDist - this._targetOrbitDistance) * Math.min(1.0, 10 * e);
    let rx = this._orbitDistance * cosP * sinY;
    let ry = this._orbitDistance * sinP + 0.70;
    let rz = this._orbitDistance * cosP * cosY;

    this.angle.value.set(rx, ry, rz);"""

if old_angle_set in text:
    text = text.replace(old_angle_set, new_angle_set)
    print("Updated updatePlayerStartAngle angle.value set")
else:
    print("WARNING: old_angle_set not found")

with open(path_cq, 'w', encoding='utf-8') as f:
    f.write(text)
print("CQl67Veh.js written successfully.")
