with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace the HUD update loop with a real physics-linked loop
old_script_start = "<!-- HUD Telemetry & Key Update Script -->"
old_script_end = "})();\n    </script>"

start_idx = c.find(old_script_start)
end_idx = c.find(old_script_end, start_idx)

new_hud_script = """<!-- HUD Telemetry & Key Update Script -->
    <script>
      (function() {
        let reloadTimer = 0;
        let isBoosting = false;

        // Auto dismiss intro overlay upon enter click
        document.addEventListener('click', function(e) {
          const btn = e.target.closest('.startup-intro__enter');
          if (btn) {
            const intro = document.querySelector('.startup-intro');
            if (intro) {
              intro.classList.add('startup-intro--dismissed');
              intro.style.display = 'none';
            }
          }
        });

        // Pointer Lock on Canvas Click
        const canvas = document.querySelector('#webgl');
        if (canvas) {
          canvas.addEventListener('click', function() {
            if (!document.pointerLockElement) {
              canvas.requestPointerLock?.();
            }
          });
        }

        // Space key cannon firing
        window.addEventListener('keydown', function(e) {
          if (e.code === 'Space' && reloadTimer <= 0) {
            triggerShoot();
          }
          if (e.code === 'ShiftLeft' || e.code === 'ShiftRight') {
            isBoosting = true;
          }
        });

        window.addEventListener('keyup', function(e) {
          if (e.code === 'ShiftLeft' || e.code === 'ShiftRight') {
            isBoosting = false;
          }
        });

        function triggerShoot() {
          if (reloadTimer > 0) return;
          reloadTimer = 0.25;

          const reloadEl = document.querySelector('.tactical-hud__reload-indicator');
          if (reloadEl) {
            reloadEl.textContent = '● RECHARGING BREECH...';
            reloadEl.style.color = '#ffaa00';
          }

          // Trigger in-game bullet system fire
          if (window._app && window._app.world && window._app.world.bulletSystem) {
            window._app.world.bulletSystem.fireSingleShot?.();
          }

          // Screen recoil kick
          const ch = document.querySelector('#tank-crosshair');
          if (ch) {
            ch.style.transform = 'translate(-50%, -55%) scale(1.15)';
            setTimeout(() => {
              ch.style.transform = 'translate(-50%, -50%) scale(1.0)';
            }, 120);
          }
        }

        // High frequency 60fps real-time physics HUD telemetry sync
        function updateHudTelemetry() {
          requestAnimationFrame(updateHudTelemetry);

          if (reloadTimer > 0) {
            reloadTimer -= 0.016;
            if (reloadTimer <= 0) {
              reloadTimer = 0;
              const reloadEl = document.querySelector('.tactical-hud__reload-indicator');
              if (reloadEl) {
                reloadEl.textContent = '● LOADED & READY';
                reloadEl.style.color = '#00ffaa';
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

            const speedEl = document.querySelector('.tactical-hud__speed-val');
            if (speedEl) {
              speedEl.textContent = kmh + ' ';
            }

            // Gear determination
            const gearEl = document.querySelector('.tactical-hud__gear-val');
            if (gearEl) {
              if (kmh < 2) {
                gearEl.textContent = 'NEUT';
                gearEl.style.color = '#00ffaa';
              } else if (isBoosting || kmh > 65) {
                gearEl.textContent = 'BOOST';
                gearEl.style.color = '#ff3366';
              } else if (kmh < 20) {
                gearEl.textContent = '1ST';
                gearEl.style.color = '#00ffaa';
              } else if (kmh < 45) {
                gearEl.textContent = '2ND';
                gearEl.style.color = '#00ffaa';
              } else {
                gearEl.textContent = '3RD';
                gearEl.style.color = '#00ffaa';
              }
            }

            // Heading calculation from tank rotation
            const rot = body.rotation();
            const siny_cosp = 2 * (rot.w * rot.y + rot.x * rot.z);
            const cosy_cosp = 1 - 2 * (rot.y * rot.y + rot.z * rot.z);
            let yaw = Math.atan2(siny_cosp, cosy_cosp);
            let deg = Math.round((yaw * 180 / Math.PI + 360) % 360);
            const headingEl = document.querySelector('.tactical-hud__heading-val');
            if (headingEl) {
              headingEl.textContent = String(deg).padStart(3, '0') + '°';
            }

            // Armor integrity from robot health
            const robot = app.world.robot;
            if (robot) {
              const hp = typeof robot.health === 'number' ? robot.health : 100;
              const maxHp = typeof robot.maxHealth === 'number' ? robot.maxHealth : 100;
              const pct = Math.max(0, Math.min(100, Math.round(hp / maxHp * 100)));
              const bar = document.querySelector('.tactical-hud__bar-fill');
              const armorVal = document.querySelector('.tactical-hud__armor-val');
              if (bar) bar.style.width = pct + '%';
              if (armorVal) armorVal.textContent = pct + '%';
            }
          } catch (e) {}
        }

        requestAnimationFrame(updateHudTelemetry);
      })();
    </script>"""

if start_idx != -1 and end_idx != -1:
    c = c[:start_idx] + new_hud_script + c[end_idx + len(old_script_end):]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("SUCCESS: index.html HUD linked to real physics telemetry!")
else:
    print("WARNING: start_idx=%d, end_idx=%d" % (start_idx, end_idx))
