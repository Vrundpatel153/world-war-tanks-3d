import re
import os

html_path = r'C:\Users\Vrund Patel\Desktop\clone-game\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

print("=== 1. ADDING PHYSICAL IN-GAME TACTICAL CURSOR ELEMENT & STYLES ===")

# 1A. Add Tactical In-Game Cursor CSS
cursor_css = """    /* =========================================================
       PHYSICAL IN-GAME TACTICAL HARDWARE CURSOR
       ========================================================= */
    body.in-menu-mode,
    body.in-menu-mode *,
    body.in-menu-mode button,
    body.in-menu-mode a,
    body.in-menu-mode input {
      cursor: none !important;
    }

    #tactical-cursor {
      position: fixed;
      top: 0;
      left: 0;
      pointer-events: none;
      z-index: 99999999;
      display: none;
      transform: translate3d(-100px, -100px, 0);
      will-change: transform;
      user-select: none;
    }

    body.in-menu-mode #tactical-cursor {
      display: block;
    }

    .cursor-pointer-chevron {
      width: 22px;
      height: 22px;
      background: #c7ff72;
      clip-path: polygon(0% 0%, 0% 100%, 35% 75%, 60% 100%, 75% 90%, 50% 65%, 100% 65%);
      filter: drop-shadow(0 0 6px rgba(199, 255, 114, 0.9)) drop-shadow(0 2px 6px rgba(0, 0, 0, 0.9));
      transition: transform 0.08s ease, background 0.12s ease;
      transform-origin: 0 0;
    }

    .cursor-reticle-ring {
      position: absolute;
      top: -12px;
      left: -12px;
      width: 44px;
      height: 44px;
      border: 1.5px dashed rgba(199, 255, 114, 0.45);
      border-radius: 50%;
      opacity: 0;
      transform: scale(0.6);
      transition: opacity 0.15s ease, transform 0.15s ease, border-color 0.15s ease;
      pointer-events: none;
    }

    .cursor-center-dot {
      position: absolute;
      top: 1px;
      left: 1px;
      width: 3px;
      height: 3px;
      background: #ffffff;
      border-radius: 50%;
      box-shadow: 0 0 6px #ffffff;
      pointer-events: none;
    }

    #tactical-cursor.hovering .cursor-pointer-chevron {
      transform: scale(1.15);
      background: #ffffff;
    }

    #tactical-cursor.hovering .cursor-reticle-ring {
      opacity: 1;
      transform: scale(1.1) rotate(45deg);
      border: 2px solid #c7ff72;
      box-shadow: 0 0 16px rgba(199, 255, 114, 0.6);
    }

    #tactical-cursor.clicking .cursor-pointer-chevron {
      transform: scale(0.85);
      background: #00ffaa;
    }
\n"""

# Remove old SVG cursor styling if present
html = re.sub(
    r'body\.in-menu-mode,\s*body\.in-menu-mode #game-home-screen[^}]*\}',
    '',
    html
)
html = re.sub(
    r'body\.in-menu-mode button,\s*body\.in-menu-mode a[^}]*\}',
    '',
    html
)

pos_cursor_insert = html.find('/* =========================================================\n       CUSTOM TACTICAL IN-GAME CURSOR & SETTINGS SYSTEM')
if pos_cursor_insert != -1:
    html = html[:pos_cursor_insert] + cursor_css + html[pos_cursor_insert:]
else:
    pos_style = html.find('</style>')
    html = html[:pos_style] + cursor_css + html[pos_style:]
print("Added Physical In-Game Tactical Cursor CSS")


print("\n=== 2. DESIGNING AAA VIDEO GAME COMMAND DECK HOME SCREEN ===")

