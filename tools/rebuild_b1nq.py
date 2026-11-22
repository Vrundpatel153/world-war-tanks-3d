import os
import subprocess

game_dir = r"C:\Users\Vrund Patel\Desktop\clone-game"
remote_path = os.path.join(game_dir, "assets", "B1Nq4Kq6.remote.js")
target_path = os.path.join(game_dir, "assets", "B1Nq4Kq6.js")

with open(remote_path, "r", encoding="utf-8") as f:
    c = f.read()

# 1. Neutralize skipGameplay class init
target_skip = "this.content=_.skipGameplay,this.init()}init(){this.initDOM(),this.bindEvents()}"
repl_skip = "this.content=_.skipGameplay,this.init()}init(){return;}"
assert target_skip in c, "target_skip not found"
c = c.replace(target_skip, repl_skip, 1)

# 2. Disable socialBox initialization
target_social = "this.socialBox&&this.socialBox.init(r?r.scene:n)"
repl_social = "0"
assert target_social in c, "target_social not found"
c = c.replace(target_social, repl_social, 1)

# 3. Disable StatueActionAnchor
target_statue = "initStatuePlaceholderPoint(t){t&&Jt({scene:this.scene,source:t,name:`StatueActionAnchor`,type:`OPEN`,handler:()=>{e.emit(`about-page:open`)}})}"
repl_statue = "initStatuePlaceholderPoint(t){return;}"
assert target_statue in c, "target_statue not found"
c = c.replace(target_statue, repl_statue, 1)

# 4. Disable PowerCoreMonitorAnchor
target_pc = "this.powerCoreMonitorAnchor=Jt({scene:this.scene,position:t,name:`PowerCoreMonitorAnchor`,handler:()=>{e.emit(`aboutproject:start-camera-sequence`,{targetPosition:t})}})"
repl_pc = "this.powerCoreMonitorAnchor=null"
assert target_pc in c, "target_pc not found"
c = c.replace(target_pc, repl_pc, 1)

# 5. Disable EB_Transition_Anchor
target_eb = "this.transitionAnchor=Jt({scene:this.scene,position:t,name:`EB_Transition_Anchor`,type:`OPEN`,key:`F`,distance:5,handler:()=>{e.emit(`page:bts:open`)}})"
repl_eb = "this.transitionAnchor=null"
assert target_eb in c, "target_eb not found"
c = c.replace(target_eb, repl_eb, 1)

# 6. Dusk filter opacity 0
target_dusk = "viewportFilterColor:`#ff8181`,viewportFilterOpacity:.15"
repl_dusk = "viewportFilterColor:`#ff8181`,viewportFilterOpacity:0"
assert target_dusk in c, "target_dusk not found"
c = c.replace(target_dusk, repl_dusk, 1)

# 7. Replace handlePointerVisual with Combat Aim Free Mouse Tracking + Q/E
hpv_target = "handlePointerVisual(e,t){this.rayCaster.setFromCamera(e.mouse,this.camera.instance);let n=null;this.turret.getWorldPosition(this.turretPos),this.groundPlane.constant=-this.turretPos.y,this.rayCaster.ray.intersectPlane(this.groundPlane,this.intersectPoint)&&(this.aimDir.set(this.intersectPoint.x-this.turretPos.x,0,this.intersectPoint.z-this.turretPos.z),this.aimDir.lengthSq()>this.aimLengthEpsilon&&(this.aimDir.normalize(),n=this.getTurretTargetQuat(this.aimDir))),this.applyTurretAim(n,t),this.aimRaycastAccumulator+=t,this.aimRaycastAccumulator>=.02&&(this.aimRaycastAccumulator=0,this.handleAiming(this.rayCaster))}"
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
      this.applyTurretAim(n, t * 3.2);
    }
    this.aimRaycastAccumulator += t;
    this.aimRaycastAccumulator >= .02 && (this.aimRaycastAccumulator = 0, this.handleAiming(this.rayCaster));
    return;
  }

  // Casual driving mode: Turret faces forward with hull heading (W) + Q/E manual offset
  this.turretManualAngle = 0;
  let manualOffset = this.turretManualOffset || 0;
  let n = this.targetTurretQuat.setFromAxisAngle(this.yAxis, manualOffset);
  this.applyTurretAim(n, t * 2.0);
  this.aimRaycastAccumulator += t;
  this.aimRaycastAccumulator >= .02 && (this.aimRaycastAccumulator = 0, this.handleAiming(this.rayCaster));
}"""
assert hpv_target in c, "hpv_target not found"
c = c.replace(hpv_target, new_hpv, 1)

# Syntax check
res = subprocess.run(['node', '--input-type=module', '--check'], input=c, capture_output=True, text=True)
if res.returncode != 0:
    print("SYNTAX ERROR:", res.stderr)
    exit(1)

with open(target_path, "w", encoding="utf-8") as f:
    f.write(c)

print(f"SUCCESS: {target_path} built and verified ({len(c)} bytes).")
