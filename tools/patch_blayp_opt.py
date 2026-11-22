with open('assets/BlAypStk.js', 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

# 1. Cap default maxRenderPixelRatio to 1.0
old_init = "this.maxRenderPixelRatio=Math.min(typeof window!=='undefined'&&(window.devicePixelRatio||1),1.25)"
new_init = "this.maxRenderPixelRatio=Math.min(typeof window!=='undefined'&&(window.devicePixelRatio||1),1.0)"

if old_init in code:
    code = code.replace(old_init, new_init)
    print("Replaced default maxRenderPixelRatio with 1.0")
else:
    print("Warning: old_init not found")

# 2. Cap quality changed maxRenderPixelRatio
old_qual = "this.maxRenderPixelRatio=t()?1.5:e?1.75:1"
new_qual = "this.maxRenderPixelRatio=t()?1.0:e?1.15:1.0"

if old_qual in code:
    code = code.replace(old_qual, new_qual)
    print("Replaced quality changed maxRenderPixelRatio with 1.15 max")
else:
    print("Warning: old_qual not found")

with open('assets/BlAypStk.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("BlAypStk.js saved.")