# Replace #game-home-screen styles with genuine AAA military command interface
aaa_home_css = """    /* =========================================================
       AUTHENTIC AAA VIDEO GAME COMMAND DECK & HOME SCREEN
       ========================================================= */
    #game-home-screen {
      position: fixed !important;
      inset: 0 !important;
      z-index: 100000 !important;
      display: flex !important;
      flex-direction: column !important;
      justify-content: space-between !important;
      align-items: center !important;
      padding: 32px 48px 24px 48px !important;
      box-sizing: border-box !important;
      pointer-events: auto !important;
      /* Genuine AAA Military Dark Slate Steel & Tactical Vignette */
      background: 
        radial-gradient(circle at 50% 25%, rgba(32, 41, 60, 0.75) 0%, rgba(13, 16, 24, 0.95) 60%, #080a0f 100%),
        linear-gradient(rgba(199, 255, 114, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(199, 255, 114, 0.03) 1px, #080a0f 1px) !important;
      background-size: 100% 100%, 40px 40px, 40px 40px !important;
      opacity: 1;
      visibility: visible;
      transition: opacity 0.35s cubic-bezier(0.16, 1, 0.3, 1), visibility 0.35s ease;
      font-family: "Rajdhani", "Barlow Condensed", sans-serif;
      user-select: none;
      overflow: hidden;
    }

    #game-home-screen.menu-hidden {
      opacity: 0 !important;
      visibility: hidden !important;
      pointer-events: none !important;
    }

    /* Top Command Header */
    .deck-top-bar {
      width: 100%;
      max-width: 1320px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(199, 255, 114, 0.2);
      padding-bottom: 14px;
      box-sizing: border-box;
    }

    .deck-brand {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .deck-badge {
      padding: 4px 10px;
      background: #c7ff72;
      color: #080a0f;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.14em;
      border-radius: 3px;
    }

    .deck-sector {
      font-size: 13px;
      font-weight: 700;
      color: #8f9bb3;
      letter-spacing: 0.12em;
      text-transform: uppercase;
    }

    .deck-telemetry {
      display: flex;
      align-items: center;
      gap: 16px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.1em;
      color: #68758d;
    }

    .deck-status-active {
      color: #00ffaa;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .deck-status-active::before {
      content: "";
      width: 8px;
      height: 8px;
      background: #00ffaa;
      border-radius: 50%;
      box-shadow: 0 0 8px #00ffaa;
      animation: status-blink 2s infinite ease-in-out;
    }

    @keyframes status-blink {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
    }

    /* Main Deck Layout: 2 High-Tech Columns */
    .deck-body {
      width: 100%;
      max-width: 1320px;
      display: grid;
      grid-template-columns: 460px 1fr;
      gap: 48px;
      align-items: center;
      margin: auto 0;
    }

    /* Left Column: Command & Deploy */
    .deck-left-col {
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    .deck-hero-title {
      font-family: "Rajdhani", "Barlow Condensed", sans-serif;
      font-size: 58px;
      font-weight: 900;
      line-height: 0.95;
      letter-spacing: 0.05em;
      color: #ffffff;
      text-transform: uppercase;
      text-shadow: 0 4px 20px rgba(0, 0, 0, 0.9);
      margin: 0;
    }

    .deck-hero-title span {
      color: #c7ff72;
      text-shadow: 0 0 24px rgba(199, 255, 114, 0.4);
    }

    .deck-hero-sub {
      font-size: 14px;
      font-weight: 700;
      color: #8f9bb3;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      margin-top: 4px;
    }

    /* Massive Primary DEPLOY CTA Button */
    .btn-deck-deploy {
      position: relative;
      width: 100%;
      padding: 20px 32px;
      background: linear-gradient(135deg, #c7ff72 0%, #a2e846 100%);
      color: #080a0f;
      border: none;
      clip-path: polygon(0 0, calc(100% - 16px) 0, 100% 16px, 100% 100%, 16px 100%, 0 calc(100% - 16px));
      font-family: "Rajdhani", "Barlow Condensed", sans-serif;
      font-size: 26px;
      font-weight: 900;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      gap: 4px;
      box-shadow: 0 8px 32px rgba(199, 255, 114, 0.3), inset 0 2px 0 rgba(255, 255, 255, 0.6);
      transition: all 0.15s ease;
      overflow: hidden;
    }

    .btn-deck-deploy:hover {
      background: linear-gradient(135deg, #d8ff8a 0%, #b4f757 100%);
      transform: translateY(-2px);
      box-shadow: 0 12px 40px rgba(199, 255, 114, 0.5), inset 0 2px 0 rgba(255, 255, 255, 0.8);
    }

    .btn-deck-deploy:active {
      transform: translateY(2px);
      box-shadow: 0 4px 16px rgba(199, 255, 114, 0.3);
    }

    .btn-deploy-main {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 28px;
      line-height: 1;
    }

    .btn-deploy-sub {
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.18em;
      color: #1e3302;
      opacity: 0.85;
    }

    /* Tactical Action Buttons */
    .deck-actions-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-top: 6px;
    }

    .btn-deck-action {
      width: 100%;
      padding: 13px 20px;
      background: rgba(19, 23, 34, 0.85);
      border: 1px solid #272f42;
      clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 10px, 100% 100%, 10px 100%, 0 calc(100% - 10px));
      color: #d1d5db;
      font-family: "Rajdhani", "Barlow Condensed", sans-serif;
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      transition: all 0.12s ease;
    }

    .btn-deck-action:hover {
      background: #1b2130;
      border-color: #c7ff72;
      color: #ffffff;
      transform: translateX(4px);
      box-shadow: 0 0 16px rgba(199, 255, 114, 0.15);
    }

    .action-num {
      color: #c7ff72;
      font-weight: 800;
      margin-right: 12px;
    }

    .action-arrow {
      color: #8f9bb3;
      font-size: 16px;
      transition: transform 0.12s ease;
    }

    .btn-deck-action:hover .action-arrow {
      color: #c7ff72;
      transform: translateX(4px);
    }

    /* Right Column: Tactical Armor Spec Sheet & Hologram */
    .deck-right-col {
      display: flex;
      flex-direction: column;
    }

    .tactical-spec-card {
      background: rgba(14, 18, 27, 0.9);
      border: 1px solid #242c3d;
      border-top: 3px solid #c7ff72;
      clip-path: polygon(0 0, 100% 0, 100% calc(100% - 16px), calc(100% - 16px) 100%, 0 100%);
      padding: 24px 28px;
      display: flex;
      flex-direction: column;
      gap: 18px;
      box-shadow: 0 16px 48px rgba(0, 0, 0, 0.6);
    }

    .spec-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      border-bottom: 1px solid #242c3d;
      padding-bottom: 14px;
    }

    .spec-asset-tag {
      font-size: 11px;
      font-weight: 800;
      color: #c7ff72;
      letter-spacing: 0.18em;
      text-transform: uppercase;
    }

    .spec-asset-name {
      font-size: 28px;
      font-weight: 900;
      color: #ffffff;
      letter-spacing: 0.08em;
      margin-top: 2px;
    }

    .spec-status-pill {
      padding: 4px 10px;
      background: rgba(0, 255, 170, 0.12);
      border: 1px solid #00ffaa;
      border-radius: 4px;
      color: #00ffaa;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.12em;
    }

    /* Telemetry Grid */
    .spec-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 14px 20px;
    }

    .spec-item {
      display: flex;
      flex-direction: column;
      gap: 3px;
      background: rgba(8, 10, 15, 0.5);
      border-left: 2px solid #363e52;
      padding: 8px 12px;
      border-radius: 0 4px 4px 0;
    }

    .spec-label {
      font-size: 11px;
      font-weight: 800;
      color: #727e96;
      letter-spacing: 0.12em;
      text-transform: uppercase;
    }

    .spec-value {
      font-size: 13px;
      font-weight: 700;
      color: #e2e8f0;
      letter-spacing: 0.06em;
    }

    .spec-value.highlight {
      color: #c7ff72;
    }

    .spec-footer-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(199, 255, 114, 0.06);
      border: 1px solid rgba(199, 255, 114, 0.15);
      padding: 10px 14px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 800;
      color: #c7ff72;
      letter-spacing: 0.1em;
    }

    /* Bottom Command Deck Footer */
    .deck-footer {
      width: 100%;
      max-width: 1320px;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 18px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      padding-top: 14px;
      font-size: 12px;
      color: #717d96;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      box-sizing: border-box;
      flex-wrap: wrap;
    }

    .deck-footer span {
      color: #c7ff72;
      font-weight: 800;
      background: rgba(199, 255, 114, 0.1);
      border: 1px solid rgba(199, 255, 114, 0.25);
      padding: 2px 6px;
      border-radius: 3px;
      margin-right: 4px;
    }
\n"""

