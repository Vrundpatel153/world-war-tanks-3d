import re

# 1. Patch index.html
path_html = "C:/Users/Vrund Patel/Desktop/clone-game/index.html"
with open(path_html, 'r', encoding='utf-8') as f:
    html = f.read()

# Fix updateHudTelemetry and triggerShoot in index.html
old_hud_block = """        function updateHudTelemetry() {
          requestAnimationFrame(updateHudTelemetry);

          if (!_cachedReloadEl) _cachedReloadEl = document.querySelector('.tactical-hud__reload-indicator');
          if (!_cachedSpeedEl) _cachedSpeedEl = document.querySelector('.tactical-hud__speed-val');
          if (!_cachedGearEl) _cachedGearEl = document.querySelector('.tactical-hud__gear-val');
          if (!_cachedHeadingEl) _cachedHeadingEl = document.querySelector('.tactical-hud__heading-val');
          if (!_cachedBarEl) _cachedBarEl = document.querySelector('.tactical-hud__bar-fill');
          if (!_cachedArmorEl) _cachedArmorEl = document.querySelector('.tactical-hud__armor-val');

          if (reloadTimer > 0) {
            reloadTimer -= 0.016;
            if (reloadTimer <= 0) {
              reloadTimer = 0;
              if (_cachedReloadEl && !_lastReloadReady) {
                _cachedReloadEl.textContent = '● LOADED & READY';
                _cachedReloadEl.style.color = '#00ffaa';
                _lastReloadReady = true;
              }
            }
          }

          try {
            const app = window._app;
            if (!app || !app.world || !app.world.physicsWorld || !app.world.physicsWorld.robotRigidBody) return;

            const body = app.world.physicsWorld.robotRigidBody;
            const linvel = body.linvel();
            const rawSpeed = Math.hypot(linvel.x, linvel.z);
            const kmh = Math.round(rawSpeed * 3.6);

            if (kmh !== _lastKmh && _cachedSpeedEl) {
              _lastKmh = kmh;
              _cachedSpeedEl.textContent = kmh + ' ';
            }

            // Gear determination
            let gearText = '1ST', gearColor = '#00ffaa';
            if (kmh < 2) {
              gearText = 'NEUT';
            } else if (isBoosting || kmh > 65) {
              gearText = 'BOOST';
              gearColor = '#ff3366';
            } else if (kmh < 20) {
              gearText = '1ST';
            } else if (kmh < 45) {
              gearText = '2ND';
            } else {
              gearText = '3RD';
            }

            if (gearText !== _lastGear && _cachedGearEl) {
              _lastGear = gearText;
              _cachedGearEl.textContent = gearText;
              _cachedGearEl.style.color = gearColor;
            }

            // Heading calculation from tank rotation
            const rot = body.rotation();
            const siny_cosp = 2 * (rot.w * rot.y + rot.x * rot.z);
            const cosy_cosp = 1 - 2 * (rot.y * rot.y + rot.z * rot.z);
            let yaw = Math.atan2(siny_cosp, cosy_cosp);
            let deg = Math.round((yaw * 180 / Math.PI + 360) % 360);
            if (deg !== _lastDeg && _cachedHeadingEl) {
              _lastDeg = deg;
              _cachedHeadingEl.textContent = String(deg).padStart(3, '0') + '°';
            }

            // Armor integrity from robot health
            const robot = app.world.robot;
            if (robot) {
              const hp = typeof robot.health === 'number' ? robot.health : 100;
              const maxHp = typeof robot.maxHealth === 'number' ? robot.maxHealth : 100;
              const pct = Math.max(0, Math.min(100, Math.round(hp / maxHp * 100)));
              if (pct !== _lastPct) {
                _lastPct = pct;
                if (_cachedBarEl) _cachedBarEl.style.width = pct + '%';
                if (_cachedArmorEl) _cachedArmorEl.textContent = pct + '%';
              }
            }
          } catch (e) {}
        }"""

