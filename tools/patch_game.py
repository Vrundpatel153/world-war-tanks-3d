import re

# 1. Update CQl67Veh.js
path_cq = r"C:/Users/Vrund Patel/Desktop/clone-game/assets/CQl67Veh.js"
with open(path_cq, 'r', encoding='utf-8') as f:
    cq = f.read()

# Replace playerStartPosition
cq = cq.replace("this.playerStartPosition=new c(57.334,10.068,98.584)", "this.playerStartPosition=new c(18.0,7.8,87.0)")

# Replace onMove
old_target = """        const onMove = ev => {
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
                this._targetOrbitPitch = Math.max(0.04, Math.min(0.68, this._targetOrbitPitch));
                this._userLookTimer = 1.5;
            }
        };"""

new_target = """        const onMove = ev => {
            const isLocked = !!document.pointerLockElement;
            const isAimActive = this.isAiming || this.isAimFixed;
            let dx = 0, dy = 0;
            if(isLocked){
                dx = ev.movementX || 0;
                dy = ev.movementY || 0;
            } else {
                if(this._lastPointerX === undefined || this._lastPointerX === 0){
                    this._lastPointerX = ev.clientX;
                    this._lastPointerY = ev.clientY;
                    return;
                }
                dx = ev.clientX - this._lastPointerX;
                dy = ev.clientY - this._lastPointerY;
                this._lastPointerX = ev.clientX;
                this._lastPointerY = ev.clientY;
                if(Math.abs(dx) > 100 || Math.abs(dy) > 100){
                    dx = Math.sign(dx) * Math.min(Math.abs(dx), 30);
                    dy = Math.sign(dy) * Math.min(Math.abs(dy), 30);
                }
            }
            const sens = isAimActive ? 0.0020 : 0.0028;
            this._targetOrbitYaw -= dx * sens;
            this._targetOrbitPitch += dy * sens;
            this._targetOrbitPitch = Math.max(0.04, Math.min(0.65, this._targetOrbitPitch));
            this._userLookTimer = 5.0;
        };"""

if old_target in cq:
    cq = cq.replace(old_target, new_target)
    print("CQl67Veh.js onMove replaced successfully")
else:
    print("WARNING: old_target not found in CQl67Veh.js")

# Remove auto-align snapping
pattern = r"if\(this\._userLookTimer > 0\)\{\s*this\._userLookTimer -= e;\s*\} else if\(this\.robotIsMoving && this\.robot\)\{[\s\S]*?this\._targetOrbitYaw \+= diff \* Math\.min\(1\.0, 1\.8 \* e\);\s*\}\s*\}"
cq_sub, count = re.subn(pattern, "if(this._userLookTimer > 0){\n        this._userLookTimer -= e;\n    }", cq)
if count > 0:
    cq = cq_sub
    print("CQl67Veh.js autoalign removed successfully (count =", count, ")")
else:
    print("WARNING: autoalign pattern not matched in CQl67Veh.js")

with open(path_cq, 'w', encoding='utf-8') as f:
    f.write(cq)
print("CQl67Veh.js saved.")

# 2. Update B1Nq4Kq6.js
path_b1 = r"C:/Users/Vrund Patel/Desktop/clone-game/assets/B1Nq4Kq6.js"
with open(path_b1, 'r', encoding='utf-8') as f:
    b1 = f.read()

# Replace getPlayerStart
old_get_start = """getPlayerStart(){if(!this.scene)return null;if(!this.cachedPlayerStart){let e=this.scene.getObjectByName(`player_start`);if(!e)return null;let t=new V,n=new M;e.getWorldPosition(t),e.getWorldQuaternion(n),this.cachedPlayerStart={position:t,quaternion:n}}return this.cachedPlayerStart}"""
new_get_start = """getPlayerStart(){if(!this.scene)return null;if(!this.cachedPlayerStart){let e=this.scene.getObjectByName(`player_start`);if(e){e.position.set(18.0,7.8,87.0);e.updateMatrixWorld(!0)}let t=new V(18.0,7.8,87.0),n=new M(0,0,0,1);this.cachedPlayerStart={position:t,quaternion:n}}return this.cachedPlayerStart}"""

if old_get_start in b1:
    b1 = b1.replace(old_get_start, new_get_start)
    print("B1Nq4Kq6.js getPlayerStart replaced successfully")
else:
    print("WARNING: old_get_start not found in B1Nq4Kq6.js")

# Replace fallback start positions
b1 = b1.replace("new V(57.33,10.07,98.58)", "new V(18.0,7.8,87.0)")
b1 = b1.replace("new V(57.334,10.068,98.584)", "new V(18.0,7.8,87.0)")

# Disable tutorial cards creation in getCardConfig
old_card_config = "getCardConfig(){return this.isTouch?this.touchTutorialCardConfig:this.desktopTutorialCardConfig}"
new_card_config = "getCardConfig(){return{}}"
if old_card_config in b1:
    b1 = b1.replace(old_card_config, new_card_config)
    print("B1Nq4Kq6.js getCardConfig disabled successfully")
else:
    print("WARNING: old_card_config not found in B1Nq4Kq6.js")

with open(path_b1, 'w', encoding='utf-8') as f:
    f.write(b1)
print("B1Nq4Kq6.js saved.")
