with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

hud_style = """
    <style id="tank-game-hud-style">
      /* Hide portfolio banners and promotional artifacts */
      [aria-label*="Skip gameplay"],
      [aria-label*="Open About Me"],
      [aria-label*="preview my projects"] {
        display: none !important;
      }

      /* World War Tank Combat HUD */
      #tank-hud {
        position: fixed;
        inset: 0;
        pointer-events: none;
        z-index: 100;
        font-family: "Barlow", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #ffffff;
        user-select: none;
      }

      /* Central Reticle */
      .tank-crosshair {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 64px;
        height: 64px;
        pointer-events: none;
      }
      .tank-crosshair svg {
        width: 100%;
        height: 100%;
        filter: drop-shadow(0 0 4px rgba(0, 255, 170, 0.6));
      }

      /* Top Header Banner */
      .tank-top-bar {
        position: absolute;
        top: 16px;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        align-items: center;
        gap: 16px;
        background: rgba(15, 20, 28, 0.75);
        border: 1px solid rgba(0, 255, 170, 0.35);
        border-radius: 6px;
        padding: 6px 20px;
        backdrop-filter: blur(8px);
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
      }
      .tank-top-bar .badge {
        background: #00ffaa;
        color: #0b0f15;
        padding: 2px 8px;
        border-radius: 3px;
        font-weight: 800;
      }

      /* Bottom Left: Vehicle Status & Hull Compass */
      .tank-status-panel {
        position: absolute;
        bottom: 24px;
        left: 24px;
        width: 280px;
        background: rgba(12, 17, 24, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-left: 4px solid #00ffaa;
        border-radius: 8px;
        padding: 16px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
      }
      .tank-status-title {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;
        font-size: 14px;
        font-weight: 800;
        letter-spacing: 0.08em;
        color: #00ffaa;
      }
      .tank-hp-bar-shell {
        width: 100%;
        height: 12px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 3px;
        overflow: hidden;
        margin-bottom: 8px;
      }
      .tank-hp-fill {
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, #00ffaa, #00bfff);
        transition: width 0.3s ease;
      }
      .tank-telemetry-row {
        display: flex;
        justify-content: space-between;
        font-size: 12px;
        color: #a0aec0;
        font-weight: 600;
      }
      .tank-telemetry-value {
        font-size: 16px;
        font-weight: 800;
        color: #ffffff;
      }

      /* Bottom Right: Weapon & Munitions Tray */
      .tank-weapon-panel {
        position: absolute;
        bottom: 24px;
        right: 24px;
        width: 260px;
        background: rgba(12, 17, 24, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-right: 4px solid #00d4ff;
        border-radius: 8px;
        padding: 16px;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        text-align: right;
      }
      .tank-weapon-name {
        font-size: 14px;
        font-weight: 800;
        color: #00d4ff;
        letter-spacing: 0.06em;
        margin-bottom: 4px;
      }
      .tank-status-ready {
        font-size: 13px;
        font-weight: 700;
        color: #00ffaa;
        margin-bottom: 8px;
      }
      .tank-ammo-counts {
        display: flex;
        justify-content: flex-end;
        gap: 16px;
        font-size: 12px;
        color: #cbd5e0;
      }

      /* Controls guide bottom bar */
      .tank-controls-bar {
        position: absolute;
        bottom: 12px;
        left: 50%;
        transform: translateX(-50%);
        font-size: 11px;
        color: rgba(255, 255, 255, 0.6);
        background: rgba(0, 0, 0, 0.5);
        padding: 4px 14px;
        border-radius: 20px;
        letter-spacing: 0.06em;
      }
      .tank-controls-bar span {
        color: #00ffaa;
        font-weight: 700;
      }
    </style>
"""

