import re
import os

html_path = r'C:\Users\Vrund Patel\Desktop\clone-game\index.html'
js_cam_path = r'C:\Users\Vrund Patel\Desktop\clone-game\assets\CQl67Veh.js'

print("=== 1. PATCHING CQl67Veh.js (Camera & Mouse Controls) ===")
with open(js_cam_path, 'r', encoding='utf-8', errors='ignore') as f:
    js_content = f.read()

# 1A. In onDown: Add isGameMenuOpen check
if 'if(window.isGameMenuOpen) return;' not in js_content:
    js_content = js_content.replace(
        'const onDown = ev => {',
        'const onDown = ev => {\n            if(window.isGameMenuOpen) return;'
    )
    print("Added menu check to onDown")

# 1B. In onMove: Add isGameMenuOpen check & sensitivity + invertY multiplier
if 'if(window.isGameMenuOpen) return;' in js_content:
    pass
else:
    js_content = js_content.replace(
        'const onMove = ev => {',
        'const onMove = ev => {\n            if(window.isGameMenuOpen) return;'
    )
    print("Added menu check to onMove")

# Sens replacement
old_sens_calc = "const sens = isAimActive ? 0.0020 : 0.0028;\n            this._targetOrbitYaw -= dx * sens;\n            this._targetOrbitPitch += dy * sens;"
new_sens_calc = """const sens = (isAimActive ? 0.0020 : 0.0028) * (window.gameMouseSensMultiplier || 1.0);
            const effDy = (window.gameInvertY ? -1 : 1) * dy;
            this._targetOrbitYaw -= dx * sens;
            this._targetOrbitPitch += effDy * sens;"""

if old_sens_calc in js_content:
    js_content = js_content.replace(old_sens_calc, new_sens_calc)
    print("Updated sens and invertY in CQl67Veh.js")
else:
    # Try regex replacement if whitespace differed slightly
    pattern = r"const sens = isAimActive \? 0\.0020 : 0\.0028;\s+this\._targetOrbitYaw -= dx \* sens;\s+this\._targetOrbitPitch \+= dy \* sens;"
    if re.search(pattern, js_content):
        js_content = re.sub(pattern, new_sens_calc, js_content)
        print("Updated sens and invertY via regex in CQl67Veh.js")
    else:
        print("Note: sens calculation might already be modified or matched differently")

# 1C. In onWheel: Add isGameMenuOpen check
if 'const onWheel = ev => {\n            if(window.isGameMenuOpen) return;' not in js_content:
    js_content = js_content.replace(
        'const onWheel = ev => {',
        'const onWheel = ev => {\n            if(window.isGameMenuOpen) return;'
    )
    print("Added menu check to onWheel")

with open(js_cam_path, 'w', encoding='utf-8') as f:
    f.write(js_content)
print("Saved CQl67Veh.js successfully")


