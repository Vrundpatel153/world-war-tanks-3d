import os, re

BASE_DIR = r"C:\Users\Vrund Patel\Desktop\clone-game"

# -------------------------------------------------------------
# 1. PATCH CQl67Veh.js (Hero Showcase Turntable Orbit during Menu)
# -------------------------------------------------------------
path_cq = os.path.join(BASE_DIR, "assets", "CQl67Veh.js")
with open(path_cq, "r", encoding="utf-8") as f:
    cq = f.read()

target_cq = "if(this._userLookTimer > 0){\n        this._userLookTimer -= e;\n    }\n\n    let damp = 1 - Math.exp(-32 * e);"
replacement_cq = """if(this._userLookTimer > 0){
        this._userLookTimer -= e;
    }

    // Hero Showcase camera orbit when in Home Menu
    if(window.isGameMenuOpen){
        this._targetOrbitYaw = (this._targetOrbitYaw || 0) + 0.12 * e;
        this._targetOrbitPitch = 0.14;
        this._targetOrbitDistance = 6.4;
    }

    let damp = 1 - Math.exp(-32 * e);"""

if target_cq in cq:
    cq = cq.replace(target_cq, replacement_cq)
    print("1. CQl67Veh.js: Added Hero Showcase turntable orbit for Menu Mode.")
else:
    print("WARNING: target_cq not found in CQl67Veh.js")

with open(path_cq, "w", encoding="utf-8") as f:
    f.write(cq)


# -------------------------------------------------------------
# 2. PATCH B1Nq4Kq6.js (Pause vehicle input & shooting in Menu Mode)
# -------------------------------------------------------------
path_b1 = os.path.join(BASE_DIR, "assets", "B1Nq4Kq6.js")
with open(path_b1, "r", encoding="utf-8") as f:
    b1 = f.read()

target_b1_input = "(this.robotInstance.isDead||this.robotInstance.isStunned)&&(n={forward:!1,backward:!1,left:!1,right:!1,boost:!1,shoot:!1,moveDirection:new gt})"
replacement_b1_input = "(this.robotInstance.isDead||this.robotInstance.isStunned||window.isGameMenuOpen)&&(n={forward:!1,backward:!1,left:!1,right:!1,boost:!1,shoot:!1,moveDirection:new gt})"

if target_b1_input in b1:
    b1 = b1.replace(target_b1_input, replacement_b1_input)
    print("2a. B1Nq4Kq6.js: Paused driving input when window.isGameMenuOpen is true.")
else:
    print("WARNING: target_b1_input not found in B1Nq4Kq6.js")

target_b1_shoot = "handleShootRequest(){if(this.robotInstance.isDead||this.robotInstance.isStunned)"
replacement_b1_shoot = "handleShootRequest(){if(window.isGameMenuOpen)return;if(this.robotInstance.isDead||this.robotInstance.isStunned)"

if target_b1_shoot in b1:
    b1 = b1.replace(target_b1_shoot, replacement_b1_shoot)
    print("2b. B1Nq4Kq6.js: Paused shoot requests when window.isGameMenuOpen is true.")
else:
    print("WARNING: target_b1_shoot not found in B1Nq4Kq6.js")

with open(path_b1, "w", encoding="utf-8") as f:
    f.write(b1)


# -------------------------------------------------------------
# 3. PATCH index.html (Home Screen Menu HTML, CSS & Logic)
# -------------------------------------------------------------
path_html = os.path.join(BASE_DIR, "index.html")
with open(path_html, "r", encoding="utf-8") as f:
    html = f.read()