new_hud_block = """        function updateHudTelemetry() {
          requestAnimationFrame(updateHudTelemetry);

          if (!_cachedReloadEl) _cachedReloadEl = document.querySelector('#tank-reload-indicator');
          if (!_cachedSpeedEl) _cachedSpeedEl = document.querySelector('#tank-speed-val');
          if (!_cachedGearEl) _cachedGearEl = document.querySelector('#tank-gear-val');
          if (!_cachedHeadingEl) _cachedHeadingEl = document.querySelector('#tank-heading-val');
          if (!_cachedBarEl) _cachedBarEl = document.querySelector('#tank-hp-bar');
          if (!_cachedArmorEl) _cachedArmorEl = document.querySelector('#tank-armor-txt');

          if (reloadTimer > 0) {
            reloadTimer -= 0.016;
            if (reloadTimer <= 0) {
              reloadTimer = 0;
              if (_cachedReloadEl && !_lastReloadReady) {
                _cachedReloadEl.textContent = '● LOADED & READY';
                _cachedReloadEl.style.color = '#00ffaa';
                _lastReloadReady = true;
              }
            }
          }

          try {
            const app = window._app;
            if (!app || !app.world || !app.world.physicsWorld || !app.world.physicsWorld.robotRigidBody) return;

            const body = app.world.physicsWorld.robotRigidBody;
            const linvel = body.linvel();
            const rawSpeed = Math.hypot(linvel.x, linvel.z);
            const kmh = Math.round(rawSpeed * 3.6);

            if (kmh !== _lastKmh && _cachedSpeedEl) {
              _lastKmh = kmh;
              _cachedSpeedEl.innerHTML = kmh + ' <span style="font-size: 11px;">KM/H</span>';
            }

            // Gear determination
            let gearText = '1ST', gearColor = '#00ffaa';
            if (kmh < 2) {
              gearText = 'NEUT';
            } else if (isBoosting || kmh > 45) {
              gearText = 'BOOST';
              gearColor = '#ff3366';
            } else if (kmh < 18) {
              gearText = '1ST';
            } else if (kmh < 35) {
              gearText = '2ND';
            } else {
              gearText = '3RD';
            }

            if (gearText !== _lastGear && _cachedGearEl) {
              _lastGear = gearText;
              _cachedGearEl.textContent = gearText;
              _cachedGearEl.style.color = gearColor;
            }

            // Heading calculation from tank rotation
            const rot = body.rotation();
            const siny_cosp = 2 * (rot.w * rot.y + rot.x * rot.z);
            const cosy_cosp = 1 - 2 * (rot.y * rot.y + rot.z * rot.z);
            let yaw = Math.atan2(siny_cosp, cosy_cosp);
            let deg = Math.round((yaw * 180 / Math.PI + 360) % 360);
            if (deg !== _lastDeg && _cachedHeadingEl) {
              _lastDeg = deg;
              _cachedHeadingEl.textContent = String(deg).padStart(3, '0') + '°';
            }

            // Armor integrity from robot health / mechanism
            const mech = app.world.mechanism;
            const hp = mech && typeof mech.playerHealth === 'number' ? mech.playerHealth : 30;
            const maxHp = mech && typeof mech.playerMaxHealth === 'number' ? mech.playerMaxHealth : 30;
            const pct = Math.max(0, Math.min(100, Math.round(hp / maxHp * 100)));
            if (pct !== _lastPct) {
              _lastPct = pct;
              if (_cachedBarEl) _cachedBarEl.style.width = pct + '%';
              if (_cachedArmorEl) _cachedArmorEl.textContent = 'ARMOR: ' + pct + '%';
            }
          } catch (e) {}
        }"""

if old_hud_block in html:
    html = html.replace(old_hud_block, new_hud_block)
    print("index.html updateHudTelemetry replaced successfully")
else:
    print("WARNING: old_hud_block not found in index.html")

# Fix triggerShoot selector in index.html
old_trigger = """        function triggerShoot() {
          if (reloadTimer > 0) return;
          reloadTimer = 0.25;

          const reloadEl = document.querySelector('.tactical-hud__reload-indicator');
          if (reloadEl) {
            reloadEl.textContent = '● RECHARGING BREECH...';
            reloadEl.style.color = '#ffaa00';
          }"""

new_trigger = """        function triggerShoot() {
          if (reloadTimer > 0) return;
          reloadTimer = 0.35;
          _lastReloadReady = false;

          const reloadEl = document.querySelector('#tank-reload-indicator');
          if (reloadEl) {
            reloadEl.textContent = '○ RELOADING...';
            reloadEl.style.color = '#ffaa00';
          }"""

if old_trigger in html:
    html = html.replace(old_trigger, new_trigger)
    print("index.html triggerShoot updated successfully")
else:
    print("WARNING: old_trigger not found in index.html")

# Remove broken duplicate script at bottom
old_dup = """  <script>
      // Left click fire trigger with aim check
      window.addEventListener('mousedown', function(e) {
        if (e.button === 0) {
          const app = window._app || window.app;
          const cam = app && app.camera;
          const isAim = cam && (cam.isAiming || cam.isAimFixed);
          if (!isAim) {
            const alertEl = document.getElementById('aim-required-alert');
            if (alertEl) {
              alertEl.classList.add('visible');
              clearTimeout(window._aimAlertTimer);
              window._aimAlertTimer = setTimeout(() => {
                alertEl.classList.remove('visible');
              }, 1800);
            }
          }
        }
      }, true);
</script>"""

if old_dup in html:
    html = html.replace(old_dup, "")
    print("index.html duplicate script removed successfully")
else:
    print("WARNING: old_dup not found in index.html")

with open(path_html, 'w', encoding='utf-8') as f:
    f.write(html)
print("index.html saved.")

# 2. Patch B1Nq4Kq6.js: isEnemyInView
path_b1 = "C:/Users/Vrund Patel/Desktop/clone-game/assets/B1Nq4Kq6.js"
with open(path_b1, 'r', encoding='utf-8') as f:
    b1 = f.read()

old_cull = "isEnemyInView(e){if(!e||!e.mesh)return!1;let t=this.world&&this.world.areaManager?this.world.areaManager.cullingManager:null;if(!t)return!0;let n=e.cullRadius||this.enemyCullRadius;return this.enemyCullSphere.set(e.mesh.position,n),t.intersectsSphere(this.enemyCullSphere)}"
new_cull = "isEnemyInView(e){if(!e||!e.mesh)return!1;let t=this.robot&&this.robot.model&&this.robot.model.object3D?this.robot.model.object3D.position:null;if(t&&e.mesh.position.distanceTo(t)<140)return!0;let n=this.world&&this.world.areaManager?this.world.areaManager.cullingManager:null;if(!n)return!0;let r=e.cullRadius||this.enemyCullRadius;return this.enemyCullSphere.set(e.mesh.position,r),n.intersectsSphere(this.enemyCullSphere)}"

if old_cull in b1:
    b1 = b1.replace(old_cull, new_cull)
    print("B1Nq4Kq6.js isEnemyInView updated successfully")
else:
    print("WARNING: old_cull not found in B1Nq4Kq6.js")

with open(path_b1, 'w', encoding='utf-8') as f:
    f.write(b1)
print("B1Nq4Kq6.js saved.")
