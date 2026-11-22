import re

# 1. Update assets/BlAypStk.js: Enable hardware antialiasing (antialias: true)
bl_path = r'C:\Users\Vrund Patel\Desktop\clone-game\assets\BlAypStk.js'
with open(bl_path, 'r', encoding='utf-8') as f:
    bl = f.read()

assert 'antialias:!1' in bl
bl = bl.replace('antialias:!1', 'antialias:!0')
print('Enabled hardware antialiasing (MSAA) in BlAypStk.js')

with open(bl_path, 'w', encoding='utf-8') as f:
    f.write(bl)

# 2. Update assets/B1Nq4Kq6.js: Disable halftone hatching, boost tank speed & steering
b1_path = r'C:\Users\Vrund Patel\Desktop\clone-game\assets\B1Nq4Kq6.js'
with open(b1_path, 'r', encoding='utf-8') as f:
    b1 = f.read()

# Disable hatching in lightingManager default: this.uHatchingEnabled=G(1) -> G(0)
assert 'this.uHatchingEnabled=G(1)' in b1
b1 = b1.replace('this.uHatchingEnabled=G(1)', 'this.uHatchingEnabled=G(0)')
print('Disabled comic-book halftone hatching shader in B1Nq4Kq6.js')

# Boost tank speed and agility:
# this.speed=12 -> this.speed=18
# this.rotationSpeed=2.4 -> this.rotationSpeed=3.6
# this.driveLerpRate=24 -> this.driveLerpRate=38
# this.rotationLerpRate=60 -> this.rotationLerpRate=85
assert 'this.speed=12,this.boostSpeed=1.8,this.rotationSpeed=2.4' in b1
b1 = b1.replace('this.speed=12,this.boostSpeed=1.8,this.rotationSpeed=2.4', 'this.speed=18,this.boostSpeed=1.75,this.rotationSpeed=3.6')

assert 'this.driveLerpRate=24' in b1
b1 = b1.replace('this.driveLerpRate=24', 'this.driveLerpRate=38')

assert 'this.rotationLerpRate=60' in b1
b1 = b1.replace('this.rotationLerpRate=60', 'this.rotationLerpRate=85')
print('Boosted tank speed, torque, acceleration, and pivot steering in B1Nq4Kq6.js')

with open(b1_path, 'w', encoding='utf-8') as f:
    f.write(b1)

# 3. Update assets/CQl67Veh.js: Boost mouse sensitivity
cq_path = r'C:\Users\Vrund Patel\Desktop\clone-game\assets\CQl67Veh.js'
with open(cq_path, 'r', encoding='utf-8') as f:
    cq = f.read()

old_sens = 'const sens = (isAimActive ? 0.0020 : 0.0028) * (window.gameMouseSensMultiplier || 1.0);'
new_sens = 'const sens = (isAimActive ? 0.0042 : 0.0058) * (window.gameMouseSensMultiplier || 1.0);'
assert old_sens in cq
cq = cq.replace(old_sens, new_sens)
print('Boosted mouse look sensitivity in CQl67Veh.js')

with open(cq_path, 'w', encoding='utf-8') as f:
    f.write(cq)

print('All HD visual & responsive control upgrades applied successfully!')