menu_css = """
    /* =========================================================
       WORLD WAR TANKS: 3D ARMORED WARFARE - HOME SCREEN MENU
       ========================================================= */
    #game-home-screen {
      position: fixed;
      inset: 0;
      z-index: 10000;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 36px 48px;
      box-sizing: border-box;
      pointer-events: auto;
      background: radial-gradient(circle at 50% 40%, rgba(10, 16, 26, 0.4) 0%, rgba(8, 12, 18, 0.82) 65%, rgba(5, 8, 12, 0.94) 100%);
      transition: opacity 0.45s cubic-bezier(0.16, 1, 0.3, 1), visibility 0.45s ease;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      user-select: none;
    }

    #game-home-screen.menu-hidden {
      opacity: 0;
      visibility: hidden;
      pointer-events: none;
    }

    /* Top Branding Bar */
    .menu-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      width: 100%;
    }

    .menu-brand {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .menu-tagline {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.22em;
      color: #00ffaa;
      text-transform: uppercase;
    }

    .menu-tagline .pill {
      background: rgba(0, 255, 170, 0.15);
      border: 1px solid #00ffaa;
      padding: 2px 8px;
      border-radius: 3px;
      font-size: 10px;
    }

    .menu-title {
      font-size: clamp(32px, 5vw, 56px);
      font-weight: 900;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      margin: 0;
      line-height: 1;
      background: linear-gradient(180deg, #ffffff 0%, #cbd5e0 60%, #94a3b8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      filter: drop-shadow(0 4px 16px rgba(0, 0, 0, 0.8));
    }

    .menu-subtitle {
      font-size: 14px;
      font-weight: 600;
      letter-spacing: 0.14em;
      color: #94a3b8;
      text-transform: uppercase;
    }

    .menu-top-right {
      display: flex;
      align-items: center;
      gap: 16px;
      background: rgba(15, 23, 34, 0.7);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 6px;
      padding: 8px 18px;
      backdrop-filter: blur(8px);
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.1em;
      color: #e2e8f0;
    }

    /* Main Center Section */
    .menu-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      margin: auto 0;
    }

    .menu-actions {
      display: flex;
      flex-direction: column;
      gap: 14px;
      width: 360px;
      max-width: 90vw;
    }

    .menu-btn {
      position: relative;
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: rgba(15, 23, 34, 0.82);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-left: 4px solid #4a5568;
      color: #ffffff;
      padding: 16px 22px;
      border-radius: 6px;
      font-size: 14px;
      font-weight: 800;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      cursor: pointer;
      backdrop-filter: blur(10px);
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
    }

    .menu-btn:hover {
      background: rgba(22, 34, 50, 0.92);
      border-color: rgba(255, 255, 255, 0.35);
      border-left-color: #00ffaa;
      transform: translateX(8px);
      box-shadow: 0 6px 24px rgba(0, 255, 170, 0.25);
    }

    .menu-btn.primary {
      background: linear-gradient(90deg, rgba(0, 255, 170, 0.22) 0%, rgba(0, 180, 255, 0.15) 100%);
      border: 1px solid #00ffaa;
      border-left: 6px solid #00ffaa;
      color: #00ffaa;
      font-size: 16px;
      padding: 20px 24px;
      box-shadow: 0 0 28px rgba(0, 255, 170, 0.3);
    }

    .menu-btn.primary:hover {
      background: linear-gradient(90deg, rgba(0, 255, 170, 0.35) 0%, rgba(0, 180, 255, 0.25) 100%);
      color: #ffffff;
      transform: translateX(10px) scale(1.02);
      box-shadow: 0 0 36px rgba(0, 255, 170, 0.5);
    }

    .menu-btn .btn-arrow {
      font-size: 18px;
      color: #00ffaa;
      transition: transform 0.2s ease;
    }

    .menu-btn:hover .btn-arrow {
      transform: translateX(4px);
    }

    /* Right Specifications Card */
    .menu-spec-card {
      width: 380px;
      background: rgba(12, 18, 28, 0.78);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-top: 4px solid #00d4ff;
      border-radius: 8px;
      padding: 24px;
      backdrop-filter: blur(12px);
      box-shadow: 0 12px 36px rgba(0, 0, 0, 0.5);
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    .spec-header {
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.18em;
      color: #00d4ff;
      text-transform: uppercase;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      padding-bottom: 8px;
    }

    .spec-title {
      font-size: 20px;
      font-weight: 900;
      color: #ffffff;
      letter-spacing: 0.04em;
    }

    .spec-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
      font-size: 12px;
    }

    .spec-item {
      display: flex;
      justify-content: space-between;
      color: #94a3b8;
      font-weight: 600;
    }

    .spec-item span:last-child {
      color: #e2e8f0;
      font-weight: 700;
    }

    .spec-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(0, 255, 170, 0.12);
      border: 1px solid rgba(0, 255, 170, 0.4);
      color: #00ffaa;
      padding: 6px 12px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.1em;
      align-self: flex-start;
      margin-top: 4px;
    }

    /* Footer Info */
    .menu-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      width: 100%;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.14em;
      color: #64748b;
      text-transform: uppercase;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      padding-top: 16px;
    }

    .menu-footer span {
      color: #00ffaa;
    }

    /* In-game return menu button */
    #btn-return-menu {
      position: absolute;
      top: 16px;
      left: 20px;
      z-index: 9999;
      background: rgba(12, 18, 28, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #e2e8f0;
      padding: 6px 14px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.1em;
      cursor: pointer;
      backdrop-filter: blur(8px);
      transition: all 0.2s ease;
      display: none;
    }

    #btn-return-menu:hover {
      background: rgba(0, 255, 170, 0.2);
      border-color: #00ffaa;
      color: #00ffaa;
      transform: scale(1.04);
    }

    /* Interactive Modals (Controls & Map Briefing) */
    .menu-modal-overlay {
      position: fixed;
      inset: 0;
      z-index: 10005;
      background: rgba(5, 8, 12, 0.85);
      backdrop-filter: blur(12px);
      display: none;
      place-items: center;
      padding: 24px;
      box-sizing: border-box;
    }

    .menu-modal-overlay.active {
      display: grid;
    }

    .menu-modal {
      width: 620px;
      max-width: 95vw;
      max-height: 85vh;
      overflow-y: auto;
      background: rgba(14, 20, 30, 0.95);
      border: 1px solid rgba(0, 255, 170, 0.35);
      border-radius: 8px;
      padding: 32px;
      box-shadow: 0 16px 48px rgba(0, 0, 0, 0.7);
      color: #e2e8f0;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .menu-modal-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
      padding-bottom: 12px;
    }

    .menu-modal-title {
      font-size: 20px;
      font-weight: 900;
      color: #00ffaa;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin: 0;
    }

    .menu-modal-close {
      background: none;
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #94a3b8;
      width: 32px;
      height: 32px;
      border-radius: 4px;
      cursor: pointer;
      font-size: 16px;
      font-weight: 800;
      display: grid;
      place-items: center;
      transition: all 0.2s ease;
    }

    .menu-modal-close:hover {
      border-color: #ff3366;
      color: #ff3366;
    }

    .controls-grid {
      display: grid;
      grid-template-columns: 140px 1fr;
      gap: 12px 18px;
      align-items: center;
      font-size: 13px;
    }

    .key-badge {
      display: inline-block;
      background: rgba(0, 255, 170, 0.15);
      border: 1px solid #00ffaa;
      color: #00ffaa;
      padding: 4px 10px;
      border-radius: 4px;
      font-weight: 800;
      font-size: 12px;
      letter-spacing: 0.08em;
      text-align: center;
    }

    /* Hide combat HUD elements while on Menu Screen */
    body.in-menu-mode .tank-top-bar,
    body.in-menu-mode .tank-status-panel,
    body.in-menu-mode .tank-weapon-panel,
    body.in-menu-mode .tank-controls-bar,
    body.in-menu-mode #aim-circle,
    body.in-menu-mode #fps-mode-badge,
    body.in-menu-mode #aim-required-alert {
      display: none !important;
    }
"""

