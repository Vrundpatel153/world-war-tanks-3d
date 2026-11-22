import re

# 1. Update index.html
path_html = "C:/Users/Vrund Patel/Desktop/clone-game/index.html"
with open(path_html, 'r', encoding='utf-8') as f:
    html = f.read()

# Fix cursor CSS: Replace cursor: none !important with authentic SVG hardware cursors
old_cursor_css = """    body.in-menu-mode,
    body.in-menu-mode *,
    body.in-menu-mode button,
    body.in-menu-mode a,
    body.in-menu-mode input {
      cursor: none !important;
    }"""

svg_default = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 28 28'%3E%3Cpolygon points='1,1 1,22 7,16 11,26 15,24 11,15 19,15' fill='%23c7ff72' stroke='%23000' stroke-width='1.5' stroke-linejoin='round' filter='drop-shadow(0 2px 4px rgba(0,0,0,0.8))'/%3E%3Cpolygon points='3,4 3,17 7,13 10,21 12,20 9,13 15,13' fill='%2300ffaa' opacity='0.7'/%3E%3Ccircle cx='2' cy='2' r='1.5' fill='%23ffffff'/%3E%3C/svg%3E"
svg_pointer = "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='28' height='28' viewBox='0 0 28 28'%3E%3Cpolygon points='1,1 1,22 7,16 11,26 15,24 11,15 19,15' fill='%2300ffaa' stroke='%23000' stroke-width='1.5' stroke-linejoin='round' filter='drop-shadow(0 2px 4px rgba(0,0,0,0.8))'/%3E%3Cpolygon points='3,4 3,17 7,13 10,21 12,20 9,13 15,13' fill='%23ffffff' opacity='0.8'/%3E%3Ccircle cx='2' cy='2' r='1.5' fill='%23ffffff'/%3E%3C/svg%3E"

new_cursor_css = f"""    /* AUTHENTIC HARDWARE-ACCELERATED IN-GAME TACTICAL CURSOR */
    body.in-menu-mode,
    body.in-menu-mode * {{
      cursor: url("{svg_default}") 1 1, default !important;
    }}

    body.in-menu-mode button,
    body.in-menu-mode a,
    body.in-menu-mode input,
    body.in-menu-mode select,
    body.in-menu-mode .btn-deck-deploy,
    body.in-menu-mode .btn-deck-action,
    body.in-menu-mode .preset-card,
    body.in-menu-mode .settings-tab-btn,
    body.in-menu-mode .opt-btn,
    body.in-menu-mode .menu-modal-close,
    body.in-menu-mode [role="button"] {{
      cursor: url("{svg_pointer}") 1 1, pointer !important;
    }}"""

if old_cursor_css in html:
    html = html.replace(old_cursor_css, new_cursor_css)
    print("Replaced cursor: none with hardware SVG cursor CSS")
else:
    print("Warning: old_cursor_css not found")

# Fix pointerdown lock trap on line 1849
old_pointerdown = """      // Canvas click lock for seamless PC mouse look
      window.addEventListener('pointerdown', function (e) {
        if (!e.target || e.target.closest('button, a, input, textarea, select')) return;
        const canvas = document.querySelector('canvas');
        if (canvas && document.pointerLockElement !== canvas) {
          canvas.requestPointerLock?.();
        }
      });"""

new_pointerdown = """      // Strict Canvas click lock for seamless PC mouse look (DISABLED IN MENUS)
      window.addEventListener('pointerdown', function (e) {
        if (window.isGameMenuOpen) return;
        if (!e.target || e.target.closest('button, a, input, textarea, select, .game-home-screen, .menu-modal-overlay, .game-command-deck, .tactical-spec-card')) return;
        const canvas = document.querySelector('canvas');
        if (canvas && document.pointerLockElement !== canvas) {
          canvas.requestPointerLock?.();
        }
      }, true);

      // Failsafe: Automatically release pointerLock if engaged while menu is open
      document.addEventListener('pointerlockchange', function () {
        if (window.isGameMenuOpen && document.pointerLockElement) {
          try { document.exitPointerLock?.(); } catch (err) {}
        }
      });"""

if old_pointerdown in html:
    html = html.replace(old_pointerdown, new_pointerdown)
    print("Fixed pointerdown lock trap in index.html")
