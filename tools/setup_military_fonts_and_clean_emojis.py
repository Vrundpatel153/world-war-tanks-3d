import re
import os

html_path = r'C:\Users\Vrund Patel\Desktop\clone-game\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

print("=== 1. ADDING MILITARY / TACTICAL GOOGLE FONTS (Rajdhani, Barlow Condensed, Inter) ===")

google_fonts_link = """  <!-- Military & Tactical AAA Game Typography (Rajdhani, Barlow Condensed, Inter) -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:ital,wght@0,600;0,700;0,800;0,900;1,700&family=Rajdhani:wght@600;700;800&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
"""

if 'family=Rajdhani' not in html:
    pos_head = html.find('</head>')
    if pos_head != -1:
        html = html[:pos_head] + google_fonts_link + html[pos_head:]
        print("Added Google Fonts links for Rajdhani, Barlow Condensed, and Inter")

print("\n=== 2. REPLACING UGLY CARTOON FONT (Crocante) WITH SHARP TACTICAL FONTS ===")

# Replace Crocante references in styles
html = re.sub(
    r'font-family:\s*["\']Crocante["\'](?:\s*,\s*display)?\s*,\s*sans-serif(?:\s*!important)?;',
    'font-family: "Rajdhani", "Barlow Condensed", "Trebuchet MS", sans-serif !important; letter-spacing: 0.08em; text-transform: uppercase;',
    html
)

# Update .home-title styling specifically for aggressive AAA game look
html = html.replace(
    '.home-title {\n      font-family: "Rajdhani", "Barlow Condensed", "Trebuchet MS", sans-serif !important;',
    '.home-title {\n      font-family: "Rajdhani", "Barlow Condensed", "Trebuchet MS", sans-serif !important;\n      font-weight: 800;\n      letter-spacing: 0.12em;\n      text-transform: uppercase;'
)

# Update .btn-home-play
html = html.replace(
    '.btn-home-play {\n      width: 100%;\n      padding: 18px 28px;\n      background: #c7ff72;\n      color: #11121a;\n      border: 3px solid #11121a;\n      border-radius: 8px;',
    '.btn-home-play {\n      width: 100%;\n      padding: 16px 28px;\n      background: #c7ff72;\n      color: #11121a;\n      border: 2px solid #c7ff72;\n      border-radius: 6px;\n      font-family: "Rajdhani", "Barlow Condensed", sans-serif !important;\n      font-weight: 800;\n      font-size: 22px;\n      letter-spacing: 0.14em;\n      text-transform: uppercase;'
)

# Update .btn-home-secondary
html = html.replace(
    '.btn-home-secondary {\n      width: 100%;\n      padding: 14px 20px;\n      background: #191b24;\n      color: #dfdfe2;\n      border: 1px solid #272935;\n      border-radius: 8px;\n      font-family: "Barlow", sans-serif;',
    '.btn-home-secondary {\n      width: 100%;\n      padding: 13px 20px;\n      background: #191b24;\n      color: #dfdfe2;\n      border: 1px solid #272935;\n      border-radius: 6px;\n      font-family: "Rajdhani", "Barlow Condensed", sans-serif;\n      font-size: 14px;\n      font-weight: 700;\n      letter-spacing: 0.1em;\n      text-transform: uppercase;'
)

# Update .settings-tab-btn
html = html.replace(
    'font-family: "Barlow", sans-serif;\n      font-size: 11px;\n      font-weight: 800;',
    'font-family: "Rajdhani", "Barlow Condensed", sans-serif;\n      font-size: 13px;\n      font-weight: 700;\n      letter-spacing: 0.08em;'
)

# Update setting-title and opt-btn
html = html.replace(
    '.setting-title {\n      font-family: "Barlow", sans-serif;\n      font-size: 13px;\n      font-weight: 800;\n      letter-spacing: 0.06em;',
    '.setting-title {\n      font-family: "Rajdhani", "Barlow Condensed", sans-serif;\n      font-size: 14px;\n      font-weight: 700;\n      letter-spacing: 0.08em;'
)

html = html.replace(
    '.opt-btn {\n      padding: 6px 14px;\n      background: #191b24;\n      border: 1px solid #272935;\n      color: #8f93a5;\n      border-radius: 6px;\n      font-family: "Barlow", sans-serif;\n      font-size: 11px;\n      font-weight: 800;\n      letter-spacing: 0.08em;',
    '.opt-btn {\n      padding: 7px 14px;\n      background: #191b24;\n      border: 1px solid #272935;\n      color: #8f93a5;\n      border-radius: 6px;\n      font-family: "Rajdhani", "Barlow Condensed", sans-serif;\n      font-size: 12px;\n      font-weight: 700;\n      letter-spacing: 0.08em;'
)

# Update preset card name
html = html.replace(
    '.preset-name {\n      font-family: "Rajdhani", "Barlow Condensed", "Trebuchet MS", sans-serif !important; letter-spacing: 0.08em; text-transform: uppercase;\n      font-size: 14px;\n      font-weight: 900;',
    '.preset-name {\n      font-family: "Rajdhani", "Barlow Condensed", sans-serif !important;\n      font-size: 16px;\n      font-weight: 800;\n      letter-spacing: 0.1em;\n      text-transform: uppercase;'
)

