import os
import subprocess

game_dir = r"C:\Users\Vrund Patel\Desktop\clone-game"
b1_path = os.path.join(game_dir, "assets", "B1Nq4Kq6.js")

with open(b1_path, "r", encoding="utf-8") as f:
    c = f.read()

# 1. Update handlePointerVisual with 3D Crosshair Raycast Targeting + Turret & Barrel Pitch
old_hpv_start = "handlePointerVisual(e,t){"
hpv_start_idx = c.find(old_hpv_start)
assert hpv_start_idx != -1, "handlePointerVisual not found"
hpv_end_idx = c.find("handleTouchVisual(e,t){", hpv_start_idx)
assert hpv_end_idx != -1, "handleTouchVisual not found"

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

  // Calculate 3D target point under the center crosshair in world space:
  let hitPoint = null;
  if(this.camera && this.camera.instance){
    this.rayCaster.setFromCamera({ x: 0, y: 0 }, this.camera.instance);
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

    // 4. Ground plane fallback if ray points downward
    if(!hitPoint && this.rayCaster.ray.direction.y < -0.01){
      this.groundPlane.constant = 0;
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

  if(isAimActive && hitPoint){
    // FREE MOUSE AIM: Turret smoothly aligns horizontally with the target point
    this.turret.getWorldPosition(this.turretPos);
    this.aimDir.set(hitPoint.x - this.turretPos.x, 0, hitPoint.z - this.turretPos.z);
    if(this.aimDir.lengthSq() > this.aimLengthEpsilon){
      this.aimDir.normalize();
      let n = this.getTurretTargetQuat(this.aimDir);
      this.applyTurretAim(n, t * 5.0);
    }

    // Barrel pitch: align elevation / depression with the 3D target point
    if(this.robotInstance && this.robotInstance.model && this.robotInstance.model.barrel){
      let horizDist = Math.sqrt((hitPoint.x - this.turretPos.x)**2 + (hitPoint.z - this.turretPos.z)**2);
      let dy = hitPoint.y - this.turretPos.y;
      let targetPitch = Math.atan2(dy, Math.max(1.0, horizDist));
      // Clamp pitch between -12 deg (-0.21 rad) and +25 deg (+0.44 rad)
      let clampedPitch = Math.max(-0.21, Math.min(0.44, targetPitch));
      let barrel = this.robotInstance.model.barrel;
      barrel.rotation.z += (clampedPitch - barrel.rotation.z) * Math.min(1.0, t * 8.0);
    }

    this.aimRaycastAccumulator += t;
    this.aimRaycastAccumulator >= .02 && (this.aimRaycastAccumulator = 0, this.handleAiming(this.rayCaster));
    return;
  }

  // Casual driving mode: Turret faces forward with hull heading (W) + Q/E manual offset
  this.turretManualAngle = 0;
  let manualOffset = this.turretManualOffset || 0;
  let n = this.targetTurretQuat.setFromAxisAngle(this.yAxis, manualOffset);
  this.applyTurretAim(n, t * 2.5);

  // Reset barrel pitch smoothly in casual driving
  if(this.robotInstance && this.robotInstance.model && this.robotInstance.model.barrel){
    let barrel = this.robotInstance.model.barrel;
    barrel.rotation.z += (0 - barrel.rotation.z) * Math.min(1.0, t * 5.0);
  }

  this.aimRaycastAccumulator += t;
  this.aimRaycastAccumulator >= .02 && (this.aimRaycastAccumulator = 0, this.handleAiming(this.rayCaster));
}"""

c = c[:hpv_start_idx] + new_hpv + c[hpv_end_idx:]
print("1. Replaced handlePointerVisual with 3D Crosshair Raycast & Barrel Pitch.")

# 2. Update fireSingleShot in BulletSystem to shoot directly at crosshairWorldTarget
old_fss_start = "fireSingleShot(t=!1){"
fss_start_idx = c.find(old_fss_start)
assert fss_start_idx != -1, "fireSingleShot not found"
fss_end_idx = c.find("handleBurstShot(){", fss_start_idx)
assert fss_end_idx != -1, "handleBurstShot not found"

new_fss = """fireSingleShot(t=!1){
  let { basePos: r, baseDir: i } = this.getGunPosDir(!0);
  
  // Direct cannon shell trajectory directly towards 3D crosshair target
  let targetPoint = (this.world && this.world.crosshairWorldTarget) || (this.robot && this.robot.crosshairWorldTarget);
  if(!targetPoint){
    let cam = this.getActiveCamera();
    if(cam){
      let ray = new Pe;
      ray.setFromCamera({ x: 0, y: 0 }, cam);
      let terrain = this.world && this.world.terrain;
      let hits = (terrain && terrain.mesh) ? ray.intersectObject(terrain.mesh, false) : [];
      if(hits.length > 0){
        targetPoint = hits[0].point;
      } else {
        targetPoint = ray.ray.origin.clone().addScaledVector(ray.ray.direction, 80);
      }
    }
  }

  if(targetPoint){
    this.tempDir.copy(targetPoint).sub(r).normalize();
  } else {
    this.tempDir.copy(i);
  }

  // Laser-precision bullet initialization directly on target (zero random spread)
  this.initBulletParticle(r, this.tempDir, t);

  let o=.05, s=.22;
  if(this.handleRecoil(this.robot.model.turret, this.recoilDistance, o, s, 0),
     this.handleTurretLiftRecoil(o, s),
     this.handleBodyShootRecoil(i, o, s),
     this.handleRecoil(this.robot.model.barrel, this.barrelRecoilDistance, o, s, 0),
     this.muzzleFlash){
    let e = this.robot && this.robot.currentModelType || `player`,
        t = this.muzzleFlash,
        n = this.modelScale;
    e === `boss` && this.bossMuzzleFlash ? (t = this.bossMuzzleFlash, n = .2 * 1.1) : e === `fodder` && this.fodderMuzzleFlash && (t = this.fodderMuzzleFlash, n = .2);
    t && t.play({ position: r, direction: this.tempDir, bulletRadius: n });
  }
  e.emit(`bullet:shoot`, { position: r, direction: this.tempDir });
}"""

c = c[:fss_start_idx] + new_fss + c[fss_end_idx:]
print("2. Replaced fireSingleShot with pinpoint crosshair trajectory targeting.")

# Syntax check with Node
res = subprocess.run(['node', '--input-type=module', '--check'], input=c, capture_output=True, text=True)
if res.returncode != 0:
    print("SYNTAX ERROR:", res.stderr)
    exit(1)

with open(b1_path, "w", encoding="utf-8") as f:
    f.write(c)

print("SUCCESS: assets/B1Nq4Kq6.js verified and written cleanly!")