hud_html = """
    <!-- World War Tanks Game Tactical HUD -->
    <div id="tank-hud">
      <!-- Reticle -->
      <div class="tank-crosshair">
        <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
          <circle cx="32" cy="32" r="24" stroke="#00ffaa" stroke-width="1.5" stroke-dasharray="4 3" opacity="0.8"/>
          <circle cx="32" cy="32" r="3" fill="#00ffaa"/>
          <line x1="32" y1="4" x2="32" y2="16" stroke="#00ffaa" stroke-width="1.5"/>
          <line x1="32" y1="48" x2="32" y2="60" stroke="#00ffaa" stroke-width="1.5"/>
          <line x1="4" y1="32" x2="16" y2="32" stroke="#00ffaa" stroke-width="1.5"/>
          <line x1="48" y1="32" x2="60" y2="32" stroke="#00ffaa" stroke-width="1.5"/>
        </svg>
      </div>

      <!-- Top Combat Header -->
      <div class="tank-top-bar">
        <span class="badge">WW TANKS</span>
        <span>SECTOR: COMBAT ZONE ALPHA</span>
        <span style="color: #00ffaa;">● ONLINE</span>
      </div>

      <!-- Bottom Left Status Widget -->
      <div class="tank-status-panel">
        <div class="tank-status-title">
          <span>T-84 COMBAT TANK</span>
          <span id="tank-armor-txt">ARMOR: 100%</span>
        </div>
        <div class="tank-hp-bar-shell">
          <div id="tank-hp-bar" class="tank-hp-fill"></div>
        </div>
        <div class="tank-telemetry-row">
          <div>
            <div>SPEED</div>
            <div id="tank-speed-val" class="tank-telemetry-value">0 <span style="font-size: 11px;">KM/H</span></div>
          </div>
          <div>
            <div>GEAR</div>
            <div id="tank-gear-val" class="tank-telemetry-value" style="color: #00ffaa;">1ST</div>
          </div>
          <div>
            <div>HULL HEADING</div>
            <div id="tank-heading-val" class="tank-telemetry-value">035°</div>
          </div>
        </div>
      </div>

      <!-- Bottom Right Weapon Widget -->
      <div class="tank-weapon-panel">
        <div class="tank-weapon-name">88mm KwK HIGH-VELOCITY CANNON</div>
        <div id="tank-reload-status" class="tank-status-ready">● LOADED & READY</div>
        <div class="tank-ammo-counts">
          <div>APCR: <strong id="tank-ap-count" style="color: #ffffff;">38</strong></div>
          <div>HE SHELL: <strong id="tank-he-count" style="color: #ffffff;">14</strong></div>
        </div>
      </div>

      <!-- Controls hint -->
      <div class="tank-controls-bar">
        <span>WASD</span> TANK TREADS &middot; <span>MOUSE</span> TURRET AIM & CAMERA &middot; <span>SPACE / L-CLICK</span> FIRE &middot; <span>SHIFT</span> BOOST &middot; <span>SCROLL</span> ZOOM
      </div>
    </div>

    <!-- HUD Telemetry & Key Update Script -->
    <script>
      (function() {
        let currentSpeed = 0;
        let targetSpeed = 0;
        let gear = 'NEUT';
        let isDrivingForward = false;
        let isDrivingReverse = false;
        let isBoosting = false;
        let heading = 35;
        let reloadTimer = 0;

        window.addEventListener('keydown', e => {
          if (e.code === 'KeyW') isDrivingForward = true;
          if (e.code === 'KeyS') isDrivingReverse = true;
          if (e.code === 'ShiftLeft' || e.code === 'ShiftRight') isBoosting = true;
          if (e.code === 'KeyA') heading = (heading - 3 + 360) % 360;
          if (e.code === 'KeyD') heading = (heading + 3) % 360;
          
          if (e.code === 'Space' && reloadTimer <= 0) {
            triggerShoot();
          }
        });

        window.addEventListener('keyup', e => {
          if (e.code === 'KeyW') isDrivingForward = false;
          if (e.code === 'KeyS') isDrivingReverse = false;
          if (e.code === 'ShiftLeft' || e.code === 'ShiftRight') isBoosting = false;
        });

        window.addEventListener('click', e => {
          // If not clicking on HUD panels
          if (!e.target.closest('#tank-hud, .about-page, [role="dialog"], button, a')) {
            if (reloadTimer <= 0) {
              triggerShoot();
            }
          }
        });

        function triggerShoot() {
          reloadTimer = 1.2; // 1.2 second reload cycle
          const statusEl = document.getElementById('tank-reload-status');
          const apEl = document.getElementById('tank-ap-count');
          if (statusEl) {
            statusEl.textContent = '⟳ RELOADING...';
            statusEl.style.color = '#ffaa00';
          }
          if (apEl) {
            let count = parseInt(apEl.textContent, 10);
            if (count > 0) apEl.textContent = count - 1;
          }
        }

        // 60FPS Telemetry Loop
        setInterval(() => {
          if (isDrivingForward) {
            const maxSpd = isBoosting ? 45 : 28;
            targetSpeed = maxSpd;
            gear = isBoosting ? '3RD' : (currentSpeed > 15 ? '2ND' : '1ST');
          } else if (isDrivingReverse) {
            targetSpeed = 14;
            gear = 'REV';
          } else {
            targetSpeed = 0;
            gear = currentSpeed < 1 ? 'NEUT' : '1ST';
          }

          // Smooth speed lerp
          currentSpeed += (targetSpeed - currentSpeed) * 0.12;
          if (Math.abs(currentSpeed) < 0.1) currentSpeed = 0;

          const speedEl = document.getElementById('tank-speed-val');
          const gearEl = document.getElementById('tank-gear-val');
          const headEl = document.getElementById('tank-heading-val');
          const statusEl = document.getElementById('tank-reload-status');

          if (speedEl) speedEl.innerHTML = Math.round(currentSpeed) + ' <span style="font-size: 11px;">KM/H</span>';
          if (gearEl) gearEl.textContent = gear;
          if (headEl) headEl.textContent = String(Math.round(heading)).padStart(3, '0') + '°';

          if (reloadTimer > 0) {
            reloadTimer -= 0.05;
            if (reloadTimer <= 0) {
              reloadTimer = 0;
              if (statusEl) {
                statusEl.textContent = '● LOADED & READY';
                statusEl.style.color = '#00ffaa';
              }
            }
          }
        }, 50);
      })();
    </script>
"""

# Insert style into head, hud into body
if "</head>" in html:
    html = html.replace("</head>", hud_style + "\n  </head>")

if "</body>" in html:
    html = html.replace("</body>", hud_html + "\n  </body>")

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Injected World War Tanks Game HUD and styling into index.html successfully!")