# Replace old home screen CSS
pos_home_css_start = html.find('/* =========================================================\n       WORLD WAR TANKS: 3D ARMORED WARFARE - AUTHENTIC HOME SCREEN')
if pos_home_css_start != -1:
    pos_home_css_end = html.find('/* Tactical HUD: only visible in-game */', pos_home_css_start)
    if pos_home_css_end != -1:
        html = html[:pos_home_css_start] + aaa_home_css + "\n    " + html[pos_home_css_end:]
        print("Replaced old home CSS with AAA Video Game Command Deck CSS")

print("\n=== 3. REPLACING HOME SCREEN MARKUP WITH AAA VIDEO GAME COMMAND DECK ===")

aaa_home_markup = """    <!-- AAA Video Game Tactical Command Deck & Home Screen -->
    <div id="game-home-screen">
      <!-- Top Tactical Header Bar -->
      <div class="deck-top-bar">
        <div class="deck-brand">
          <span class="deck-badge">WW TANKS</span>
          <span class="deck-sector">COMBAT ZONE ALPHA // SIMULATOR BUILD V2.5</span>
        </div>
        <div class="deck-telemetry">
          <span id="deck-simulation-status" class="deck-status-active">SIMULATION ONLINE</span>
          <span>●</span>
          <span>FREE ROAM TESTING SANDBOX</span>
        </div>
      </div>

      <!-- Main Command Deck Body: 2 High-Tech Columns -->
      <div class="deck-body">
        <!-- Left Column: Combat Command & Deployment -->
        <div class="deck-left-col">
          <div>
            <h1 class="deck-hero-title">WORLD WAR <span>TANKS</span></h1>
            <div class="deck-hero-sub">3D Armored Tactical Combat Simulator</div>
          </div>

          <!-- Massive Primary DEPLOY CTA Button -->
          <button class="btn-deck-deploy" onclick="window.startGameFromMenu()">
            <div class="btn-deploy-main">
              <span>▶</span>
              <span id="btn-deck-play-txt">DEPLOY TO BATTLE</span>
            </div>
            <div class="btn-deploy-sub">ENTER OPEN WORLD BATTLEFIELD // FREE ROAM [ENTER]</div>
          </button>

          <!-- Tactical Actions Menu -->
          <div class="deck-actions-list">
            <button class="btn-deck-action" onclick="window.openMenuModal('modal-controls')">
              <div><span class="action-num">[01]</span><span>FIELD MANUAL &amp; CONTROLS</span></div>
              <span class="action-arrow">&rarr;</span>
            </button>
            <button class="btn-deck-action" onclick="window.openMenuModal('modal-options')">
              <div><span class="action-num">[02]</span><span>GRAPHICS &amp; SYSTEM SETTINGS</span></div>
              <span class="action-arrow">&rarr;</span>
            </button>
            <button class="btn-deck-action" onclick="window.openMenuModal('modal-map')">
              <div><span class="action-num">[03]</span><span>SECTOR ALPHA MAP &amp; RECON</span></div>
              <span class="action-arrow">&rarr;</span>
            </button>
            <button id="btn-home-audio" class="btn-deck-action" onclick="window.toggleMenuAudio()">
              <div><span class="action-num">[04]</span><span id="txt-home-audio">AUDIO SFX: ENABLED</span></div>
              <span class="action-arrow">&rarr;</span>
            </button>
          </div>
        </div>

        <!-- Right Column: Combat Vehicle Specs & Tactical Blueprint -->
        <div class="deck-right-col">
          <div class="tactical-spec-card">
            <div class="spec-header">
              <div>
                <div class="spec-asset-tag">ACTIVE COMBAT ASSET SPECIFICATIONS</div>
                <div class="spec-asset-name">T-84 COMBAT TANK</div>
              </div>
              <div class="spec-status-pill">COMBAT READY</div>
            </div>

            <div class="spec-grid">
              <div class="spec-item">
                <span class="spec-label">PRIMARY ARMAMENT</span>
                <span class="spec-value highlight">88mm KwK L/71 High-Velocity</span>
              </div>
              <div class="spec-item">
                <span class="spec-label">AMMUNITION TYPE</span>
                <span class="spec-value">APCR Kinetic Penetrator</span>
              </div>
              <div class="spec-item">
                <span class="spec-label">CHASSIS &amp; DRIVE</span>
                <span class="spec-value">Heavy Caterpillar Treads</span>
              </div>
              <div class="spec-item">
                <span class="spec-label">MAX VELOCITY</span>
                <span class="spec-value highlight">68 km/h (Boost Turbine)</span>
              </div>
              <div class="spec-item">
                <span class="spec-label">ARMOR INTEGRITY</span>
                <span class="spec-value">100% Sloped Composite Steel</span>
              </div>
              <div class="spec-item">
                <span class="spec-label">TURRET MECHANISM</span>
                <span class="spec-value highlight">360&deg; Independent Traverse</span>
              </div>
              <div class="spec-item">
                <span class="spec-label">TARGETING OPTICS</span>
                <span class="spec-value">Combat Direct-Fire Zoom [R-Click]</span>
              </div>
              <div class="spec-item">
                <span class="spec-label">BALLISTICS ACCURACY</span>
                <span class="spec-value highlight">Zero-Convergence Reticle Lock</span>
              </div>
            </div>

            <div class="spec-footer-bar">
              <span>RAPID COMBAT DEPLOYMENT // SECTOR ALPHA</span>
              <span>100% OPERATIONAL</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom Tactical Keystrip -->
      <div class="deck-footer">
        <div><span>WASD</span> DRIVE TANK</div>
        <div>&middot;</div>
        <div><span>HOLD R-CLICK</span> COMBAT AIM ZOOM</div>
        <div>&middot;</div>
        <div><span>L-CLICK</span> FIRE 88mm CANNON</div>
        <div>&middot;</div>
        <div><span>Q / E</span> TURRET OVERRIDE</div>
        <div>&middot;</div>
        <div><span>SHIFT</span> TURBO BOOST</div>
        <div>&middot;</div>
        <div><span>ESC</span> SYSTEM PAUSE</div>
      </div>
    </div>
"""

