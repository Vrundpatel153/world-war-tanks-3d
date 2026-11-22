with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re

# Remove any remaining sections inside main with About, Contact, or Core Technology Stack
c = re.sub(r'<section[^>]*aria-label="About".*?</section>', '', c, flags=re.DOTALL)
c = re.sub(r'<section[^>]*aria-label="Contact".*?</section>', '', c, flags=re.DOTALL)
c = re.sub(r'<section[^>]*aria-label="Core Technology Stack[^"]*".*?</section>', '', c, flags=re.DOTALL)

# Also check for any remaining emails or portfolio names
c = c.replace('longhoang.0816@gmail.com', 'operations@wwtanks3d.internal')
c = c.replace('Product designer and developer with nearly 5 years in EdTech and smart home, one failed startup alongside incredible people, and a fresh commitment to breaking out of my comfort zone to push interactive 3D WebGL experiences.', 'World War Tanks 3D is a tactical tank combat simulator featuring realistic track physics, neutral pivot steering, independent turret traverse, and open battlefield exploration.')
c = c.replace("Crafting high-performance digital experiences utilizing Three.js, WebGPU, Rapier physics, GSAP, TSL shaders, and semantic accessible web standards.", "Engineered with Three.js, Rapier 3D physics, procedural track dynamics, and WebGL rendering.")

# Also add CSS to fully hide .startup-intro once dismisses
css_fix = """
    /* Ensure intro briefing completely disappears after dismiss */
    body:not(.intro-overlay-active) .startup-intro,
    .startup-intro--dismissed {
      display: none !important;
      opacity: 0 !important;
      pointer-events: none !important;
      visibility: hidden !important;
    }
"""

if '/* Custom Tactical Combat HUD */' in c:
    c = c.replace('/* Custom Tactical Combat HUD */', css_fix + '\n    /* Custom Tactical Combat HUD */')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("SUCCESS: Cleaned remaining portfolio artifacts from index.html")