print("\n=== 2. PATCHING index.html (CSS, Settings Modal HTML & Controller JS) ===")
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 2A. Add Custom In-Game Cursor & Settings CSS
css_anchor = '/* =========================================================\n       WORLD WAR TANKS: 3D ARMORED WARFARE - AUTHENTIC HOME SCREEN'
if 'CUSTOM TACTICAL IN-GAME CURSOR' not in html:
    custom_css = """    /* =========================================================
       CUSTOM TACTICAL IN-GAME CURSOR & SETTINGS SYSTEM
       ========================================================= */
    body.in-menu-mode,
    body.in-menu-mode #game-home-screen,
    body.in-menu-mode .menu-modal-overlay,
    body.in-menu-mode .menu-modal {
      cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24'%3E%3Cpath d='M2 2 L2 20 L7 15 L12 22 L15 20 L10 13 L17 13 Z' fill='%23c7ff72' stroke='%2311121a' stroke-width='1.5' stroke-linejoin='round'/%3E%3C/svg%3E"), auto !important;
    }

    body.in-menu-mode button,
    body.in-menu-mode a,
    body.in-menu-mode input,
    body.in-menu-mode .opt-btn,
    body.in-menu-mode .preset-card,
    body.in-menu-mode .settings-tab-btn,
    body.in-menu-mode .menu-modal-close {
      cursor: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24'%3E%3Cpolygon points='2,2 2,19 6.5,14.5 11,21 13.5,19.5 9,13 15.5,13' fill='%23ffffff' stroke='%23c7ff72' stroke-width='1.5' stroke-linejoin='round'/%3E%3Ccircle cx='9' cy='13' r='2' fill='%23c7ff72'/%3E%3C/svg%3E"), pointer !important;
    }

    /* In-game Live FPS Badge */
    #live-fps-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      background: #11121a;
      border: 1px solid #272935;
      border-radius: 999px;
      color: #c7ff72;
      font-family: monospace;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.05em;
    }

    /* Pause Menu Header Return Button */
    #btn-return-menu {
      position: fixed;
      top: 18px;
      left: 18px;
      z-index: 999;
      background: #11121a;
      border: 1px solid #272935;
      color: #c7ff72;
      padding: 8px 16px;
      font-family: "Barlow", sans-serif;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.08em;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    #btn-return-menu:hover {
      background: #191b24;
      border-color: #c7ff72;
      box-shadow: 0 0 12px rgba(199, 255, 114, 0.25);
    }

    /* Settings Modal Navigation Tabs */
    .settings-tabs-bar {
      display: flex;
      gap: 8px;
      border-bottom: 2px solid #272935;
      padding-bottom: 12px;
      margin-bottom: 16px;
      overflow-x: auto;
    }

    .settings-tab-btn {
      background: #11121a;
      border: 1px solid #272935;
      color: #8f93a5;
      font-family: "Barlow", sans-serif;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      padding: 8px 16px;
      border-radius: 6px;
      transition: all 0.15s ease;
      white-space: nowrap;
    }

    .settings-tab-btn:hover {
      color: #ffffff;
      border-color: #393b49;
    }

    .settings-tab-btn.active {
      background: #191b24;
      border-color: #c7ff72;
      color: #c7ff72;
      box-shadow: 0 0 12px rgba(199, 255, 114, 0.15);
    }

    .settings-tab-pane {
      display: none;
      flex-direction: column;
      gap: 14px;
    }

    .settings-tab-pane.active {
      display: flex;
    }

    /* Settings Rows & Pill Buttons */
    .setting-row {
      display: flex;
      flex-direction: column;
      gap: 6px;
      padding: 12px 14px;
      background: #11121a;
      border: 1px solid #202330;
      border-radius: 8px;
    }

    .setting-label-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .setting-title {
      font-family: "Barlow", sans-serif;
      font-size: 13px;
      font-weight: 800;
      letter-spacing: 0.06em;
      color: #dfdfe2;
      text-transform: uppercase;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .setting-current-val {
      font-size: 11px;
      font-weight: 800;
      color: #c7ff72;
      letter-spacing: 0.06em;
    }

    .setting-desc {
      font-size: 11px;
      color: #686a77;
      margin: 0;
      line-height: 1.4;
    }

    .opt-btn-group {
      display: flex;
      gap: 6px;
      flex-wrap: wrap;
      margin-top: 4px;
    }

    .opt-btn {
      padding: 6px 14px;
      background: #191b24;
      border: 1px solid #272935;
      color: #8f93a5;
      border-radius: 6px;
      font-family: "Barlow", sans-serif;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      transition: all 0.12s ease;
    }

    .opt-btn:hover {
      border-color: #393b49;
      color: #dfdfe2;
    }

    .opt-btn.active {
      background: rgba(199, 255, 114, 0.12);
      border-color: #c7ff72;
      color: #c7ff72;
      box-shadow: 0 0 10px rgba(199, 255, 114, 0.2);
    }

    .preset-card-group {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      margin-top: 4px;
    }

    .preset-card {
      background: #11121a;
      border: 2px solid #272935;
      border-radius: 8px;
      padding: 10px 8px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
      cursor: pointer;
      transition: all 0.15s ease;
      text-align: center;
    }

    .preset-card:hover {
      border-color: #393b49;
      transform: translateY(-2px);
    }

    .preset-card.active {
      border-color: #c7ff72;
      background: rgba(199, 255, 114, 0.08);
      box-shadow: 0 0 16px rgba(199, 255, 114, 0.2);
    }

    .preset-name {
      font-family: "Crocante", display, sans-serif;
      font-size: 14px;
      font-weight: 900;
      letter-spacing: 0.05em;
      color: #ffffff;
    }

    .preset-card.active .preset-name {
      color: #c7ff72;
    }

    .preset-sub {
      font-size: 10px;
      color: #686a77;
      font-weight: 700;
    }

    /* Sliders */
    .setting-slider {
      width: 100%;
      height: 6px;
      background: #272935;
      border-radius: 3px;
      outline: none;
      -webkit-appearance: none;
      margin-top: 6px;
    }

    .setting-slider::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 18px;
      height: 18px;
      background: #c7ff72;
      border: 2px solid #11121a;
      border-radius: 50%;
      cursor: pointer;
      box-shadow: 0 0 8px rgba(199, 255, 114, 0.4);
    }
\n"""
    pos_css = html.find(css_anchor)
    if pos_css != -1:
        html = html[:pos_css] + custom_css + html[pos_css:]
        print("Injected custom cursor and settings CSS")

# 2B. Inject Live FPS badge in top bar if not present
if 'id="live-fps-badge"' not in html:
    pos_top = html.find('SECTOR: COMBAT ZONE ALPHA')
    if pos_top != -1:
        pos_div_end = html.find('</div>', pos_top)
        fps_badge_html = '\n      <div id="live-fps-badge" style="display: none;">⚡ <span id="live-fps-val">60</span> FPS</div>'
        html = html[:pos_div_end] + fps_badge_html + html[pos_div_end:]
        print("Injected live-fps-badge to top HUD")

