import os
import re

print("Starting complete portfolio removal and game conversion...")

# 1. Update site.webmanifest
manifest_content = """{
  "name": "World War Tanks 3D: Armored Warfare",
  "short_name": "WW Tanks 3D",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0b0f15",
  "theme_color": "#00ffaa",
  "icons": [
    {
      "src": "/assets/elements/app-icon.svg",
      "sizes": "any",
      "type": "image/svg+xml"
    },
    {
      "src": "/assets/elements/icon-192.png",
      "sizes": "192x192",
      "type": "image/png"
    },
    {
      "src": "/assets/elements/icon-512.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
"""
with open("site.webmanifest", "w", encoding="utf-8") as f:
    f.write(manifest_content)
print("Updated site.webmanifest!")

# 2. Update assets/elements/hud/title-intro.svg with military title
title_svg = """<svg width="569" height="213" viewBox="0 0 569 213" fill="none" xmlns="http://www.w3.org/2000/svg">
  <g id="ww_tanks_title">
    <rect x="10" y="20" width="549" height="173" rx="12" fill="#0c1118" fill-opacity="0.9" stroke="#00ffaa" stroke-width="4"/>
    <text x="50%" y="90" text-anchor="middle" font-family="'Barlow', sans-serif" font-weight="900" font-size="52" fill="#00ffaa" letter-spacing="4">WORLD WAR TANKS</text>
    <text x="50%" y="140" text-anchor="middle" font-family="'Barlow', sans-serif" font-weight="800" font-size="24" fill="#ffffff" letter-spacing="8">3D ARMORED WARFARE</text>
    <line x1="60" y1="160" x2="509" y2="160" stroke="#00ffaa" stroke-width="2" stroke-dasharray="8 6"/>
  </g>
</svg>"""
with open("assets/elements/hud/title-intro.svg", "w", encoding="utf-8") as f:
    f.write(title_svg)
print("Updated title-intro.svg!")

# 3. Update assets/t1WzwXnd.js (intro text, banners, contact form, social links)
with open("assets/t1WzwXnd.js", "r", encoding="utf-8") as f:
    t1_code = f.read()

# Replace bodyText
old_body = "Think this was just an AI prompt, huh? Think again!<br />It was forged with 2300+ hours of love, late-night coffee, and way too many pixels. I poured everything into making this fun and memorable—so come on in and enjoy the ride!"
new_body = "Commander, armored reconnaissance forces have established a combat perimeter in Sector 04.<br />Engage hostile units, calibrate 88mm high-velocity ordnance, and secure strategic supply lines across the battlefield."
if old_body in t1_code:
    t1_code = t1_code.replace(old_body, new_body)
    print("Replaced intro briefing text in t1WzwXnd.js!")
else:
    print("Could not find exact old_body in t1WzwXnd.js")

# Replace notePrefix and noteSuffix
t1_code = t1_code.replace("notePrefix:`Short on time? Skip`", "notePrefix:``")
t1_code = t1_code.replace("noteSuffix:`for a quick preview of`", "noteSuffix:``")
t1_code = t1_code.replace("noteEmphasis:`my work`", "noteEmphasis:``")
t1_code = t1_code.replace("notePrefix:`Want to know more? Visit`", "notePrefix:``")
t1_code = t1_code.replace("noteSuffix:`and meet`", "noteSuffix:``")
t1_code = t1_code.replace("noteEmphasis:`the creator`", "noteEmphasis:``")

# Replace collab contact title
t1_code = t1_code.replace("title:`LET’S COLLAB`", "title:`TACTICAL SITREP`")
t1_code = t1_code.replace("location:`Nam Tu Liem, Ha Noi (GMT+7)`", "location:`Combat Sector Alpha`")
t1_code = t1_code.replace("email:`long.hh.0816@gmail.com`", "email:`hq@wwtanks3d.net`")
t1_code = t1_code.replace("defaultSubject:`[PORTFOLIO COLLAB]`", "defaultSubject:`[SITREP DISPATCH]`")
t1_code = t1_code.replace("defaultMessage:`Hi Long, I would like to collaborate on a project.`", "defaultMessage:`Sector secured. Awaiting next combat directive.`")

