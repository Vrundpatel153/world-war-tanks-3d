import os

game_dir = r"C:\Users\Vrund Patel\Desktop\clone-game"

# ==============================================================================
# 1. Patch DPqB0RfP.js: Fix inputEnabled default & fix swapped forward/backward
# ==============================================================================
dp_path = os.path.join(game_dir, "assets", "DPqB0RfP.js")
with open(dp_path, "r", encoding="utf-8") as f:
    dp = f.read()

# Make inputEnabled = true by default
dp = dp.replace("this.inputEnabled=!1,this.world=null", "this.inputEnabled=!0,this.world=null")

# Fix swapped backward / forward in getInput()
old_swap = "this.cachedInput.backward=t,this.cachedInput.forward=e"
new_swap = "this.cachedInput.backward=e,this.cachedInput.forward=t"
if old_swap in dp:
    dp = dp.replace(old_swap, new_swap)
    print("1a. DPqB0RfP.js: Fixed forward/backward swap in cachedInput.")
else:
    print("Warning: old_swap not found in DPqB0RfP.js")

# Also add Arrow keys support to inputMap
old_map = "this.inputMap=new Map([[`forward`,[`KeyW`]],[`backward`,[`KeyS`]],[`left`,[`KeyA`]],[`right`,[`KeyD`]]"
new_map = "this.inputMap=new Map([[`forward`,[`KeyW`,`ArrowUp`]],[`backward`,[`KeyS`,`ArrowDown`]],[`left`,[`KeyA`,`ArrowLeft`]],[`right`,[`KeyD`,`ArrowRight`]]"
if old_map in dp:
    dp = dp.replace(old_map, new_map)
    print("1b. DPqB0RfP.js: Added Arrow keys to inputMap.")

with open(dp_path, "w", encoding="utf-8") as f:
    f.write(dp)

# ==============================================================================
# 2. Patch B1Nq4Kq6.js: Dynamic body guarantee, GTA car forward/reverse physics
# ==============================================================================
b1_path = os.path.join(game_dir, "assets", "B1Nq4Kq6.js")
with open(b1_path, "r", encoding="utf-8") as f:
    b1 = f.read()

# Ensure robotRigidBody is Dynamic (0) during handlePhysics
target_guard = "let r=this.physicsWorld.robotRigidBody,i=r.linvel(),a=r.angvel()"
repl_guard = "let r=this.physicsWorld.robotRigidBody;r&&r.bodyType&&r.bodyType()!==0&&(r.setBodyType(0,!0),r.wakeUp());let i=r.linvel(),a=r.angvel()"
if target_guard in b1:
    b1 = b1.replace(target_guard, repl_guard)
    print("2a. B1Nq4Kq6.js: Added dynamic body enforcement.")
else:
    print("Warning: target_guard not found in B1Nq4Kq6.js")

# Find and replace the keyboard driving block
# Current block in b1:
old_phys_drive = "let s=(n.forward?-1:0)+ +!!n.backward,l=+!!n.left+(n.right?-1:0);if(this.world.grabMode&&this.world.grabMode.grabbedObject){let e=this.controller.keyPressed.has(`KeyW`),t=this.controller.keyPressed.has(`KeyS`),n=this.controller.keyPressed.has(`KeyA`),r=this.controller.keyPressed.has(`KeyD`);s=(t?-1:0)+ +!!e,l=+!!n+(r?-1:0)}let u=s!==0||l!==0;if(c=l!==0,u!==this.wasMoving&&(this.wasMoving=u,e.emit(`robot:moving`,u)),s!==0&&(o?this.applyAirMove(r,i,p,f,s,t):this.applyDriveMove(r,i,p,f,s,t)),l!==0){let e=o?this.airRotationControlFactor:1;let steerVal=(s>0)?-l:l;let steerScale=(s===0)?0.5:1.0;this.applyDriveRotation(r,a,n.boost,steerVal*steerScale,t,e)}s===0&&!o&&this.applyMoveFriction(r,i,f,t),l===0&&this.applyRotationDamping(r,a,t)"

new_phys_drive = "let s=(+!!n.forward)+(n.backward?-1:0),l=(+!!n.left)+(n.right?-1:0);if(this.controller&&this.controller.keyPressed){let e=this.controller.keyPressed.has(`KeyW`)||this.controller.keyPressed.has(`ArrowUp`),t=this.controller.keyPressed.has(`KeyS`)||this.controller.keyPressed.has(`ArrowDown`),rW=this.controller.keyPressed.has(`KeyA`),rE=this.controller.keyPressed.has(`KeyD`);(e||t)&&(s=(+!!e)+(t?-1:0)),(rW||rE)&&(l=(+!!rW)+(rE?-1:0))}let u=s!==0||l!==0;if(c=l!==0,u!==this.wasMoving&&(this.wasMoving=u,e.emit(`robot:moving`,u)),s!==0&&(o?this.applyAirMove(r,i,p,f,s,t):this.applyDriveMove(r,i,p,f,s,t)),l!==0){let e=o?this.airRotationControlFactor:1;let steerVal=(s<0)?-l:l;let steerScale=(s===0)?0.35:1.0;this.applyDriveRotation(r,a,n.boost,steerVal*steerScale,t,e)}s===0&&!o&&this.applyMoveFriction(r,i,f,t),l===0&&this.applyRotationDamping(r,a,t)"

if old_phys_drive in b1:
    b1 = b1.replace(old_phys_drive, new_phys_drive)
    print("2b. B1Nq4Kq6.js: Fixed forward (+1)/reverse (-1) throttle and GTA car steering.")
else:
    print("Warning: old_phys_drive not found in B1Nq4Kq6.js")

# Check applyDriveMove for reverse speed multiplier
old_apply_move = "let s=this.tempMoveVel.dot(this.tempDriveTargetDir)<this.reverseDotThreshold,c=0,l=0,u=r*o;s||(c=n.x*u*i,l=n.z*u*i);"
new_apply_move = "let s=this.tempMoveVel.dot(this.tempDriveTargetDir)<this.reverseDotThreshold,c=0,l=0,u=r*o*(i<0?0.6:1.0);s||(c=n.x*u*i,l=n.z*u*i);"
if old_apply_move in b1:
    b1 = b1.replace(old_apply_move, new_apply_move)
    print("2c. B1Nq4Kq6.js: Added smooth 60% reverse speed scaling.")

with open(b1_path, "w", encoding="utf-8") as f:
    f.write(b1)

# ==============================================================================
# 3. Patch index.html: Auto-enable input & dynamic body on start
# ==============================================================================
index_path = os.path.join(game_dir, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Add automatic input activation in HUD script
hud_init_target = "function updateHudTelemetry() {"
hud_init_repl = """// Auto-enable input and dynamic physics body immediately
        function ensureGameActive() {
          if (window._app && window._app.world) {
            const ctrl = window._app.world.controller;
            if (ctrl) ctrl.inputEnabled = true;
            const pw = window._app.world.physicsWorld;
            if (pw && pw.robotRigidBody && pw.robotRigidBody.bodyType && pw.robotRigidBody.bodyType() !== 0) {
              pw.robotRigidBody.setBodyType(0, true);
              pw.robotRigidBody.wakeUp();
            }
          }
        }
        setInterval(ensureGameActive, 500);

        function updateHudTelemetry() {"""

if hud_init_target in html and "ensureGameActive" not in html:
    html = html.replace(hud_init_target, hud_init_repl)
    print("3. index.html: Added ensureGameActive background check.")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

print("=== ALL DRIVING PHYSICS FIXES SUCCESSFULLY APPLIED ===")
