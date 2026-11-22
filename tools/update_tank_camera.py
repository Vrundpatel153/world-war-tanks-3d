with open("assets/CQl67Veh.js", "r", encoding="utf-8") as f:
    code = f.read()

# Replace the camera orbit parameters in updatePlayerStartAngle
old_init = "this._orbitDistance = 16.0;\n        this._targetOrbitYaw = 0.46;\n        this._targetOrbitPitch = 0.58;\n        this._targetOrbitDistance = 16.0;"
new_init = "this._orbitDistance = 5.2;\n        this._targetOrbitYaw = 0.0;\n        this._targetOrbitPitch = 0.28;\n        this._targetOrbitDistance = 5.2;"

# Also adjust distance clamping and pitch clamping
old_clamps = "Math.max(0.06, Math.min(1.38, this._targetOrbitPitch));"
new_clamps = "Math.max(-0.08, Math.min(0.85, this._targetOrbitPitch));"

old_dist_clamp = "Math.max(7.0, Math.min(38.0, this._targetOrbitDistance + delta));"
new_dist_clamp = "Math.max(3.0, Math.min(8.5, this._targetOrbitDistance + delta * 0.8));"

# Also vertical offset
old_height = "this.viewAFocus.y+=1.2,this.viewAPosition.y+=1.2"
new_height = "this.viewAFocus.y+=1.4,this.viewAPosition.y+=1.4"

code = code.replace(old_init, new_init)
code = code.replace(old_clamps, new_clamps)
code = code.replace(old_dist_clamp, new_dist_clamp)
code = code.replace(old_height, new_height)

# Also ensure auto-chase camera when driving forward gently aligns behind the tank's heading
with open("assets/CQl67Veh.js", "w", encoding="utf-8") as f:
    f.write(code)

print("Updated CQl67Veh.js with tight World War Tank camera parameters (5.2m distance)!")