with open("assets/t1WzwXnd.js", "w", encoding="utf-8") as f:
    f.write(t1_code)
print("Updated t1WzwXnd.js!")

# 4. Update assets/B1Nq4Kq6.js (disable social boxes and statue action point)
with open("assets/B1Nq4Kq6.js", "r", encoding="utf-8") as f:
    b1_code = f.read()

# Disable social boxes init
if "this.socialBox&&this.socialBox.init(" in b1_code:
    b1_code = b1_code.replace("this.socialBox&&this.socialBox.init(", "// this.socialBox&&this.socialBox.init(")
    print("Disabled socialBox.init in B1Nq4Kq6.js!")

# Disable statue placeholder point
if "initStatuePlaceholderPoint(t){t&&Jt(" in b1_code:
    b1_code = b1_code.replace("initStatuePlaceholderPoint(t){t&&Jt(", "initStatuePlaceholderPoint(t){return;t&&Jt(")
    print("Disabled initStatuePlaceholderPoint in B1Nq4Kq6.js!")

with open("assets/B1Nq4Kq6.js", "w", encoding="utf-8") as f:
    f.write(b1_code)
print("Updated B1Nq4Kq6.js!")

# 5. Overwrite all sub-routes with redirects to root game
redirect_html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8" />
  <meta http-equiv="refresh" content="0; url=/" />
  <title>World War Tanks 3D</title>
  <script>window.location.replace("/");</script>
</head>
<body style="background: #0c1118; color: #00ffaa; font-family: sans-serif; text-align: center; padding-top: 20vh;">
  <h2>Redirecting to World War Tanks 3D...</h2>
  <p><a href="/" style="color: #00ffaa;">Click here if not redirected automatically</a></p>
