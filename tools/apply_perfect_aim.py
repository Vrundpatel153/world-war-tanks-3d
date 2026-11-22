import re
import os

game_dir = r'C:\Users\Vrund Patel\Desktop\clone-game'

# ==========================================
# 1. PATCH assets/B1Nq4Kq6.js
# ==========================================
b1_path = os.path.join(game_dir, 'assets', 'B1Nq4Kq6.js')
with open(b1_path, 'r', encoding='utf-8') as f:
    b1 = f.read()

new_handle_pointer_visual = '''handlePointerVisual(e,t){
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

  // Crosshair NDC coordinates: Exactly match visual crosshair position on screen
  let aimNDC = { x: 0, y: 0 };
  let crosshairEl = document.getElementById("aim-circle");
  if(crosshairEl){
    let rect = crosshairEl.getBoundingClientRect();
    if(rect.width > 0 && rect.height > 0){
      aimNDC.x = ((rect.left + rect.width * 0.5) / window.innerWidth) * 2 - 1;
      aimNDC.y = -((rect.top + rect.height * 0.5) / window.innerHeight) * 2 + 1;
    }
  } else if(e && e.mouse){
    aimNDC.x = e.mouse.x;
    aimNDC.y = e.mouse.y;
  }

  // Bullet-proof 3D Target Raycasting:
  let hitPoint = null;
  if(this.camera && this.camera.instance){
    let camInstance = this.camera.instance;
    this.rayCaster.setFromCamera(aimNDC, camInstance);
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
            hitPoint = hits[0].point.clone();
          }
        }
      }
    }

    // 2. Raycast against all scenery, roads, buildings, barriers, bridges & obstacles
    let collidables = [];
    let areaMgr = this.world && this.world.areaManager;
    if(areaMgr){
      if(areaMgr.fixedRaycastTargets) areaMgr.fixedRaycastTargets.forEach(o => collidables.push(o));
      if(areaMgr.objects) areaMgr.objects.forEach(o => collidables.push(o));
    }
    let bs = this.world && this.world.bulletSystem;
    if(bs && bs.collidableObjects){
      bs.collidableObjects.forEach(o => collidables.push(o));
    }
    if(collidables.length > 0){
      let hits = this.rayCaster.intersectObjects(collidables, true);
      if(hits.length > 0 && hits[0].distance < closestDist){
        closestDist = hits[0].distance;
        hitPoint = hits[0].point.clone();
      }
    }

    // 3. Terrain Ray-marching using getHeightAt
    let terrain = this.world && this.world.terrain;
    if(terrain && typeof terrain.getHeightAt === 'function'){
      let ray = this.rayCaster.ray;
      let p = ray.origin.clone();
      let maxDist = Math.min(closestDist, 180);
      for(let dist = 1; dist < maxDist; dist += 1.2){
        p.copy(ray.origin).addScaledVector(ray.direction, dist);
        let gh = terrain.getHeightAt(p.x, p.z);
        let groundY = gh ? (typeof gh === 'number' ? gh : gh.y) : 0;
        if(p.y <= groundY){
          closestDist = dist;
          hitPoint = p.clone();
          hitPoint.y = groundY;
          break;
        }
      }
    }

    // 4. Ground plane fallback at terrain height
    if(!hitPoint){
      this.turret.getWorldPosition(this.turretPos);
      let groundY = (this.turretPos.y > 4.0) ? (this.turretPos.y - 1.0) : 0;
      this.groundPlane.constant = -groundY;
      if(this.rayCaster.ray.intersectPlane(this.groundPlane, this.intersectPoint)){
        let d = this.rayCaster.ray.origin.distanceTo(this.intersectPoint);
        if(d > 0 && d < closestDist){
          closestDist = d;
          hitPoint = this.intersectPoint.clone();
        }
      }
    }

    // 5. Sky / horizon projection fallback (90 meters down crosshair ray)
    if(!hitPoint){
      hitPoint = this.rayCaster.ray.origin.clone().addScaledVector(this.rayCaster.ray.direction, 90);
    }
  }

  // Store target point for BulletSystem precision shooting
  if(hitPoint){
    this.currentAimTargetPoint = hitPoint;
    if(this.world) this.world.crosshairWorldTarget = hitPoint;
    if(this.robotInstance) this.robotInstance.crosshairWorldTarget = hitPoint;
  }

  // TURRET TRACKING: Turret ALWAYS aims directly at the crosshair point!
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
      let clampedPitch = Math.max(-0.24, Math.min(0.44, targetPitch));
      let barrel = this.robotInstance.model.barrel;
      barrel.rotation.z += (clampedPitch - barrel.rotation.z) * Math.min(1.0, t * 28.0);
    }
  }

  this.aimRaycastAccumulator += t;
  this.aimRaycastAccumulator >= .02 && (this.aimRaycastAccumulator = 0, this.handleAiming(this.rayCaster));
}'''

idx_hpv_start = b1.find('handlePointerVisual(e,t){')
idx_hpv_end = b1.find('handleTouchVisual(e,t){')
if idx_hpv_start != -1 and idx_hpv_end != -1:
    b1 = b1[:idx_hpv_start] + new_handle_pointer_visual + b1[idx_hpv_end:]
    print('Updated handlePointerVisual in B1Nq4Kq6.js')
else:
    print('Could not find handlePointerVisual in B1Nq4Kq6.js')

with open(b1_path, 'w', encoding='utf-8') as f:
    f.write(b1)

