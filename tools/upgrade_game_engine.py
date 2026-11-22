import os
import subprocess
import shutil

print("=== 1. Restoring and Upgrading assets/DPqB0RfP.js ===")
shutil.copy('assets/DPqB0RfP.js.bak', 'assets/DPqB0RfP.js')

with open('assets/DPqB0RfP.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Unlock boost immediately
target_boost = "this.isTouch||this.world.tutorial.hasCardAppeared(`boost`)||(i=!1)"
repl_boost = "0"
assert target_boost in c, "target_boost not found"
c = c.replace(target_boost, repl_boost, 1)
print("DPqB0RfP: Boost unlocked immediately")

# Track left mouse button down for continuous rapid cannon firing
target_mdown = "this.onMouseDown=e=>{"
repl_mdown = "this.onMouseDown=e=>{e.button===0&&(this.leftMouseDown=!0);"
assert target_mdown in c, "target_mdown not found"
c = c.replace(target_mdown, repl_mdown, 1)
print("DPqB0RfP: onMouseDown leftMouseDown tracked")

target_mup = "this.onMouseUp=e=>{"
repl_mup = "this.onMouseUp=e=>{e.button===0&&(this.leftMouseDown=!1);"
assert target_mup in c, "target_mup not found"
c = c.replace(target_mup, repl_mup, 1)
print("DPqB0RfP: onMouseUp leftMouseDown released")

# In getInput, check leftMouseDown for fire
target_shoot = "let e=this.isInputPressed(`backward`),t=this.isInputPressed(`forward`),n=this.isInputPressed(`left`),r=this.isInputPressed(`right`),i=this.isInputPressed(`boost`),a=this.shouldBlockShoot()?!1:this.shootRequested"
repl_shoot = "let e=this.isInputPressed(`backward`),t=this.isInputPressed(`forward`),n=this.isInputPressed(`left`),r=this.isInputPressed(`right`),i=this.isInputPressed(`boost`),a=this.shouldBlockShoot()?!1:(this.shootRequested||!!this.leftMouseDown)"
assert target_shoot in c, "target_shoot not found"
c = c.replace(target_shoot, repl_shoot, 1)
print("DPqB0RfP: Continuous cannon fire enabled on left-click hold")

res = subprocess.run(['node', '--input-type=module', '--check'], input=c, capture_output=True, text=True)
if res.returncode != 0:
    print("DPqB0RfP SYNTAX ERROR:", res.stderr)
    exit(1)
with open('assets/DPqB0RfP.js', 'w', encoding='utf-8') as f:
    f.write(c)
print("DPqB0RfP.js saved successfully.")


print("=== 2. Upgrading assets/BlAypStk.js (Graphics, Antialias, Soft Shadows) ===")
with open('assets/BlAypStk.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Enable antialias
target_aa = "antialias:!1"
repl_aa = "antialias:!0"
if target_aa in c:
    c = c.replace(target_aa, repl_aa, 1)
    print("BlAypStk: antialias -> true")

# High quality PCFSoftShadowMap
target_sh = "this.renderer.shadowMap.type=1"
repl_sh = "this.renderer.shadowMap.type=2"
if target_sh in c:
    c = c.replace(target_sh, repl_sh, 1)
    print("BlAypStk: shadowMap.type -> 2 (PCFSoftShadowMap)")

# Crisp render pixel ratio
target_pr = "this.maxRenderPixelRatio=n?1.5:i?1:1.75"
repl_pr = "this.maxRenderPixelRatio=Math.min(typeof window!=='undefined'&&(window.devicePixelRatio||1),2.0)"
if target_pr in c:
    c = c.replace(target_pr, repl_pr, 1)
    print("BlAypStk: maxRenderPixelRatio -> up to 2.0")

res = subprocess.run(['node', '--input-type=module', '--check'], input=c, capture_output=True, text=True)
if res.returncode != 0:
    print("BlAypStk SYNTAX ERROR:", res.stderr)
    exit(1)
with open('assets/BlAypStk.js', 'w', encoding='utf-8') as f:
    f.write(c)
print("BlAypStk.js saved successfully.")


print("=== 3. Upgrading assets/B1Nq4Kq6.js (Speed, Physics, Ballistics, Anisotropy) ===")
with open('assets/B1Nq4Kq6.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Combat speeds: speed = 15.0, boostSpeed = 2.2, rotationSpeed = 4.8
target_speed = "this.frictionDecayRate=.1,this.speed=8,this.boostSpeed=1.9,this.rotationSpeed=3.12,this.boostRotationMultiplier=1.2"
repl_speed = "this.frictionDecayRate=.1,this.speed=15,this.boostSpeed=2.2,this.rotationSpeed=4.8,this.boostRotationMultiplier=1.25"
if target_speed in c:
    c = c.replace(target_speed, repl_speed, 1)
    print("B1Nq4Kq6: Combat speeds upgraded (speed=15, boost=2.2x, rotation=4.8)")

# Snappy drive lerp rate
target_lerp = "this.driveInputEpsilon=.001,this.driveLerpRate=8"
repl_lerp = "this.driveInputEpsilon=.001,this.driveLerpRate=16"
if target_lerp in c:
    c = c.replace(target_lerp, repl_lerp, 1)
    print("B1Nq4Kq6: Drive throttle lerp rate -> 16")

# Ballistics: projectileSpeed = 95, projectileLife = 3.0
target_proj = "this.projectileSpeed=55,this.projectileLife=1"
repl_proj = "this.projectileSpeed=95,this.projectileLife=3.0"
if target_proj in c:
    c = c.replace(target_proj, repl_proj, 1)
    print("B1Nq4Kq6: Cannon ballistics upgraded (velocity=95 m/s, life=3s)")

# Max 16x Anisotropic texture filtering
target_aniso = "this.textureAnisotropy=4"
repl_aniso = "this.textureAnisotropy=16"
if target_aniso in c:
    c = c.replace(target_aniso, repl_aniso, 1)
    print("B1Nq4Kq6: Texture anisotropy -> 16x hardware maximum")

res = subprocess.run(['node', '--input-type=module', '--check'], input=c, capture_output=True, text=True)
if res.returncode != 0:
    print("B1Nq4Kq6 SYNTAX ERROR:", res.stderr)
    exit(1)
with open('assets/B1Nq4Kq6.js', 'w', encoding='utf-8') as f:
    f.write(c)
print("B1Nq4Kq6.js saved successfully.")

print("All game engine upgrades completed with 100% clean syntax!")