# 2C. Replace #modal-options with full 4-tab Comprehensive Settings Modal
new_modal_html = """<!-- Comprehensive Game Options & Settings Modal -->
    <div id="modal-options" class="menu-modal-overlay">
      <div class="menu-modal" style="max-width: 680px; max-height: 85vh; overflow-y: auto;">
        <div class="menu-modal-header">
          <div style="display: flex; align-items: center; gap: 10px;">
            <span style="color: #c7ff72; font-size: 20px;">⚙</span>
            <h2 class="menu-modal-title">GAME OPTIONS &amp; SETTINGS</h2>
          </div>
          <button class="menu-modal-close" onclick="window.closeMenuModal('modal-options')">&times;</button>
        </div>

        <!-- Navigation Tabs -->
        <div class="settings-tabs-bar">
          <button id="tabbtn-graphics" class="settings-tab-btn active" onclick="window.switchSettingsTab('tab-graphics')">⚡ GRAPHICS &amp; VISUALS</button>
          <button id="tabbtn-controls" class="settings-tab-btn" onclick="window.switchSettingsTab('tab-controls')">🎮 CONTROLS &amp; CAMERA</button>
          <button id="tabbtn-audio" class="settings-tab-btn" onclick="window.switchSettingsTab('tab-audio')">🔊 AUDIO</button>
          <button id="tabbtn-intel" class="settings-tab-btn" onclick="window.switchSettingsTab('tab-intel')">🗺️ SECTOR INTEL</button>
        </div>

        <!-- TAB 1: GRAPHICS & VISUALS -->
        <div id="tab-graphics" class="settings-tab-pane active">
          <!-- 1-Click Master Presets -->
          <div class="setting-row">
            <div class="setting-label-row">
              <span class="setting-title">🔥 GRAPHICS PRESET (1-CLICK OPTIMIZATION)</span>
              <span id="txt-preset-val" class="setting-current-val">ULTRA</span>
            </div>
            <p class="setting-desc">Instantly configures resolution scaling, shadow maps, and visual post-processing for your hardware.</p>
            <div class="preset-card-group">
              <div id="preset-low" class="preset-card" onclick="window.applyPreset('low')">
                <span class="preset-name">LOW</span>
                <span class="preset-sub">60 FPS Locked</span>
              </div>
              <div id="preset-med" class="preset-card" onclick="window.applyPreset('med')">
                <span class="preset-name">MEDIUM</span>
                <span class="preset-sub">Balanced</span>
              </div>
              <div id="preset-high" class="preset-card" onclick="window.applyPreset('high')">
                <span class="preset-name">HIGH</span>
                <span class="preset-sub">Detailed FX</span>
              </div>
              <div id="preset-ultra" class="preset-card active" onclick="window.applyPreset('ultra')">
                <span class="preset-name">ULTRA</span>
                <span class="preset-sub">Max Quality</span>
              </div>
            </div>
          </div>

          <!-- Resolution Scaling (DPI) -->
          <div class="setting-row">
            <div class="setting-label-row">
              <span class="setting-title">🖥️ RENDER RESOLUTION SCALE (DPI)</span>
              <span id="txt-scale-val" class="setting-current-val">1.25x (HIGH RES)</span>
            </div>
            <p class="setting-desc">Adjusts internal rendering pixel density. Lower for smooth 60 FPS on laptops, higher for crystal clarity.</p>
            <div class="opt-btn-group">
              <button class="opt-btn" id="btn-scale-75" onclick="window.setResolutionScale(0.75, '0.75x (PERFORMANCE)')">0.75x PERFORMANCE</button>
              <button class="opt-btn" id="btn-scale-100" onclick="window.setResolutionScale(1.0, '1.0x (NATIVE 1080P)')">1.0x NATIVE (1080P)</button>
              <button class="opt-btn active" id="btn-scale-125" onclick="window.setResolutionScale(1.25, '1.25x (HIGH RES)')">1.25x HIGH RES</button>
              <button class="opt-btn" id="btn-scale-150" onclick="window.setResolutionScale(1.5, '1.5x (ULTRA RETINA)')">1.5x ULTRA RETINA</button>
            </div>
          </div>

          <!-- Dynamic Shadows -->
          <div class="setting-row">
            <div class="setting-label-row">
              <span class="setting-title">🌓 REAL-TIME SHADOW MAPS</span>
              <span id="txt-shadow-val" class="setting-current-val">ULTRA (2048px)</span>
            </div>
            <p class="setting-desc">Calculates high-definition directional sunlight casting and tank track shadows.</p>
            <div class="opt-btn-group">
              <button class="opt-btn" id="btn-shadow-off" onclick="window.setShadowQuality('off')">DISABLED</button>
              <button class="opt-btn" id="btn-shadow-low" onclick="window.setShadowQuality('low')">LOW (512px)</button>
              <button class="opt-btn" id="btn-shadow-med" onclick="window.setShadowQuality('med')">MEDIUM (1024px)</button>
              <button class="opt-btn active" id="btn-shadow-ultra" onclick="window.setShadowQuality('ultra')">ULTRA (2048px)</button>
            </div>
          </div>

          <!-- Bloom & Glow -->
          <div class="setting-row">
            <div class="setting-label-row">
              <span class="setting-title">✨ BLOOM &amp; HDR LIGHT GLOW</span>
              <span id="txt-bloom-val" class="setting-current-val">VIBRANT (0.6)</span>
            </div>
            <p class="setting-desc">Enhances muzzle flash intensity, tank headlamp optics, and ambient atmospheric haze.</p>
            <div class="opt-btn-group">
              <button class="opt-btn" id="btn-bloom-off" onclick="window.setBloom(0.0, 'OFF')">OFF</button>
              <button class="opt-btn" id="btn-bloom-subtle" onclick="window.setBloom(0.3, 'SUBTLE (0.3)')">SUBTLE (0.3)</button>
              <button class="opt-btn active" id="btn-bloom-vibrant" onclick="window.setBloom(0.6, 'VIBRANT (0.6)')">VIBRANT (0.6)</button>
              <button class="opt-btn" id="btn-bloom-cinematic" onclick="window.setBloom(0.9, 'CINEMATIC (0.9)')">CINEMATIC (0.9)</button>
            </div>
          </div>

          <!-- Chromatic Aberration -->
          <div class="setting-row">
            <div class="setting-label-row">
              <span class="setting-title">🎯 CHROMATIC LENS ABERRATION</span>
              <span id="txt-chroma-val" class="setting-current-val">MILD (0.0015)</span>
            </div>
            <p class="setting-desc">Simulates physical optical dispersion across wide focal lengths and high-speed maneuvers.</p>
            <div class="opt-btn-group">
              <button class="opt-btn" id="btn-chroma-off" onclick="window.setChromaticAberration(0.0, 'DISABLED')">DISABLED</button>
              <button class="opt-btn active" id="btn-chroma-mild" onclick="window.setChromaticAberration(0.0015, 'MILD (0.0015)')">MILD</button>
              <button class="opt-btn" id="btn-chroma-intense" onclick="window.setChromaticAberration(0.0028, 'INTENSE (0.0028)')">INTENSE</button>
            </div>
          </div>

          <!-- Anisotropic Texture Filtering -->
          <div class="setting-row">
            <div class="setting-label-row">
              <span class="setting-title">🔍 ANISOTROPIC TEXTURE FILTERING</span>
              <span id="txt-aniso-val" class="setting-current-val">16x ULTRA</span>
            </div>
            <p class="setting-desc">Preserves crisp road asphalt, rock surfaces, and terrain details at oblique camera angles.</p>
            <div class="opt-btn-group">
              <button class="opt-btn" id="btn-aniso-2" onclick="window.setAnisotropy(2)">2x FAST</button>
              <button class="opt-btn" id="btn-aniso-4" onclick="window.setAnisotropy(4)">4x BALANCED</button>
              <button class="opt-btn" id="btn-aniso-8" onclick="window.setAnisotropy(8)">8x HIGH</button>
              <button class="opt-btn active" id="btn-aniso-16" onclick="window.setAnisotropy(16)">16x ULTRA</button>
            </div>
          </div>

          <!-- Live In-Game FPS Counter -->
          <div class="setting-row">
            <div class="setting-label-row">
              <span class="setting-title">📊 LIVE IN-GAME FPS COUNTER</span>
              <span id="txt-fps-val" class="setting-current-val">ENABLED</span>
            </div>
            <p class="setting-desc">Renders real-time hardware telemetry and frame pacing badge on the upper tactical HUD.</p>
            <div class="opt-btn-group">
              <button class="opt-btn active" id="btn-fps-on" onclick="window.toggleFpsCounter(true)">ENABLED (ON)</button>
              <button class="opt-btn" id="btn-fps-off" onclick="window.toggleFpsCounter(false)">HIDDEN (OFF)</button>
            </div>
          </div>
        </div>

        <!-- TAB 2: CONTROLS & CAMERA -->
        <div id="tab-controls" class="settings-tab-pane">
          <!-- Mouse Sensitivity -->
          <div class="setting-row">
            <div class="setting-label-row">
              <span class="setting-title">🖱️ MOUSE TURRET &amp; LOOK SENSITIVITY</span>
              <span id="txt-sens-val" class="setting-current-val">1.0x (DEFAULT)</span>
            </div>
            <p class="setting-desc">Tunes mouse yaw/pitch camera orbit rate and fine optical aiming response.</p>
            <div class="opt-btn-group">
              <button class="opt-btn" id="btn-sens-50" onclick="window.setMouseSensitivity(0.5, '0.5x (SLOW)')">0.5x SLOW</button>
              <button class="opt-btn active" id="btn-sens-100" onclick="window.setMouseSensitivity(1.0, '1.0x (DEFAULT)')">1.0x DEFAULT</button>
              <button class="opt-btn" id="btn-sens-150" onclick="window.setMouseSensitivity(1.5, '1.5x (FAST)')">1.5x FAST</button>
              <button class="opt-btn" id="btn-sens-200" onclick="window.setMouseSensitivity(2.0, '2.0x (PRO)')">2.0x PRO</button>
            </div>
          </div>

          <!-- Invert Mouse Pitch -->
          <div class="setting-row">
            <div class="setting-label-row">
              <span class="setting-title">🔄 INVERT VERTICAL CAMERA (Y-AXIS)</span>
              <span id="txt-invert-val" class="setting-current-val">OFF</span>
            </div>
            <p class="setting-desc">Inverts pitch when moving the mouse up and down (flight simulator style).</p>
            <div class="opt-btn-group">
              <button class="opt-btn active" id="btn-invert-off" onclick="window.setInvertPitch(false)">NORMAL (OFF)</button>
              <button class="opt-btn" id="btn-invert-on" onclick="window.setInvertPitch(true)">INVERTED (ON)</button>
            </div>
          </div>

          <!-- Display Mode -->
          <div class="setting-row">
            <div class="setting-label-row">
              <span class="setting-title">🖥️ DISPLAY MODE</span>
              <span class="setting-current-val">WINDOWED / FULLSCREEN</span>
            </div>
            <div class="opt-btn-group">
              <button class="opt-btn" onclick="window.toggleFullscreen()">⛶ TOGGLE FULLSCREEN [F11]</button>
            </div>
          </div>
        </div>

        <!-- TAB 3: AUDIO -->
        <div id="tab-audio" class="settings-tab-pane">
          <!-- Master SFX Toggle -->
          <div class="setting-row">
            <div class="setting-label-row">
              <span class="setting-title">🔊 SOUND EFFECTS (SFX)</span>
              <span id="opt-txt-audio" class="setting-current-val">ENABLED</span>
            </div>
            <p class="setting-desc">Toggles tank diesel engine roar, 88mm cannon breech firing, track suspension clatter, and UI sounds.</p>
            <div class="opt-btn-group">
              <button class="opt-btn active" id="btn-audio-on" onclick="window.setAudioMuted(false)">🔊 SFX ENABLED</button>
              <button class="opt-btn" id="btn-audio-off" onclick="window.setAudioMuted(true)">🔇 MUTED</button>
            </div>
          </div>

          <!-- Volume Slider -->
          <div class="setting-row">
            <div class="setting-label-row">
              <span class="setting-title">🎚️ MASTER AUDIO VOLUME</span>
              <span id="txt-vol-val" class="setting-current-val">100%</span>
            </div>
            <input id="slider-volume" type="range" min="0" max="100" value="100" class="setting-slider" oninput="window.setMasterVolume(this.value)" />
          </div>
        </div>

        <!-- TAB 4: MAP INTEL -->
        <div id="tab-intel" class="settings-tab-pane">
          <div style="background: rgba(0,0,0,0.3); border-left: 3px solid #00d4ff; padding: 14px 18px; border-radius: 6px; font-size: 13px; line-height: 1.6; color: #cbd5e0;">
            <div style="font-weight: 800; color: #00d4ff; margin-bottom: 6px;">SECTOR ALPHA COMBAT ZONE:</div>
            <ul style="margin: 0; padding-left: 20px;">
              <li><strong>Open World Free Roam:</strong> Complete free testing sandbox with responsive tank dynamics, sloped terrain climbing, and destructible obstacles.</li>
              <li><strong>Primary Armament:</strong> 88mm KwK L/71 cannon firing APCR high-velocity kinetic rounds.</li>
              <li><strong>Controls:</strong> WASD to drive, Mouse to rotate turret &amp; aim, Hold Right-Click for Combat Sniper Zoom, Left-Click to fire.</li>
            </ul>
          </div>
        </div>

        <!-- Modal Footer -->
        <div style="margin-top: 24px; display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #272935; padding-top: 16px;">
          <span style="font-size: 11px; color: #686a77; font-weight: 700;">SETTINGS SAVED AUTOMATICALLY</span>
          <button class="btn-home-play" style="padding: 10px 24px; font-size: 16px; width: auto;" onclick="window.closeMenuModal('modal-options')">
            <span>CLOSE</span>
          </button>
        </div>
      </div>
    </div>"""