menu_html = """
    <!-- In-Game Return to Menu Button -->
    <button id="btn-return-menu" onclick="window.openGameMenu()">⚙ MENU [ESC]</button>

    <!-- World War Tanks: Beautiful 3D Home Screen Menu -->
    <div id="game-home-screen" class="game-home-screen">
      <!-- Top Header -->
      <div class="menu-header">
        <div class="menu-brand">
          <div class="menu-tagline">
            <span class="pill">SIMULATOR V2.4</span>
            <span>TACTICAL ARMORED WARFARE</span>
          </div>
          <h1 class="menu-title">WORLD WAR TANKS</h1>
          <div class="menu-subtitle">OPEN WORLD 3D ARMORED COMBAT · COMBAT ZONE ALPHA</div>
        </div>
        <div class="menu-top-right">
          <span style="color: #00ffaa;">● SECTOR ALPHA</span>
          <span>FREE ROAM &amp; COMBAT</span>
          <span style="color: #00d4ff;">60 FPS READY</span>
        </div>
      </div>

      <!-- Center Content -->
      <div class="menu-content">
        <!-- Actions List -->
        <div class="menu-actions">
          <button class="menu-btn primary" onclick="window.startGameFromMenu()">
            <span>▶ DEPLOY TO BATTLEFIELD</span>
            <span class="btn-arrow">&rarr;</span>
          </button>
          <button class="menu-btn" onclick="window.openMenuModal('modal-controls')">
            <span>⚙ CONTROLS &amp; MANUAL</span>
            <span class="btn-arrow">&rsaquo;</span>
          </button>
          <button class="menu-btn" onclick="window.openMenuModal('modal-map')">
            <span>🌐 SECTOR INTEL &amp; MAP</span>
            <span class="btn-arrow">&rsaquo;</span>
          </button>
          <button class="menu-btn" id="btn-toggle-audio" onclick="window.toggleMenuAudio()">
            <span id="txt-audio-status">🔊 AUDIO: SFX ON</span>
            <span class="btn-arrow">&bull;</span>
          </button>
          <button class="menu-btn" onclick="window.toggleFullscreen()">
            <span>⚡ FULLSCREEN TOGGLE</span>
            <span class="btn-arrow">&harr;</span>
          </button>
        </div>

        <!-- Tank Specs Showcase Card -->
        <div class="menu-spec-card">
          <div class="spec-header">ACTIVE COMBAT ASSET SPECIFICATIONS</div>
          <div class="spec-title">T-84 COMBAT TANK</div>
          <div class="spec-list">
            <div class="spec-item">
              <span>PRIMARY ARMAMENT</span>
              <span style="color: #00ffaa;">88mm KwK L/71 HIGH-VELOCITY</span>
            </div>
            <div class="spec-item">
              <span>CHASSIS TYPE</span>
              <span>HEAVY CATERPILLAR TREADS</span>
            </div>
            <div class="spec-item">
              <span>MAX VELOCITY</span>
              <span>68 KM/H (WITH BOOST TURBINE)</span>
            </div>
            <div class="spec-item">
              <span>ARMOR INTEGRITY</span>
              <span>100% SLOPED COMPOSITE STEEL</span>
            </div>
            <div class="spec-item">
              <span>TRAVERSE MECHANISM</span>
              <span>360° HYDRAULIC TURRET + Q/E OVERRIDE</span>
            </div>
            <div class="spec-item">
              <span>TARGETING SYSTEM</span>
              <span>DIRECT-FIRE OPTICAL ZOOM (R-CLICK)</span>
            </div>
          </div>
          <div class="spec-badge">
            <span>● COMBAT READY &middot; ALL SYSTEMS ONLINE</span>
          </div>
        </div>
      </div>

      <!-- Footer Status -->
      <div class="menu-footer">
        <div>CONTROLS: <span>WASD</span> DRIVE &middot; <span>HOLD R-CLICK</span> AIM &middot; <span>L-CLICK</span> FIRE &middot; <span>Q / E</span> TURRET</div>
        <div>PRESS <span>[ENTER]</span> OR CLICK <span>DEPLOY</span> TO ENGAGE</div>
      </div>
    </div>

    <!-- Controls Manual Modal -->
    <div id="modal-controls" class="menu-modal-overlay">
      <div class="menu-modal">
        <div class="menu-modal-header">
          <h2 class="menu-modal-title">TANK COMBAT FIELD MANUAL</h2>
          <button class="menu-modal-close" onclick="window.closeMenuModal('modal-controls')">&times;</button>
        </div>
        <div class="controls-grid">
          <div><span class="key-badge">W / A / S / D</span></div>
          <div><strong>Tank Drive &amp; Steering:</strong> GTA-style car physics with forward drive, smooth proportional steering, and natural reverse.</div>

          <div><span class="key-badge">MOUSE MOVE</span></div>
          <div><strong>Camera Orbit &amp; Aim:</strong> Smooth 360° situational look around and independent turret orientation.</div>

          <div><span class="key-badge">HOLD R-CLICK</span></div>
          <div><strong>Precision Combat Aim:</strong> Zooms in over-the-turret sniper camera, aligns focus, and unlocks free target aiming.</div>

          <div><span class="key-badge">PRESS SCROLL</span></div>
          <div><strong>Toggle Aim Lock:</strong> Middle mouse button clicks lock/unlock Combat Aim mode without needing to hold right click.</div>

          <div><span class="key-badge">L-CLICK / SPACE</span></div>
          <div><strong>Fire 88mm Cannon:</strong> High-velocity APCR cannon shot directly where the crosshair points. Realistic breech recoil &amp; smoke.</div>

          <div><span class="key-badge">Q / E KEYS</span></div>
          <div><strong>Turret Swivel Override:</strong> Independently rotate turret left and right for 360° shooting and reverse defense while driving.</div>

          <div><span class="key-badge">SHIFT</span></div>
          <div><strong>Turbo Boost:</strong> High-output powertrain acceleration across hills and straightaways.</div>

          <div><span class="key-badge">SCROLL WHEEL</span></div>
          <div><strong>Camera Zoom:</strong> Adjust camera orbit distance from close tactical to wide panoramic view.</div>
        </div>
      </div>
    </div>

    <!-- Sector Intel / Map Modal -->
    <div id="modal-map" class="menu-modal-overlay">
      <div class="menu-modal">
        <div class="menu-modal-header">
          <h2 class="menu-modal-title">SECTOR ALPHA &middot; TACTICAL MAP INTEL</h2>
          <button class="menu-modal-close" onclick="window.closeMenuModal('modal-map')">&times;</button>
        </div>
        <div style="display: flex; flex-direction: column; gap: 14px; font-size: 13px; line-height: 1.6; color: #cbd5e0;">
          <p>
            <strong style="color: #00ffaa;">OPERATIONAL THEATER:</strong> Sector Alpha is a vast 4 square kilometer open-world combat testing ground featuring diverse topography, elevated bridges, asphalt roads, and industrial infrastructure.
          </p>
          <div style="background: rgba(0,0,0,0.3); border-left: 3px solid #00d4ff; padding: 12px 16px; border-radius: 4px;">
            <div style="font-weight: 800; color: #00d4ff; margin-bottom: 4px;">KEY TOPOGRAPHICAL FEATURES:</div>
            <ul style="margin: 0; padding-left: 20px;">
              <li><strong>Asphalt Highway Network:</strong> High-speed roadways connecting industrial hubs with concrete safety barriers and curbs.</li>
              <li><strong>Off-Road Plains &amp; Embankments:</strong> Variable grassy terrain testing track suspension and hill-climbing torque.</li>
              <li><strong>Industrial Compound:</strong> Shelters, storage bins, conduits, and heavy steel drainage pipes.</li>
              <li><strong>Tactical Obstacles:</strong> Abandoned dump trucks, wooden pallets/logs, fire hydrants, and highway fences.</li>
            </ul>
          </div>
          <p>
            <strong style="color: #ffaa00;">MISSION OBJECTIVE:</strong> Free-roam testing. Explore terrain, test vehicle maneuverability, practice high-velocity cannon ballistics, and engage autonomous combat targets across the sector.
          </p>
        </div>
      </div>
    </div>
"""