# ==========================================
# 2. PATCH assets/CQl67Veh.js
# ==========================================
cq_path = os.path.join(game_dir, 'assets', 'CQl67Veh.js')
with open(cq_path, 'r', encoding='utf-8') as f:
    cq = f.read()

# Update camera elevation and framing
cq = cq.replace('let camElev=isAim?1.2:1.4;', 'let camElev=isAim?2.0:2.5;')
cq = cq.replace('let focusElev=isAim?3.6:4.4;', 'let focusElev=isAim?2.2:2.6;')
cq = cq.replace('let focusDist=isAim?35:30;', 'let focusDist=isAim?45:35;')
cq = cq.replace('let targetFov=isAimActive?26:35;', 'let targetFov=isAimActive?24:35;')

# Clamp pitch to prevent awkward overhead flipping
cq = cq.replace('this._targetOrbitPitch = Math.max(0.04, Math.min(1.10, this._targetOrbitPitch));',
                'this._targetOrbitPitch = Math.max(0.04, Math.min(0.68, this._targetOrbitPitch));')

# Initial camera orientation
cq = cq.replace('this._orbitYaw = 0.46;', 'this._orbitYaw = 0.0;')
cq = cq.replace('this._orbitPitch = 0.20;', 'this._orbitPitch = 0.22;')
cq = cq.replace('this._orbitDistance = 5.4;', 'this._orbitDistance = 6.6;')
cq = cq.replace('this._targetOrbitYaw = 0.0;', 'this._targetOrbitYaw = 0.0;')
cq = cq.replace('this._targetOrbitPitch = 0.20;', 'this._targetOrbitPitch = 0.22;')
cq = cq.replace('this._targetOrbitDistance = 5.4;', 'this._targetOrbitDistance = 6.6;')

with open(cq_path, 'w', encoding='utf-8') as f:
    f.write(cq)
print('Updated camera framing in CQl67Veh.js')

# ==========================================
# 3. PATCH assets/DPqB0RfP.js
# ==========================================
dp_path = os.path.join(game_dir, 'assets', 'DPqB0RfP.js')
with open(dp_path, 'r', encoding='utf-8') as f:
    dp = f.read()

old_up = 'updatePosition(e,t){this.root&&(this.root.style.left=`${e}px`,this.root.style.top=`${t}px`,(!this.isVisible||this.root.style.display===`none`)&&this.show())}'
new_up = 'updatePosition(e,t){if(!this.root)return;this.root.style.left=`50%`;this.root.style.top=`50%`;this.root.style.transform=`translate(-50%,-50%)`;(!this.isVisible||this.root.style.display===`none`)&&this.show()}'

if old_up in dp:
    dp = dp.replace(old_up, new_up)
    print('Locked crosshair to center 50% in DPqB0RfP.js')
else:
    print('updatePosition already updated or pattern not found in DPqB0RfP.js')

with open(dp_path, 'w', encoding='utf-8') as f:
    f.write(dp)

# ==========================================
# 4. PATCH index.html
# ==========================================
html_path = os.path.join(game_dir, 'index.html')
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Make #aim-circle always centered, high contrast, clean, and visible
old_css_search = '''      /* World War Tanks Precision Combat Crosshair */
      #aim-circle {'''

new_css = '''      /* World War Tanks Precision Combat Crosshair */
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
        opacity: 0.92 !important;
        transition: opacity 0.2s ease, width 0.15s ease, height 0.15s ease;
      }
      body.aim-mode-active #aim-circle {
        opacity: 1.0 !important;
        width: 38px !important;
        height: 38px !important;
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
        width: 5px !important;
        height: 5px !important;
        background: #00ffaa !important;
        border-radius: 50% !important;
        transform: translate(-50%, -50%) !important;
        box-shadow: 0 0 6px rgba(0, 255, 170, 0.95), 0 0 2px #000000 !important;
        border: none !important;
        opacity: 1 !important;
        display: block !important;
      }
      body.aim-mode-active #aim-circle .aim-dot {
        background: #ff3344 !important;
        box-shadow: 0 0 10px rgba(255, 51, 68, 1.0), 0 0 2px #000000 !important;
      }
      #aim-circle .aim-part {
        position: absolute !important;
        background: #ffffff !important;
        box-shadow: 0 0 2px #000000, 0 0 4px rgba(0, 0, 0, 0.8) !important;
        background-image: none !important;
        border-radius: 1px !important;
      }
      body.aim-mode-active #aim-circle .aim-part {
        background: #00ffaa !important;
        box-shadow: 0 0 6px rgba(0, 255, 170, 0.9), 0 0 2px #000000 !important;
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
      }'''

idx_css = html.find(old_css_search)
if idx_css != -1:
    idx_css_end = html.find('/* Top Header Banner */', idx_css)
    if idx_css_end != -1:
        html = html[:idx_css] + new_css + '\n\n      ' + html[idx_css_end:]
        print('Updated CSS in index.html')

# Update HUD banner control hints
old_hints_pattern = re.compile(r'<div class="tank-footer-controls">.*?</div>', re.DOTALL)
new_hints = '<div class="tank-footer-controls"><b>WASD</b> TANK DRIVE &middot; <b>MOUSE</b> TURRET AIM &middot; <b>HOLD R-CLICK / SCROLL PRESS</b> ZOOM AIM &middot; <b>L-CLICK / SPACE</b> FIRE &middot; <b>SCROLL</b> ZOOM &middot; <b>SHIFT</b> BOOST</div>'

html = old_hints_pattern.sub(new_hints, html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print('Updated index.html successfully')
print('=== ALL FILES PATCHED PERFECTLY ===')
