with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# 1. Add u-visually-hidden to Core Technology section
old_sec = '<section aria-label="Core Technology">'
new_sec = '<section class="u-visually-hidden" aria-label="Core Technology">'

if old_sec in html:
    html = html.replace(old_sec, new_sec)
    print("Fixed Core Technology section visibility")
else:
    print("Warning: old_sec not found")

# 2. Ensure #webgl CSS has opacity: 1 !important and visibility: visible !important
old_webgl_css = """    #webgl {
      position: fixed;
      inset: 0;
      width: 100%;
      height: 100%;
      display: block;
      z-index: 1;
      touch-action: none;
    }"""

new_webgl_css = """    #webgl {
      position: fixed !important;
      inset: 0 !important;
      width: 100% !important;
      height: 100% !important;
      display: block !important;
      opacity: 1 !important;
      visibility: visible !important;
      z-index: 1 !important;
      touch-action: none;
    }"""

if old_webgl_css in html:
    html = html.replace(old_webgl_css, new_webgl_css)
    print("Enforced #webgl opacity: 1 !important in CSS")
else:
    print("Warning: old_webgl_css not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html updated.")

# 3. In assets/vYUQZzfX.js: ensure canvas is never hidden with opacity = 0
with open('assets/vYUQZzfX.js', 'r', encoding='utf-8', errors='ignore') as f:
    vy = f.read()

old_vy = 'v&&(v.style.opacity=`0`,v.style.transition=`opacity 320ms ease`)'
new_vy = 'v&&(v.style.opacity=`1`,v.style.transition=`opacity 320ms ease`)'

if old_vy in vy:
    vy = vy.replace(old_vy, new_vy)
    with open('assets/vYUQZzfX.js', 'w', encoding='utf-8') as f:
        f.write(vy)
    print("assets/vYUQZzfX.js updated to keep canvas visible at opacity 1!")
else:
    print("Warning: old_vy not found in vYUQZzfX.js")

# 4. In assets/B1Nq4Kq6.js: ONLY fix reverse steering (s>0 l=-l), leave all rendering/culling intact
with open('assets/B1Nq4Kq6.js', 'r', encoding='utf-8', errors='ignore') as f:
    b1 = f.read()

old_steer = 'if(s>0){l=-l;}'
new_steer = '/* natural steer */'

if old_steer in b1:
    b1 = b1.replace(old_steer, new_steer)
    with open('assets/B1Nq4Kq6.js', 'w', encoding='utf-8') as f:
        f.write(b1)
    print("assets/B1Nq4Kq6.js reverse steering fixed!")
else:
    print("Note: old_steer not found or already fixed in B1Nq4Kq6.js")