# Replace old <div id="game-home-screen">...</div>
pos_home_start = html.find('<div id="game-home-screen">')
if pos_home_start != -1:
    pos_home_end = html.find('<!-- Modals: Controls & Settings -->', pos_home_start)
    if pos_home_end == -1:
        pos_home_end = html.find('<div id="modal-options"', pos_home_start)
    if pos_home_end != -1:
        html = html[:pos_home_start] + aaa_home_markup + "\n\n    " + html[pos_home_end:]
        print("Replaced old home screen markup with AAA Video Game Command Deck markup")

# Add physical tactical cursor element right before </body>
if '<div id="tactical-cursor"' not in html:
    pos_body_close = html.rfind('</body>')
    cursor_markup = """  <!-- Physical Hardware Tactical In-Game Cursor -->
  <div id="tactical-cursor">
    <div class="cursor-pointer-chevron"></div>
    <div class="cursor-reticle-ring"></div>
    <div class="cursor-center-dot"></div>
  </div>\n"""
    html = html[:pos_body_close] + cursor_markup + html[pos_body_close:]
    print("Injected #tactical-cursor element into body")

print("\n=== 4. UPDATING JS HANDLERS FOR PHYSICAL CURSOR & DECK PAUSE/RESUME ===")

cursor_js = """
      // PHYSICAL IN-GAME TACTICAL HARDWARE CURSOR ENGINE
      const _tacticalCursor = document.getElementById('tactical-cursor');
      if (_tacticalCursor) {
        window.addEventListener('mousemove', function(e) {
          _tacticalCursor.style.transform = `translate3d(${e.clientX}px, ${e.clientY}px, 0)`;
        }, { passive: true });

        document.addEventListener('mouseover', function(e) {
          if (e.target && e.target.closest('button, a, input, select, .opt-btn, .preset-card, .settings-tab-btn, .btn-deck-deploy, .btn-deck-action, .menu-modal-close, [role="button"]')) {
            _tacticalCursor.classList.add('hovering');
          } else {
            _tacticalCursor.classList.remove('hovering');
          }
        }, { passive: true });

        window.addEventListener('mousedown', function() {
          _tacticalCursor.classList.add('clicking');
        });
        window.addEventListener('mouseup', function() {
          _tacticalCursor.classList.remove('clicking');
        });
      }
"""