pos_modal_start = html.find('<div id="modal-options"')
if pos_modal_start != -1:
    pos_modal_end = html.find('<!-- Sector Intel / Map Modal -->', pos_modal_start)
    if pos_modal_end == -1:
        pos_modal_end = html.find('<div id="modal-controls"', pos_modal_start)
    if pos_modal_end != -1:
        html = html[:pos_modal_start] + new_modal_html + "\n\n    " + html[pos_modal_end:]
        print("Replaced #modal-options with full 4-tab Comprehensive Settings Modal")

# 2D. Add button to return to menu from gameplay (top left)
if 'id="btn-return-menu"' not in html:
    pos_body = html.find('<body>')
    if pos_body != -1:
        btn_html = '\n  <button id="btn-return-menu" onclick="window.openGameMenu()">⚙ MENU [ESC]</button>'
        html = html[:pos_body+6] + btn_html + html[pos_body+6:]
        print("Added #btn-return-menu to body")

# 2E. In canvas click and keydown handlers: ensure menu mode prevents lock & shooting
html = html.replace(
    'canvas.addEventListener(\'click\', function () {\n          if (!document.pointerLockElement) {\n            canvas.requestPointerLock?.();\n          }\n        });',
    'canvas.addEventListener(\'click\', function () {\n          if (window.isGameMenuOpen) return;\n          if (!document.pointerLockElement) {\n            canvas.requestPointerLock?.();\n          }\n        });'
)