else:
    print("Warning: old_pointerdown not found")

# Fix defaultSettings to Balanced 60 FPS
old_settings = """      const defaultSettings = {
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
      };"""

new_settings = """      const defaultSettings = {
        preset: 'med',
        renderScale: 1.0,
        shadowQuality: 'med',
        bloomStrength: 0.25,
        chromaticAberration: 0.0,
        anisotropy: 4,
        showFps: true,
        mouseSens: 1.0,
        invertY: false,
        audioMuted: false,
        masterVolume: 100
      };"""

if old_settings in html:
    html = html.replace(old_settings, new_settings)
    print("Updated defaultSettings to Balanced 60 FPS")
else:
    print("Warning: old_settings not found")

# Migrate old localStorage settings if preset was ultra
old_storage_load = """      let currentSettings = { ...defaultSettings };
      try {
        const saved = localStorage.getItem(SETTINGS_STORAGE_KEY);
        if (saved) {
          currentSettings = { ...defaultSettings, ...JSON.parse(saved) };
        }
      } catch(e) {}"""

new_storage_load = """      let currentSettings = { ...defaultSettings };
      try {
        const saved = localStorage.getItem(SETTINGS_STORAGE_KEY);
        if (saved) {
          const parsed = JSON.parse(saved);
          if (parsed && parsed.preset === 'ultra') {
            // Upgrade legacy lagging ultra to 60 FPS balanced preset
            currentSettings = { ...defaultSettings };
            localStorage.setItem(SETTINGS_STORAGE_KEY, JSON.stringify(currentSettings));
          } else {
            currentSettings = { ...defaultSettings, ...parsed };
          }
        }
      } catch(e) {}"""

if old_storage_load in html:
    html = html.replace(old_storage_load, new_storage_load)
    print("Updated storage loading with 60 FPS migration")
else:
    print("Warning: old_storage_load not found")

# Hide DOM tactical cursor div by default so it doesn't leave an unmoving green arrow at 50vw,50vh
old_cursor_style = """    #tactical-cursor {
      position: fixed;
      top: 0;
      left: 0;
      pointer-events: none;
      z-index: 99999999;
      display: none;
      transform: translate3d(50vw, 50vh, 0);
      will-change: transform;
      user-select: none;
    }"""

new_cursor_style = """    #tactical-cursor {
      position: fixed;
      top: 0;
      left: 0;
      pointer-events: none;
      z-index: 99999999;
      display: none;
      opacity: 0;
      transform: translate3d(-100px, -100px, 0);
      will-change: transform;
      user-select: none;
      transition: opacity 0.15s ease;
    }

    body.in-menu-mode #tactical-cursor.cursor-active {
      display: block;
      opacity: 1;
    }"""

if old_cursor_style in html:
    html = html.replace(old_cursor_style, new_cursor_style)
    print("Updated #tactical-cursor styling to prevent static arrow")
else:
    print("Warning: old_cursor_style not found")

# Update cursor mousemove listener
old_cursor_listener = """      const _tacticalCursor = document.getElementById('tactical-cursor');
      if (_tacticalCursor) {
        window.addEventListener('mousemove', function(e) {
          _tacticalCursor.style.transform = `translate3d(${e.clientX}px, ${e.clientY}px, 0)`;
        }, { passive: true });"""

new_cursor_listener = """      const _tacticalCursor = document.getElementById('tactical-cursor');
      if (_tacticalCursor) {
        window.addEventListener('mousemove', function(e) {
          _tacticalCursor.classList.add('cursor-active');
          _tacticalCursor.style.transform = `translate3d(${e.clientX}px, ${e.clientY}px, 0)`;
        }, { passive: true });"""

if old_cursor_listener in html:
    html = html.replace(old_cursor_listener, new_cursor_listener)
    print("Updated cursor mousemove listener")
else:
    print("Warning: old_cursor_listener not found")

# Cache busting meta tags in head
head_tag = "<head>"
cache_bust_meta = """<head>
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />"""

if head_tag in html and cache_bust_meta not in html:
    html = html.replace(head_tag, cache_bust_meta, 1)
    print("Added cache busting meta headers")

with open(path_html, 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html successfully updated!")
