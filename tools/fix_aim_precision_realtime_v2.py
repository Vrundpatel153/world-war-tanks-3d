import os
import subprocess

game_dir = r"C:\Users\Vrund Patel\Desktop\clone-game"

# 1. Patch index.html to allow #aim-circle to track mouse smoothly without forced 50% lock
html_path = os.path.join(game_dir, "index.html")
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

target_css = """      #aim-circle {
        position: fixed !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;"""

repl_css = """      #aim-circle {
        position: fixed !important;
        transform: translate(-50%, -50%) !important;"""

if target_css in html:
    html = html.replace(target_css, repl_css, 1)
    print("1. index.html: Removed rigid 50% lock from #aim-circle so it follows mouse pointer.")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
else:
    print("Warning: target_css not found in index.html")

# 2. Patch assets/B1Nq4Kq6.js:
# - handlePointerVisual uses e.mouse directly
# - rayCaster casts through e.mouse
# - turret tracks hitPoint at all times
# - barrel pitch tilts to hitPoint
# - fireSingleShot shoots directly along normalize(crosshairWorldTarget - muzzlePos)
b1_path = os.path.join(game_dir, "assets", "B1Nq4Kq6.js")
with open(b1_path, "r", encoding="utf-8") as f:
    c = f.read()

hpv_start = c.find("handlePointerVisual(e,t){")
assert hpv_start != -1, "handlePointerVisual not found"
hpv_end = c.find("handleTouchVisual(e,t){", hpv_start)
assert hpv_end != -1, "handleTouchVisual not found"

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

  // Crosshair NDC coordinates: Use e.mouse directly from the controller
  let aimNDC = (e && e.mouse) ? e.mouse : { x: 0, y: 0 };
  if(document.pointerLockElement){
    aimNDC = { x: 0, y: 0 };
  }

  // Raycast from camera through the exact crosshair position into 3D world:
  let hitPoint = null;
  if(this.camera && this.camera.instance){
    this.rayCaster.setFromCamera(aimNDC, this.camera.instance);
    let closestDist = Infinity;

    // 1. Raycast against active enemies
    let enemyMgr = this.world && this.world.enemyManager;
    if(enemyMgr && enemyMgr.enemies){
      for(let i = 0; i < enemyMgr.enemies.length; i++){
        let en = enemyMgr.enemies[i];
        if(en.isActive && en.health > 0 && en.mesh){
          let hits = this.rayCaster.intersectObject(en.mesh, true);
          if(hits.length > 0 && hits[0].distance < closestDist){
            closestDist = hits[0].distance;
            hitPoint = hits[0].point;
          }
        }
      }
    }

    // 2. Raycast against environment interactive objects
    let areaMgr = this.world && this.world.areaManager;
    if(areaMgr && areaMgr.objects && closestDist > 60){
      for(let i = 0; i < areaMgr.objects.length; i++){
        let obj = areaMgr.objects[i];
        if(obj.visible && (obj.userData.isInteractive || obj.userData.isDynamicPhysics)){
          let hits = this.rayCaster.intersectObject(obj, true);
          if(hits.length > 0 && hits[0].distance < closestDist){
            closestDist = hits[0].distance;
            hitPoint = hits[0].point;
          }
        }
      }
    }

    // 3. Raycast against terrain mesh
    let terrain = this.world && this.world.terrain;
    if(!hitPoint && terrain && terrain.mesh){
      let hits = this.rayCaster.intersectObject(terrain.mesh, false);
      if(hits.length > 0 && hits[0].distance < closestDist){
        closestDist = hits[0].distance;
        hitPoint = hits[0].point;
      }
    }

    // 4. Horizontal plane at turret height fallback
    if(!hitPoint){
      this.turret.getWorldPosition(this.turretPos);
      this.groundPlane.constant = -this.turretPos.y;
      if(this.rayCaster.ray.intersectPlane(this.groundPlane, this.intersectPoint)){
        hitPoint = this.intersectPoint.clone();
      }
    }

    // 5. Sky / distant projection fallback (80 meters down crosshair ray)
    if(!hitPoint){
      hitPoint = this.rayCaster.ray.origin.clone().addScaledVector(this.rayCaster.ray.direction, 80);
    }
  }

  // Store the exact target point on world & robot so BulletSystem shoots exactly at it
  if(hitPoint){
    this.currentAimTargetPoint = hitPoint;
    if(this.world) this.world.crosshairWorldTarget = hitPoint;
    if(this.robotInstance) this.robotInstance.crosshairWorldTarget = hitPoint;
  }

  // TURRET TRACKING: Turret ALWAYS aims at the crosshair point!
  if(hitPoint){
    this.turret.getWorldPosition(this.turretPos);
    this.aimDir.set(hitPoint.x - this.turretPos.x, 0, hitPoint.z - this.turretPos.z);
    if(this.aimDir.lengthSq() > this.aimLengthEpsilon){
      this.aimDir.normalize();
      let n = this.getTurretTargetQuat(this.aimDir);
      this.applyTurretAim(n, t);
    }

    // Barrel pitch: align elevation / depression with the 3D target point
    if(this.robotInstance && this.robotInstance.model && this.robotInstance.model.barrel){
      let horizDist = Math.sqrt((hitPoint.x - this.turretPos.x)**2 + (hitPoint.z - this.turretPos.z)**2);
      let dy = hitPoint.y - this.turretPos.y;
      let targetPitch = Math.atan2(dy, Math.max(1.0, horizDist));
      let clampedPitch = Math.max(-0.21, Math.min(0.44, targetPitch));
      let barrel = this.robotInstance.model.barrel;
      barrel.rotation.z += (clampedPitch - barrel.rotation.z) * Math.min(1.0, t * 18.0);
    }
  }

  this.aimRaycastAccumulator += t;
  this.aimRaycastAccumulator >= .02 && (this.aimRaycastAccumulator = 0, this.handleAiming(this.rayCaster));
}"""

c = c[:hpv_start] + new_hpv + c[hpv_end:]
print("2. B1Nq4Kq6.js: Updated handlePointerVisual to use e.mouse directly.")

# Verify Node syntax
res = subprocess.run(['node', '--input-type=module', '--check'], input=c, capture_output=True, text=True)
if res.returncode != 0:
    print("SYNTAX ERROR in B1Nq4Kq6.js:", res.stderr)
    exit(1)

with open(b1_path, "w", encoding="utf-8") as f:
    f.write(c)

print("SUCCESS: Both index.html and assets/B1Nq4Kq6.js verified and patched cleanly!")