print("Updated typography to military tactical font stack")


print("\n=== 3. REMOVING ALL EMOJIS ACROSS HTML & JAVASCRIPT ===")

# List of exact emoji replacements
replacements = [
    # Top bar & HUD
    ('⚡ <span id="live-fps-val">60</span> FPS', 'FPS: <span id="live-fps-val">60</span>'),
    ('⚡ <span id="opt-txt-perf">', '<span id="opt-txt-perf">'),
    ('⚡ 60 FPS', '60 FPS'),
    ('⚙ MENU [ESC]', 'MENU [ESC]'),
    ('⚙ PAUSE', 'PAUSE'),
    ('<span style="color: #c7ff72; font-size: 20px;">⚙</span>', ''),

    # Home Screen buttons
    ('🎮 CONTROLS MANUAL', 'CONTROLS MANUAL'),
    ('⚙ OPTIONS &amp; SETTINGS', 'OPTIONS &amp; SETTINGS'),
    ('🔊 AUDIO: SFX ON', 'AUDIO: SFX ON'),
    ('🔇 AUDIO: SFX MUTED', 'AUDIO: SFX MUTED'),
    ('• ⏸️ COMBAT SIMULATION PAUSED •', '• COMBAT SIMULATION PAUSED •'),

    # Settings Tabs
    ('⚡ GRAPHICS &amp; VISUALS', 'GRAPHICS &amp; VISUALS'),
    ('🎮 CONTROLS &amp; CAMERA', 'CONTROLS &amp; CAMERA'),
    ('🔊 AUDIO', 'AUDIO'),
    ('🗺️ SECTOR INTEL', 'SECTOR INTEL'),

    # Settings Row Titles
    ('🔥 GRAPHICS PRESET (1-CLICK OPTIMIZATION)', 'GRAPHICS PRESET (OPTIMIZATION)'),
    ('🖥️ RENDER RESOLUTION SCALE (DPI)', 'RENDER RESOLUTION SCALE (DPI)'),
    ('🌓 REAL-TIME SHADOW MAPS', 'SHADOW QUALITY (DYNAMIC MAPS)'),
    ('✨ BLOOM &amp; HDR LIGHT GLOW', 'BLOOM &amp; LIGHT GLOW'),
    ('🎯 CHROMATIC LENS ABERRATION', 'CHROMATIC LENS ABERRATION'),
    ('🔍 ANISOTROPIC TEXTURE FILTERING', 'ANISOTROPIC TEXTURE FILTERING'),
    ('📊 LIVE IN-GAME FPS COUNTER', 'LIVE IN-GAME FPS COUNTER'),
    ('🖱️ MOUSE TURRET &amp; LOOK SENSITIVITY', 'MOUSE LOOK SENSITIVITY'),
    ('🔄 INVERT VERTICAL CAMERA (Y-AXIS)', 'INVERT VERTICAL LOOK (Y-AXIS)'),
    ('🖥️ DISPLAY MODE', 'DISPLAY MODE'),
    ('⛶ TOGGLE FULLSCREEN [F11]', 'TOGGLE FULLSCREEN [F11]'),
    ('⛶ TOGGLE FULLSCREEN', 'TOGGLE FULLSCREEN'),
    ('🔊 SOUND EFFECTS (SFX)', 'SOUND EFFECTS (SFX)'),
    ('🔊 SFX ENABLED', 'SFX ENABLED'),
    ('🔇 MUTED', 'SFX MUTED'),
    ('🎚️ MASTER AUDIO VOLUME', 'MASTER AUDIO VOLUME'),

    # In JS functions
    ("txtHome.textContent = _isAudioMuted ? '🔇 AUDIO: SFX MUTED' : '🔊 AUDIO: SFX ON';",
     "txtHome.textContent = _isAudioMuted ? 'AUDIO: SFX MUTED' : 'AUDIO: SFX ON';"),
    ("optTxt.textContent = _isAudioMuted ? '🔇 SFX: MUTED' : '🔊 SFX: ENABLED';",
     "optTxt.textContent = _isAudioMuted ? 'SFX: MUTED' : 'SFX: ENABLED';"),
    ("if (badge) badge.textContent = '• ⏸️ COMBAT SIMULATION PAUSED •';",
     "if (badge) badge.textContent = '• COMBAT SIMULATION PAUSED •';"),
]

for old, new in replacements:
    if old in html:
        html = html.replace(old, new)
        print(f"Replaced: '{old[:30]}' -> '{new[:30]}'")

# Check if any remaining emojis exist
emoji_pattern = re.compile(r'[\U00010000-\U0010ffff]|[\u2600-\u27bf]|[\u2300-\u23ff]|[\u2b50-\u2b55]|[\u3030\u303d\u3297\u3299]')
matches = emoji_pattern.findall(html)
if matches:
    print(f"Remaining emojis found in HTML: {set(matches)}")
    # Clean any remaining emojis
    for em in set(matches):
        html = html.replace(em, '')
    print("Stripped all remaining emojis!")
else:
    print("Zero emojis remaining! All clean.")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved updated index.html successfully!")
