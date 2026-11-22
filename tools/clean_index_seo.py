with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re

# Replace twitter creator and og preview alt
c = c.replace('@longhoang_lyo', '@wwtanks_game')
c = c.replace('Long Hoang Interactive 3D Portfolio Preview', 'World War Tanks 3D Combat Simulator Preview')

# Find <section class="u-visually-hidden" aria-label="Portfolio Summary and Index"> ... </section>
pattern = re.compile(r'<section class="u-visually-hidden" aria-label="Portfolio Summary and Index">.*?</section>\s*</section>', re.DOTALL)
match = pattern.search(c)
if not match:
    pattern = re.compile(r'<section class="u-visually-hidden" aria-label="Portfolio Summary and Index">.*?</section>', re.DOTALL)
    match = pattern.search(c)

if match:
    old_seo = match.group(0)
    print("Found old seo summary (len: %d)" % len(old_seo))
    
    new_seo = '''<section class="u-visually-hidden" aria-label="Game Overview and Field Manual">
        <header>
          <h2>World War Tanks: 3D Armored Warfare</h2>
          <p>
            Command heavy armor in an authentic 3D World War tank simulator. Featuring realistic track dynamics, neutral pivot steering, independent turret traverse, ballistic cannon trajectories, and tactical battlefield destruction.
          </p>
        </header>
        <section aria-label="Armored Combat Systems">
          <h3>Combat Specifications</h3>
          <ul>
            <li><strong>Chassis:</strong> Heavy Combat Track System with dual-sprocket independent track physics</li>
            <li><strong>Main Armament:</strong> 88mm KwK High-Velocity Cannon with APCR and HE shell complement</li>
            <li><strong>Turret Drive:</strong> 360-degree precision hydraulic turret with gyroscopic stabilization</li>
            <li><strong>Controls:</strong> WASD track steering, Mouse turret look & aim, Left Click / Space to fire</li>
          </ul>
        </section>
        <section aria-label="Combat Sectors">
          <h3>Combat Operations</h3>
          <p>
            Navigate hazardous industrial conflict zones, engage hostile armor detachments, eliminate enemy fortifications, and secure allied supply depots across open battlegrounds.
          </p>
        </section>
      </section>'''
    c = c[:match.start()] + new_seo + c[match.end():]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("SUCCESS: index.html SEO and metadata sanitized to pure tank game!")
else:
    print("WARNING: Portfolio Summary section not found in index.html")
