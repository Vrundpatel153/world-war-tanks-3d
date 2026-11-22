index_path = r'C:\Users\Vrund Patel\Desktop\clone-game\index.html'
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove the aim alert div
idx1 = html.find('id="aim-required-alert"')
if idx1 != -1:
    start = html.rfind('<div', 0, idx1)
    end = html.find('</div>', idx1) + 6
    html = html[:start] + '<!-- Free Combat Fire Active -->' + html[end:]
    print('Removed aim-required-alert div')

# 2. Update controls hint bar
idx2 = html.find('class="tank-controls-bar"')
if idx2 != -1:
    start2 = html.rfind('<div', 0, idx2)
    end2 = html.find('</div>', idx2) + 6
    new_bar = '''    <div class="tank-controls-bar">
      <span>WASD</span> DRIVE TANK &middot; <span>MOUSE</span> 360° TURRET AIM &middot; <span>L-CLICK / SPACE</span> FIRE CANNON &middot; <span>HOLD R-CLICK</span> OPTICAL SNIPER ZOOM &middot; <span>ESC</span> PAUSE MENU
    </div>'''
    html = html[:start2] + new_bar + html[end2:]
    print('Updated controls hint bar')

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(html)

print('Cleaned HUD markup in index.html successfully!')
