with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# 1. Remove CSS block from #tactical-cursor to #tactical-cursor.clicking
css_start = html.find('    #tactical-cursor {\n')
css_end = html.find('/* =========================================================\n       CUSTOM TACTICAL IN-GAME CURSOR & SETTINGS SYSTEM')

if css_start != -1 and css_end != -1:
    html = html[:css_start] + html[css_end:]
    print("Purged #tactical-cursor CSS block successfully!")
else:
    print("Warning: css bounds not found", css_start, css_end)

# 2. Remove JS engine
js_start = html.find('      // PHYSICAL IN-GAME TACTICAL HARDWARE CURSOR ENGINE\n')
js_end = html.find('    </script>\n\n  <!-- Physical Hardware Tactical In-Game Cursor -->')

if js_start != -1 and js_end != -1:
    html = html[:js_start] + html[js_end:]
    print("Purged tactical-cursor JS engine successfully!")
else:
    print("Warning: js bounds not found", js_start, js_end)

# 3. Remove DOM HTML elements
dom_start = html.find('  <!-- Physical Hardware Tactical In-Game Cursor -->\n')
dom_end = html.find('</body>\n\n</html>')

if dom_start != -1 and dom_end != -1:
    html = html[:dom_start] + html[dom_end:]
    print("Purged tactical-cursor DOM HTML elements successfully!")
else:
    print("Warning: dom bounds not found", dom_start, dom_end)

# Verify no more #tactical-cursor in index.html
if 'tactical-cursor' in html:
    print("Warning: tactical-cursor still found in html!")
else:
    print("Confirmed: tactical-cursor is 100% COMPLETELY GONE from index.html!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html saved successfully.")