</body>
</html>
"""

subroutes = [
    "about.html", "contact.html", "about/index.html", "contact/index.html",
    "work/index.html", "work/hanzii.html", "work/mazii.html", "work/todaii.html", "work/niubii.html",
    "work/hanzii/index.html", "work/mazii/index.html", "work/todaii/index.html", "work/niubii/index.html"
]

for sr in subroutes:
    d = os.path.dirname(sr)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(sr, "w", encoding="utf-8") as f:
        f.write(redirect_html)

print("Updated all subroutes with redirects to root game!")

# 6. Rewrite index.html metadata, title, schema, and semantic tags
with open("index.html", "r", encoding="utf-8") as f:
    index_html = f.read()

# Replace title
index_html = re.sub(r'<title>.*?</title>', '<title>World War Tanks: 3D Armored Warfare</title>', index_html)

# Replace author and description
index_html = re.sub(r'<meta name="author" content=".*?" />', '<meta name="author" content="WW Tanks Team" />', index_html)
index_html = re.sub(r'<meta name="description" content=".*?" />', '<meta name="description" content="World War Tanks 3D is an immersive armored warfare combat simulator featuring realistic track physics, 360-degree turret aiming, and open-world tactical exploration." />', index_html)
index_html = re.sub(r'<meta name="keywords" content=".*?" />', '<meta name="keywords" content="Tank Game, World War Tanks, Armored Warfare, Three.js, WebGL, 3D Game, Tank Simulator" />', index_html)

# Replace OpenGraph
index_html = re.sub(r'<meta property="og:title" content=".*?" />', '<meta property="og:title" content="World War Tanks: 3D Armored Warfare" />', index_html)
index_html = re.sub(r'<meta property="og:description" content=".*?" />', '<meta property="og:description" content="Immersive 3D armored combat simulator with realistic physics." />', index_html)
index_html = re.sub(r'<meta property="og:site_name" content=".*?" />', '<meta property="og:site_name" content="World War Tanks 3D" />', index_html)

# Replace Twitter
index_html = re.sub(r'<meta name="twitter:title" content=".*?" />', '<meta name="twitter:title" content="World War Tanks: 3D Armored Warfare" />', index_html)
index_html = re.sub(r'<meta name="twitter:description" content=".*?" />', '<meta name="twitter:description" content="Immersive 3D armored combat simulator with realistic physics." />', index_html)

# Replace JSON-LD schema with VideoGame schema
game_schema = """<script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "VideoGame",
      "name": "World War Tanks 3D: Armored Warfare",
      "description": "Immersive 3D armored combat simulator with realistic track physics, independent turret traversal, and open-world tactical gameplay.",
      "genre": ["Action", "Simulation", "Vehicle Combat"],
      "gamePlatform": ["Web Browser", "PC"]
    }
    </script>"""
index_html = re.sub(r'<script type="application/ld\+json">.*?</script>', game_schema, index_html, flags=re.DOTALL)

# Replace aria-label="LYOOO PORTFOLIO"
index_html = index_html.replace('aria-label="LYOOO PORTFOLIO"', 'aria-label="WORLD WAR TANKS 3D"')
index_html = index_html.replace('role="main" aria-label="3D Interactive Portfolio Application"', 'role="main" aria-label="World War Tanks 3D Game"')
index_html = index_html.replace('<h1 class="u-visually-hidden">Long Hoang (Lyo) – Designer & Developer</h1>', '<h1 class="u-visually-hidden">World War Tanks: 3D Armored Warfare</h1>')

# Replace semantic hidden section
game_manual = """<section class="u-visually-hidden" aria-label="Game Field Manual and Combat Controls">
        <header>
          <h2>World War Tanks 3D: Tactical Field Manual</h2>
          <p>Tactical armored warfare combat simulator built with Three.js WebGL and Rapier 3D physics.</p>
        </header>
        <section aria-label="Controls">
          <h3>Combat Controls</h3>
          <ul>
            <li><strong>W / S:</strong> Drive tracks forward / Reverse along tank hull</li>
            <li><strong>A / D:</strong> Neutral track pivot steering left / right</li>
            <li><strong>Mouse:</strong> 360-degree turret aim and camera orbit</li>
            <li><strong>Space / Left-Click:</strong> Fire 88mm main cannon</li>
            <li><strong>Shift:</strong> Engine overdrive boost</li>
            <li><strong>Mouse Wheel:</strong> Tactical zoom</li>
          </ul>
        </section>
      </section>"""
index_html = re.sub(r'<section class="u-visually-hidden" aria-label="Portfolio Summary and Index">.*?</section>\s*</section>', game_manual, index_html, flags=re.DOTALL)

# Replace noscript
noscript_game = """<noscript>
      <div style="padding: 2rem; color: #ffffff; background: #0c1118; font-family: sans-serif; max-width: 800px; margin: 0 auto;">
        <h1>World War Tanks: 3D Armored Warfare</h1>
        <p>A WebGL-enabled browser is required to play World War Tanks 3D.</p>
        <h2>Combat Controls</h2>
        <ul>
          <li><strong>W / S:</strong> Hull Treads Forward / Reverse</li>
          <li><strong>A / D:</strong> Neutral Pivot Steering Left / Right</li>
          <li><strong>Mouse:</strong> Turret Traverse & Camera Orbit</li>
          <li><strong>Space / Click:</strong> Fire Main Cannon</li>
          <li><strong>Shift:</strong> Boost Overdrive</li>
        </ul>
      </div>
    </noscript>"""
index_html = re.sub(r'<noscript>.*?</noscript>', noscript_game, index_html, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)
print("Updated index.html metadata, title, schema, and semantic tags!")

print("=== PORTFOLIO PURGE AND GAME TRANSFORMATION COMPLETE ===")
