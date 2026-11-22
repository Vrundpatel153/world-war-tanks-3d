with open("C:/Users/Vrund Patel/Desktop/clone-game/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update CSS to hide all storytelling/portfolio/tutorial elements
css_to_add = """      /* Completely eliminate all storytelling, case-study, tutorial, and portfolio elements */
      .tutorial-card,
      .tutorial-layer,
      #tutorial-layer,
      .action-point,
      .action-point-layer,
      .case-study-page,
      .case-study-page__images-column,
      .case-study-page__sidebar,
      .case-study-page__toc-bg,
      .case-study-page__toc-surface,
      .about-page,
      .statue-page,
      .hanzii-page,
      .touch-map-button,
      .grab-mode-bottom-hud,
      .grab-mode-pill,
      .email-popup,
      .submit-item-popup {
        display: none !important;
        opacity: 0 !important;
        visibility: hidden !important;
        pointer-events: none !important;
      }
"""

old_hide = """      #aim-circle .aim-kill,
      #aim-circle .aim-kill-part,
      #aim-circle .aim-grab-mode-wrapper,
      .tank-crosshair {
        display: none !important;
      }"""

new_hide = old_hide + "\n\n" + css_to_add

if old_hide in html:
    html = html.replace(old_hide, new_hide)
    print("index.html CSS updated successfully")
else:
    print("WARNING: old_hide not found")

# Update bottom bar controls text
old_bar = """      <div class="tank-controls-bar">
        <span>WASD</span> DRIVE (GTA CAR) &middot; <span>HOLD R-CLICK</span> AIM &amp; ZOOM &middot; <span>PRESS SCROLL</span> LOCK AIM &middot; <span>SCROLL</span> ZOOM IN/OUT &middot; <span>L-CLICK</span> FIRE
      </div>"""

new_bar = """      <div class="tank-controls-bar">
        <span>WASD</span> TANK TREADS &middot; <span>MOUSE</span> 360° LOOK &amp; TURRET AIM &middot; <span>CLICK CANVAS</span> LOCK CURSOR &middot; <span>HOLD R-CLICK</span> ZOOM &middot; <span>PRESS SCROLL</span> LOCK AIM &middot; <span>L-CLICK</span> FIRE CANNON
      </div>"""

if old_bar in html:
    html = html.replace(old_bar, new_bar)
    print("tank-controls-bar updated successfully")
else:
    print("WARNING: old_bar not found")

# Canvas click handler to request pointer lock
old_click = """        // Canvas click lock for seamless Zelda camera look
        window.addEventListener('click', function(e) {
          if (!e.target || e.target.closest('button, a, input, textarea')) return;
          const canvas = document.querySelector('canvas');
          if (canvas && document.pointerLockElement !== canvas) {
            canvas.requestPointerLock?.();
          }
        });"""

new_click = """        // Canvas click lock for seamless PC mouse look
        window.addEventListener('pointerdown', function(e) {
          if (!e.target || e.target.closest('button, a, input, textarea, select')) return;
          const canvas = document.querySelector('canvas');
          if (canvas && document.pointerLockElement !== canvas) {
            canvas.requestPointerLock?.();
          }
        });"""

if old_click in html:
    html = html.replace(old_click, new_click)
    print("click handler updated successfully")

with open("C:/Users/Vrund Patel/Desktop/clone-game/index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("index.html saved.")