menu_script = """
    <script>
      // =========================================================
      // HOME SCREEN MENU STATE & TRANSITIONS
      // =========================================================
      window.isGameMenuOpen = true;
      document.body.classList.add('in-menu-mode');

      window.startGameFromMenu = function() {
        window.isGameMenuOpen = false;
        document.body.classList.remove('in-menu-mode');
        
        const menuEl = document.getElementById('game-home-screen');
        if (menuEl) menuEl.classList.add('menu-hidden');

        const btnReturn = document.getElementById('btn-return-menu');
        if (btnReturn) btnReturn.style.display = 'block';

        // Unlock camera from turntable to combat follow
        const cam = window._app && window._app.world ? window._app.world.camera : null;
        if (cam) {
          cam._targetOrbitPitch = 0.16;
          cam._targetOrbitDistance = 7.0;
        }
      };

      window.openGameMenu = function() {
        window.isGameMenuOpen = true;
        document.body.classList.add('in-menu-mode');

        const menuEl = document.getElementById('game-home-screen');
        if (menuEl) menuEl.classList.remove('menu-hidden');

        const btnReturn = document.getElementById('btn-return-menu');
        if (btnReturn) btnReturn.style.display = 'none';
      };

      window.openMenuModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) modal.classList.add('active');
      };

      window.closeMenuModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) modal.classList.remove('active');
      };

      // Close modal on background click
      document.querySelectorAll('.menu-modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', function(e) {
          if (e.target === this) this.classList.remove('active');
        });
      });

      // ESC key toggles menu
      window.addEventListener('keydown', function(e) {
        if (e.code === 'Escape') {
          // If a modal is open, close it first
          const openModal = document.querySelector('.menu-modal-overlay.active');
          if (openModal) {
            openModal.classList.remove('active');
            return;
          }
          if (window.isGameMenuOpen) {
            window.startGameFromMenu();
          } else {
            window.openGameMenu();
          }
        }
        if (window.isGameMenuOpen && (e.code === 'Enter' || e.code === 'Space')) {
          const openModal = document.querySelector('.menu-modal-overlay.active');
          if (!openModal) {
            window.startGameFromMenu();
          }
        }
      });

      // Audio toggle
      let _isAudioMuted = false;
      window.toggleMenuAudio = function() {
        _isAudioMuted = !_isAudioMuted;
        const txt = document.getElementById('txt-audio-status');
        if (txt) {
          txt.textContent = _isAudioMuted ? '🔇 AUDIO: SFX MUTED' : '🔊 AUDIO: SFX ON';
        }
        const app = window._app;
        if (app && app.world && app.world.audio) {
          try {
            if (_isAudioMuted) {
              app.world.audio.masterGain?.gain?.setValueAtTime(0, 0);
            } else {
              app.world.audio.masterGain?.gain?.setValueAtTime(1, 0);
            }
          } catch(e) {}
        }
      };

      // Fullscreen toggle
      window.toggleFullscreen = function() {
        if (!document.fullscreenElement) {
          document.documentElement.requestFullscreen().catch(() => {});
        } else {
          document.exitFullscreen().catch(() => {});
        }
      };
    </script>
"""