# 2F. In ensureGameActive: Do not re-enable when menu is open
html = html.replace(
    'function ensureGameActive() {\n        if (window._app && window._app.world) {',
    'function ensureGameActive() {\n        if (window.isGameMenuOpen) return;\n        if (window._app && window._app.world) {'
)

# 2G. In mousedown firing: Skip if menu is open
html = html.replace(
    'window.addEventListener(\'mousedown\', function (e) {\n        if (e.button === 0) {',
    'window.addEventListener(\'mousedown\', function (e) {\n        if (window.isGameMenuOpen) return;\n        if (e.button === 0) {'
)

# 2H. Replace Script handlers with complete settings architecture
script_marker = '// CLEAN SEPARATION: LOADER -> HOME SCREEN -> 3D GAMEPLAY'
pos_script = html.find(script_marker)

new_script_code = """// CLEAN SEPARATION: LOADER -> HOME SCREEN -> 3D GAMEPLAY
      // =========================================================
      window.isGameMenuOpen = true;
      document.body.classList.add('in-menu-mode');

      // Comprehensive Settings State Store
      const SETTINGS_STORAGE_KEY = 'world_war_tanks_settings_v2';
      const defaultSettings = {
        preset: 'ultra',
        renderScale: 1.25,
        shadowQuality: 'ultra',
        bloomStrength: 0.6,
        chromaticAberration: 0.0015,
        anisotropy: 16,
        showFps: true,
        mouseSens: 1.0,
        invertY: false,
        audioMuted: false,
        masterVolume: 100
      };

      let currentSettings = { ...defaultSettings };
      try {
        const saved = localStorage.getItem(SETTINGS_STORAGE_KEY);
        if (saved) {
          currentSettings = { ...defaultSettings, ...JSON.parse(saved) };
        }
      } catch(e) {}

      window._gameSettings = currentSettings;
      window.gameMouseSensMultiplier = currentSettings.mouseSens;
      window.gameInvertY = currentSettings.invertY;

      function saveSettings() {
        try {
          localStorage.setItem(SETTINGS_STORAGE_KEY, JSON.stringify(currentSettings));
        } catch(e) {}
      }

      function dismissLoaderAndShowMenu() {
        const intro = document.getElementById('startup-intro');
        if (intro && !intro.classList.contains('loading-dismissed')) {
          intro.classList.add('loading-dismissed');
          setTimeout(() => {
            intro.style.display = 'none';
          }, 450);
        }
        const menu = document.getElementById('game-home-screen');
        if (menu) {
          menu.classList.remove('menu-hidden');
        }
      }

      // Check when 3D engine is initialized, then dismiss loader & apply settings
      let _loaderCheckInterval = setInterval(function() {
        if (window._app && window._app.world && window._app.world.camera) {
          clearInterval(_loaderCheckInterval);
          setTimeout(dismissLoaderAndShowMenu, 350);
          window.applyAllSettings();
        }
      }, 100);

      setTimeout(function() {
        clearInterval(_loaderCheckInterval);
        dismissLoaderAndShowMenu();
      }, 2200);

      // GAME PAUSE & RESUME MECHANISM
      window.startGameFromMenu = function() {
        window.isGameMenuOpen = false;
        document.body.classList.remove('in-menu-mode');
        
        const menuEl = document.getElementById('game-home-screen');
        if (menuEl) menuEl.classList.add('menu-hidden');

        // Close any active modal overlays
        document.querySelectorAll('.menu-modal-overlay.active').forEach(m => m.classList.remove('active'));

        const btnReturn = document.getElementById('btn-return-menu');
        if (btnReturn) btnReturn.style.display = 'flex';

        // Play authentic CTA sound if available
        try {
          const audio = new Audio('/assets/audio/ui/cta-button-click.mp3');
          audio.volume = 0.5;
          audio.play().catch(() => {});
        } catch(e) {}

        // UNPAUSE 3D SIMULATION & RESTORE AUDIO
        if (window._app) {
          if (window._app.time && typeof window._app.time.setTimeScale === 'function') {
            window._app.time.setTimeScale(1);
          }
          if (window._app.world) {
            if (window._app.world.time && typeof window._app.world.time.setTimeScale === 'function') {
              window._app.world.time.setTimeScale(1);
            }
            if (window._app.world.physicsWorld) {
              window._app.world.physicsWorld.enabled = true;
              if (window._app.world.physicsWorld.robotRigidBody) {
                window._app.world.physicsWorld.robotRigidBody.wakeUp();
              }
            }
            if (window._app.world.audio && window._app.world.audio.masterGain) {
              const vol = currentSettings.audioMuted ? 0 : (currentSettings.masterVolume / 100);
              try {
                window._app.world.audio.masterGain.gain.setValueAtTime(vol, 0);
              } catch(e) {}
            }
          }
        }

        // Position camera behind tank in combat view
        const cam = window._app && window._app.world ? window._app.world.camera : null;
        if (cam) {
          cam._targetOrbitPitch = 0.16;
          cam._targetOrbitDistance = 7.0;
        }
      };

      window.openGameMenu = function() {
        window.isGameMenuOpen = true;
        document.body.classList.add('in-menu-mode');

        // Unlock pointer so custom tactical cursor is freed
        try {
          if (document.exitPointerLock) document.exitPointerLock();
        } catch(e) {}

        // PAUSE 3D SIMULATION & MUFFLE ENGINE AUDIO
        if (window._app) {
          if (window._app.time && typeof window._app.time.setTimeScale === 'function') {
            window._app.time.setTimeScale(0);
          }
          if (window._app.world) {
            if (window._app.world.time && typeof window._app.world.time.setTimeScale === 'function') {
              window._app.world.time.setTimeScale(0);
            }
            if (window._app.world.physicsWorld) {
              window._app.world.physicsWorld.enabled = false;
            }
            if (window._app.world.audio && window._app.world.audio.masterGain) {
              try {
                window._app.world.audio.masterGain.gain.setValueAtTime(0.05, 0);
              } catch(e) {}
            }
          }
        }

        const menuEl = document.getElementById('game-home-screen');
        if (menuEl) menuEl.classList.remove('menu-hidden');

        const playBtnTxt = document.querySelector('#btn-home-play-txt');
        if (playBtnTxt) playBtnTxt.textContent = '▶ RESUME BATTLE';

        const btnReturn = document.getElementById('btn-return-menu');
        if (btnReturn) btnReturn.style.display = 'none';
      };

      // Modal management
      window.openMenuModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) modal.classList.add('active');
      };

      window.closeMenuModal = function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) modal.classList.remove('active');
      };

      document.querySelectorAll('.menu-modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', function(e) {
          if (e.target === this) this.classList.remove('active');
        });
      });

      // Settings Tab Switcher
      window.switchSettingsTab = function(tabId) {
        document.querySelectorAll('.settings-tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.settings-tab-pane').forEach(pane => pane.classList.remove('active'));

        const targetPane = document.getElementById(tabId);
        if (targetPane) targetPane.classList.add('active');

        const btnId = tabId.replace('tab-', 'tabbtn-');
        const targetBtn = document.getElementById(btnId);
        if (targetBtn) targetBtn.classList.add('active');
      };

      // ESC key toggles menu / modals
      window.addEventListener('keydown', function(e) {
        if (e.code === 'Escape') {
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

      // Settings Controllers
      window.applyPreset = function(preset) {
        currentSettings.preset = preset;
        if (preset === 'low') {
          currentSettings.renderScale = 0.85;
          currentSettings.shadowQuality = 'low';
          currentSettings.bloomStrength = 0.0;
          currentSettings.chromaticAberration = 0.0;
          currentSettings.anisotropy = 2;
        } else if (preset === 'med') {
          currentSettings.renderScale = 1.0;
          currentSettings.shadowQuality = 'med';
          currentSettings.bloomStrength = 0.3;
          currentSettings.chromaticAberration = 0.0;
          currentSettings.anisotropy = 4;
        } else if (preset === 'high') {
          currentSettings.renderScale = 1.25;
          currentSettings.shadowQuality = 'ultra';
          currentSettings.bloomStrength = 0.6;
          currentSettings.chromaticAberration = 0.0015;
          currentSettings.anisotropy = 8;
        } else if (preset === 'ultra') {
          currentSettings.renderScale = 1.5;
          currentSettings.shadowQuality = 'ultra';
          currentSettings.bloomStrength = 0.8;
          currentSettings.chromaticAberration = 0.0028;
          currentSettings.anisotropy = 16;
        }
        saveSettings();
        window.applyAllSettings();
        updateSettingsUI();
      };

      window.setResolutionScale = function(scale, label) {
        currentSettings.renderScale = scale;
        currentSettings.preset = 'custom';
        saveSettings();
        window.applyAllSettings();
        updateSettingsUI();
      };

      window.setShadowQuality = function(quality) {
        currentSettings.shadowQuality = quality;
        currentSettings.preset = 'custom';
        saveSettings();
        window.applyAllSettings();
        updateSettingsUI();
      };

      window.setBloom = function(strength, label) {
        currentSettings.bloomStrength = strength;
        currentSettings.preset = 'custom';
        saveSettings();
        window.applyAllSettings();
        updateSettingsUI();
      };

      window.setChromaticAberration = function(val, label) {
        currentSettings.chromaticAberration = val;
        currentSettings.preset = 'custom';
        saveSettings();
        window.applyAllSettings();
        updateSettingsUI();
      };

      window.setAnisotropy = function(val) {
        currentSettings.anisotropy = val;
        currentSettings.preset = 'custom';
        saveSettings();
        window.applyAllSettings();
        updateSettingsUI();
      };

      window.toggleFpsCounter = function(enable) {
        currentSettings.showFps = enable;
        saveSettings();
        updateSettingsUI();
      };

      window.setMouseSensitivity = function(multiplier, label) {
        currentSettings.mouseSens = multiplier;
        window.gameMouseSensMultiplier = multiplier;
        saveSettings();
        updateSettingsUI();
      };

      window.setInvertPitch = function(invert) {
        currentSettings.invertY = invert;
        window.gameInvertY = invert;
        saveSettings();
        updateSettingsUI();
      };

      window.setAudioMuted = function(isMuted) {
        currentSettings.audioMuted = isMuted;
        saveSettings();
        window.applyAllSettings();
        updateSettingsUI();
      };

      window.setMasterVolume = function(val) {
        currentSettings.masterVolume = parseInt(val, 10);
        saveSettings();
        window.applyAllSettings();
        updateSettingsUI();
      };

      window.toggleFullscreen = function() {
        if (!document.fullscreenElement) {
          document.documentElement.requestFullscreen().catch(() => {});
        } else {
          document.exitFullscreen().catch(() => {});
        }
      };

      // APPLY SETTINGS TO THREE.JS ENGINE
      window.applyAllSettings = function() {
        const app = window._app;
        if (!app) return;

        // 1. Resolution / Pixel Ratio
        if (app.renderer) {
          try {
            app.maxRenderPixelRatio = currentSettings.renderScale;
            app.renderer.setPixelRatio(currentSettings.renderScale);
            app.renderer.setSize(window.innerWidth, window.innerHeight);
          } catch(e) {}
        }

        // 2. Shadows
        if (app.renderer && app.renderer.shadowMap) {
          try {
            if (currentSettings.shadowQuality === 'off') {
              app.renderer.shadowMap.enabled = false;
            } else {
              app.renderer.shadowMap.enabled = true;
              const size = currentSettings.shadowQuality === 'low' ? 512 : (currentSettings.shadowQuality === 'med' ? 1024 : 2048);
              if (app.world && app.world.scene) {
                app.world.scene.traverse(node => {
                  if (node.isDirectionalLight && node.shadow) {
                    node.shadow.mapSize.set(size, size);
                    if (node.shadow.map) {
                      node.shadow.map.dispose();
                      node.shadow.map = null;
                    }
                  }
                });
              }
            }
            app.renderer.shadowMap.needsUpdate = true;
          } catch(e) {}
        }

        // 3. Bloom
        if (app.bloomPass) {
          try {
            app.bloomPass.strength = currentSettings.bloomStrength;
          } catch(e) {}
        }

        // 4. Chromatic Aberration
        if (app.chromaticAberrationIntensity) {
          try {
            app.chromaticAberrationIntensity.value = currentSettings.chromaticAberration;
          } catch(e) {}
        }

        // 5. Anisotropic Filtering
        if (app.world && app.world.scene) {
          try {
            app.world.scene.traverse(node => {
              if (node.material) {
                const mats = Array.isArray(node.material) ? node.material : [node.material];
                mats.forEach(m => {
                  ['map', 'normalMap', 'roughnessMap', 'metalnessMap', 'aoMap'].forEach(k => {
                    if (m[k] && m[k].anisotropy !== undefined) {
                      m[k].anisotropy = currentSettings.anisotropy;
                      m[k].needsUpdate = true;
                    }
                  });
                });
              }
            });
          } catch(e) {}
        }

        // 6. Audio
        if (app.world && app.world.audio && app.world.audio.masterGain) {
          try {
            if (window.isGameMenuOpen) {
              app.world.audio.masterGain.gain.setValueAtTime(0.05, 0);
            } else {
              const vol = currentSettings.audioMuted ? 0 : (currentSettings.masterVolume / 100);
              app.world.audio.masterGain.gain.setValueAtTime(vol, 0);
            }
          } catch(e) {}
        }

        // 7. Controls
        window.gameMouseSensMultiplier = currentSettings.mouseSens;
        window.gameInvertY = currentSettings.invertY;
      };

      function updateSettingsUI() {
        // Preset cards
        ['low', 'med', 'high', 'ultra'].forEach(p => {
          const el = document.getElementById('preset-' + p);
          if (el) el.classList.toggle('active', currentSettings.preset === p);
        });
        const txtPreset = document.getElementById('txt-preset-val');
        if (txtPreset) txtPreset.textContent = currentSettings.preset.toUpperCase();

        // Scale
        const scaleMap = { 0.75: 'btn-scale-75', 1.0: 'btn-scale-100', 1.25: 'btn-scale-125', 1.5: 'btn-scale-150' };
        Object.entries(scaleMap).forEach(([k, id]) => {
          const btn = document.getElementById(id);
          if (btn) btn.classList.toggle('active', Math.abs(currentSettings.renderScale - parseFloat(k)) < 0.05);
        });
        const txtScale = document.getElementById('txt-scale-val');
        if (txtScale) txtScale.textContent = currentSettings.renderScale + 'x';

        // Shadows
        ['off', 'low', 'med', 'ultra'].forEach(q => {
          const btn = document.getElementById('btn-shadow-' + q);
          if (btn) btn.classList.toggle('active', currentSettings.shadowQuality === q);
        });
        const txtShadow = document.getElementById('txt-shadow-val');
        if (txtShadow) txtShadow.textContent = currentSettings.shadowQuality.toUpperCase();

        // Bloom
        const bloomMap = { 0.0: 'btn-bloom-off', 0.3: 'btn-bloom-subtle', 0.6: 'btn-bloom-vibrant', 0.9: 'btn-bloom-cinematic' };
        Object.entries(bloomMap).forEach(([k, id]) => {
          const btn = document.getElementById(id);
          if (btn) btn.classList.toggle('active', Math.abs(currentSettings.bloomStrength - parseFloat(k)) < 0.1);
        });
        const txtBloom = document.getElementById('txt-bloom-val');
        if (txtBloom) txtBloom.textContent = currentSettings.bloomStrength > 0 ? (currentSettings.bloomStrength + '') : 'OFF';

        // Chroma
        const chromaMap = { 0.0: 'btn-chroma-off', 0.0015: 'btn-chroma-mild', 0.0028: 'btn-chroma-intense' };
        Object.entries(chromaMap).forEach(([k, id]) => {
          const btn = document.getElementById(id);
          if (btn) btn.classList.toggle('active', Math.abs(currentSettings.chromaticAberration - parseFloat(k)) < 0.0005);
        });
        const txtChroma = document.getElementById('txt-chroma-val');
        if (txtChroma) txtChroma.textContent = currentSettings.chromaticAberration > 0 ? 'MILD' : 'DISABLED';

        // Anisotropy
        [2, 4, 8, 16].forEach(a => {
          const btn = document.getElementById('btn-aniso-' + a);
          if (btn) btn.classList.toggle('active', currentSettings.anisotropy === a);
        });
        const txtAniso = document.getElementById('txt-aniso-val');
        if (txtAniso) txtAniso.textContent = currentSettings.anisotropy + 'x';

        // FPS Badge
        const fpsBadge = document.getElementById('live-fps-badge');
        if (fpsBadge) fpsBadge.style.display = currentSettings.showFps ? 'inline-flex' : 'none';
        const btnFpsOn = document.getElementById('btn-fps-on');
        const btnFpsOff = document.getElementById('btn-fps-off');
        if (btnFpsOn) btnFpsOn.classList.toggle('active', currentSettings.showFps);
        if (btnFpsOff) btnFpsOff.classList.toggle('active', !currentSettings.showFps);
        const txtFps = document.getElementById('txt-fps-val');
        if (txtFps) txtFps.textContent = currentSettings.showFps ? 'ENABLED' : 'HIDDEN';

        // Sensitivity
        const sensMap = { 0.5: 'btn-sens-50', 1.0: 'btn-sens-100', 1.5: 'btn-sens-150', 2.0: 'btn-sens-200' };
        Object.entries(sensMap).forEach(([k, id]) => {
          const btn = document.getElementById(id);
          if (btn) btn.classList.toggle('active', Math.abs(currentSettings.mouseSens - parseFloat(k)) < 0.1);
        });
        const txtSens = document.getElementById('txt-sens-val');
        if (txtSens) txtSens.textContent = currentSettings.mouseSens + 'x';

        // Invert Y
        const btnInvOff = document.getElementById('btn-invert-off');
        const btnInvOn = document.getElementById('btn-invert-on');
        if (btnInvOff) btnInvOff.classList.toggle('active', !currentSettings.invertY);
        if (btnInvOn) btnInvOn.classList.toggle('active', currentSettings.invertY);
        const txtInv = document.getElementById('txt-invert-val');
        if (txtInv) txtInv.textContent = currentSettings.invertY ? 'INVERTED (ON)' : 'NORMAL (OFF)';

        // Audio
        const btnAudOn = document.getElementById('btn-audio-on');
        const btnAudOff = document.getElementById('btn-audio-off');
        if (btnAudOn) btnAudOn.classList.toggle('active', !currentSettings.audioMuted);
        if (btnAudOff) btnAudOff.classList.toggle('active', currentSettings.audioMuted);
        const optTxtAud = document.getElementById('opt-txt-audio');
        if (optTxtAud) optTxtAud.textContent = currentSettings.audioMuted ? 'MUTED' : 'ENABLED';
        const sliderVol = document.getElementById('slider-volume');
        if (sliderVol) sliderVol.value = currentSettings.masterVolume;
        const txtVol = document.getElementById('txt-vol-val');
        if (txtVol) txtVol.textContent = currentSettings.masterVolume + '%';
      }

      // Live FPS Counter Loop
      let _fpsFrameCount = 0, _fpsLastTime = performance.now();
      function runFpsMonitorLoop() {
        requestAnimationFrame(runFpsMonitorLoop);
        _fpsFrameCount++;
        const now = performance.now();
        if (now - _fpsLastTime >= 400) {
          const fps = Math.round((_fpsFrameCount * 1000) / (now - _fpsLastTime));
          const el = document.getElementById('live-fps-val');
          if (el) el.textContent = fps;
          _fpsFrameCount = 0;
          _fpsLastTime = now;
        }
      }
      requestAnimationFrame(runFpsMonitorLoop);

      // Initialize UI state
      setTimeout(updateSettingsUI, 50);
"""

if pos_script != -1:
    pos_script_end = html.find('</script>', pos_script)
    html = html[:pos_script] + new_script_code + "\n    " + html[pos_script_end:]
    print("Replaced script handlers with complete Settings Architecture")

# Save updated HTML
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved updated index.html successfully!")
