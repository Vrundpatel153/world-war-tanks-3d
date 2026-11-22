import os

game_dir = r"C:\Users\Vrund Patel\Desktop\clone-game"

# 1. Update index.html
index_path = os.path.join(game_dir, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

reticle_css_target_start = "/* Zelda-style Minimalist Fixed Center White Reticle */"
reticle_css_target_end = "/* Top Header Banner */"
start_idx = html.find(reticle_css_target_start)
end_idx = html.find(reticle_css_target_end)

if start_idx != -1 and end_idx != -1:
    new_reticle_css = """/* World War Tanks Single Precision Tactical Crosshair */
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
        opacity: 0.95;
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
      #aim-circle .aim-part {
        position: absolute !important;
        background: rgba(255, 255, 255, 0.92) !important;
        box-shadow: 0 0 3px rgba(0, 0, 0, 0.9) !important;
        background-image: none !important;
        border-radius: 1px !important;
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
    html = html[:start_idx] + new_reticle_css + html[end_idx:]
    print("1a. index.html reticle CSS updated to single precision crosshair.")

# Update controls hint text in index.html
old_controls_hint = '<div class="tank-controls-bar">\n        <span>WASD</span> TANK TREADS &middot; <span>MOUSE</span> TURRET AIM & CAMERA &middot; <span>SPACE / L-CLICK</span> FIRE &middot; <span>SHIFT</span> BOOST &middot; <span>SCROLL</span> ZOOM\n      </div>'
new_controls_hint = '<div class="tank-controls-bar">\n        <span>WASD</span> DRIVE (GTA CAR) &middot; <span>MOUSE</span> 360&deg; LOOK &middot; <span>Q / E</span> ROTATE TURRET &middot; <span>C</span> RE-CENTER &middot; <span>SPACE / L-CLICK</span> FIRE &middot; <span>SHIFT</span> BOOST\n      </div>'

if old_controls_hint in html:
    html = html.replace(old_controls_hint, new_controls_hint)
    print("1b. index.html controls hint updated.")
else:
    print("Notice: old_controls_hint format differed.")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

# 2. Update assets/CQl67Veh.js
cq_path = os.path.join(game_dir, "assets", "CQl67Veh.js")
with open(cq_path, "r", encoding="utf-8") as f:
    cq = f.read()

old_clamp = "if (Math.abs(dx) > 160 || Math.abs(dy) > 160) { dx = 0; dy = 0; }"
new_clamp = "if (Math.abs(dx) > 120) dx = Math.sign(dx) * 120; if (Math.abs(dy) > 120) dy = Math.sign(dy) * 120;"
if old_clamp in cq:
    cq = cq.replace(old_clamp, new_clamp)
    print("2a. CQl67Veh.js clamp updated (no discarded flicks).")

old_damp = "let damp = 1 - Math.exp(-12 * e);"
new_damp = "let damp = 1 - Math.exp(-32 * e);"
if old_damp in cq:
    cq = cq.replace(old_damp, new_damp)
    print("2b. CQl67Veh.js damp rate updated to 32 (snappy, responsive mouse look).")

with open(cq_path, "w", encoding="utf-8") as f:
    f.write(cq)

# 3. Update assets/B1Nq4Kq6.js
b1_path = os.path.join(game_dir, "assets", "B1Nq4Kq6.js")
with open(b1_path, "r", encoding="utf-8") as f:
    b1 = f.read()

# Update rotationSpeed and rotationLerpRate for GTA car handling
b1 = b1.replace("this.rotationSpeed=4.8", "this.rotationSpeed=2.4")
b1 = b1.replace("this.rotationLerpRate=50", "this.rotationLerpRate=16")
b1 = b1.replace("this.driveLerpRate=16", "this.driveLerpRate=14")

old_phys_drive = "let s=(n.forward?-1:0)+ +!!n.backward,l=+!!n.left+(n.right?-1:0);if(this.world.grabMode&&this.world.grabMode.grabbedObject){let e=this.controller.keyPressed.has(`KeyW`),t=this.controller.keyPressed.has(`KeyS`),n=this.controller.keyPressed.has(`KeyA`),r=this.controller.keyPressed.has(`KeyD`);s=(t?-1:0)+ +!!e,l=+!!n+(r?-1:0)}let u=s!==0||l!==0;if(c=l!==0,u!==this.wasMoving&&(this.wasMoving=u,e.emit(`robot:moving`,u)),s!==0&&(o?this.applyAirMove(r,i,p,f,s,t):this.applyDriveMove(r,i,p,f,s,t)),l!==0){let e=o?this.airRotationControlFactor:1;this.applyDriveRotation(r,a,n.boost,l,t,e)}s===0&&!o&&this.applyMoveFriction(r,i,f,t),l===0&&this.applyRotationDamping(r,a,t)"

new_phys_drive = "let s=(n.forward?-1:0)+ +!!n.backward,l=+!!n.left+(n.right?-1:0);if(this.world.grabMode&&this.world.grabMode.grabbedObject){let e=this.controller.keyPressed.has(`KeyW`),t=this.controller.keyPressed.has(`KeyS`),n=this.controller.keyPressed.has(`KeyA`),r=this.controller.keyPressed.has(`KeyD`);s=(t?-1:0)+ +!!e,l=+!!n+(r?-1:0)}let u=s!==0||l!==0;if(c=l!==0,u!==this.wasMoving&&(this.wasMoving=u,e.emit(`robot:moving`,u)),s!==0&&(o?this.applyAirMove(r,i,p,f,s,t):this.applyDriveMove(r,i,p,f,s,t)),l!==0){let e=o?this.airRotationControlFactor:1;let steerVal=(s>0)?-l:l;let steerScale=(s===0)?0.5:1.0;this.applyDriveRotation(r,a,n.boost,steerVal*steerScale,t,e)}s===0&&!o&&this.applyMoveFriction(r,i,f,t),l===0&&this.applyRotationDamping(r,a,t)"

if old_phys_drive in b1:
    b1 = b1.replace(old_phys_drive, new_phys_drive)
    print("3a. B1Nq4Kq6.js handlePhysics updated (GTA car steering & reverse handling).")
else:
    print("Warning: old_phys_drive not found in B1Nq4Kq6.js")

with open(b1_path, "w", encoding="utf-8") as f:
    f.write(b1)

print("All patches applied successfully!")