# Insert CSS right before </style>
if "/* WORLD WAR TANKS: 3D ARMORED WARFARE - HOME SCREEN MENU */" not in html:
    html = html.replace("</style>", menu_css + "\n    </style>")
    print("3a. index.html: Added Home Screen Menu CSS.")

# Insert HTML before </body>
if "id=\"game-home-screen\"" not in html:
    html = html.replace("</body>", menu_html + "\n" + menu_script + "\n</body>")
    print("3b. index.html: Added Home Screen Menu HTML, modals, and scripts.")

# Update startup-intro dismissal so it reveals the Home Screen Menu
target_intro_dismiss = """        if (intro && intro.style.display !== 'none' && !intro.classList.contains('startup-intro--dismissed')) {
          const btn = document.querySelector('.startup-intro__enter');
          if (btn) btn.click();
          intro.classList.add('startup-intro--dismissed');
          intro.style.display = 'none';
        }"""

replacement_intro_dismiss = """        if (intro && intro.style.display !== 'none' && !intro.classList.contains('startup-intro--dismissed')) {
          const btn = document.querySelector('.startup-intro__enter');
          if (btn) btn.click();
          intro.classList.add('startup-intro--dismissed');
          intro.style.display = 'none';
          // Ensure Home Screen Menu is visible
          window.openGameMenu();
        }"""

if target_intro_dismiss in html:
    html = html.replace(target_intro_dismiss, replacement_intro_dismiss)
    print("3c. index.html: Updated startup intro to seamlessly reveal Home Screen Menu.")

with open(path_html, "w", encoding="utf-8") as f:
    f.write(html)
print("index.html saved successfully.")
