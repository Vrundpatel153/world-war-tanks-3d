# 1. Zero out chromatic aberration in BlAypStk.js
with open("assets/BlAypStk.js", "r", encoding="utf-8") as f:
    bl_code = f.read()

if "this.chromaticAberrationIntensity=S(1)" in bl_code:
    bl_code = bl_code.replace("this.chromaticAberrationIntensity=S(1)", "this.chromaticAberrationIntensity=S(0)")
    with open("assets/BlAypStk.js", "w", encoding="utf-8") as f:
        f.write(bl_code)
    print("Chromatic aberration disabled in BlAypStk.js (razor-sharp rendering)!")
else:
    print("Could not find chromaticAberrationIntensity=S(1) in BlAypStk.js")

# 2. Tone down dusk viewport filter opacity in B1Nq4Kq6.js
with open("assets/B1Nq4Kq6.js", "r", encoding="utf-8") as f:
    b1_code = f.read()

# Replace dusk filter opacity 0.15 with 0.0 to remove murky pink/orange haze
if "viewportFilterOpacity:.15" in b1_code:
    b1_code = b1_code.replace("viewportFilterOpacity:.15", "viewportFilterOpacity:0")
    with open("assets/B1Nq4Kq6.js", "w", encoding="utf-8") as f:
        f.write(b1_code)
    print("Dusk murky viewport filter opacity removed in B1Nq4Kq6.js!")