if 'PHYSICAL IN-GAME TACTICAL HARDWARE CURSOR ENGINE' not in html:
    pos_script_end = html.rfind('</script>')
    html = html[:pos_script_end] + cursor_js + "\n    " + html[pos_script_end:]
    print("Injected physical cursor tracking JS")

# Update openGameMenu and startGameFromMenu for deck labels
html = html.replace(
    "const playBtnTxt = document.querySelector('#btn-home-play-txt');\n        if (playBtnTxt) playBtnTxt.textContent = '▶ RESUME BATTLE';\n        const badge = document.querySelector('.home-badge');\n        if (badge) badge.textContent = '• COMBAT SIMULATION PAUSED •';",
    """const playBtnTxt = document.querySelector('#btn-deck-play-txt');
        if (playBtnTxt) playBtnTxt.textContent = 'RESUME BATTLE';
        const deckStatus = document.getElementById('deck-simulation-status');
        if (deckStatus) {
          deckStatus.textContent = 'SIMULATION PAUSED';
          deckStatus.style.color = '#ffcc00';
        }"""
)

html = html.replace(
    "window.startGameFromMenu = function() {\n        window.isGameMenuOpen = false;\n        const badge = document.querySelector('.home-badge');\n        if (badge) badge.textContent = '• COMBAT SIMULATOR - FREE ROAM ALPHA •';",
    """window.startGameFromMenu = function() {\n        window.isGameMenuOpen = false;
        const playBtnTxt = document.querySelector('#btn-deck-play-txt');
        if (playBtnTxt) playBtnTxt.textContent = 'DEPLOY TO BATTLE';
        const deckStatus = document.getElementById('deck-simulation-status');
        if (deckStatus) {
          deckStatus.textContent = 'SIMULATION ONLINE';
          deckStatus.style.color = '#00ffaa';
        }"""
)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved updated index.html successfully!")
