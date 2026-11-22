import re

# 1. Update CQl67Veh.js vertical framing
with open("assets/CQl67Veh.js", "r", encoding="utf-8") as f:
    cq_code = f.read()

# Look for viewAPosition.copy(this.targetEased).add(n)
old_str = "this.viewAPosition.copy(this.targetEased).add(n).add(this.mousePanOffset).add(this.panViewOffset).add(this.recoilOffset),this.viewAFocus.copy(this.targetEased).add(this.mousePanOffset).add(this.panViewOffset).add(this.recoilOffset)"
new_str = "this.viewAPosition.copy(this.targetEased).add(n).add(this.mousePanOffset).add(this.panViewOffset).add(this.recoilOffset),this.viewAFocus.copy(this.targetEased).add(this.mousePanOffset).add(this.panViewOffset).add(this.recoilOffset),this.viewAFocus.y+=1.2,this.viewAPosition.y+=1.2"

if old_str in cq_code:
    cq_code = cq_code.replace(old_str, new_str)
    with open("assets/CQl67Veh.js", "w", encoding="utf-8") as f:
        f.write(cq_code)
    print("Adjusted CQl67Veh.js camera focus height (+1.2y)!")
else:
    print("Could not find viewAPosition string in CQl67Veh.js")

# 2. Patch B1Nq4Kq6.js for Camera-Guided Tank Driving
with open("assets/B1Nq4Kq6.js", "r", encoding="utf-8") as f:
    b1_code = f.read()

target_str = 'let s=(n.forward?-1:0)+ +!!n.backward,l=+!!n.left+(n.right?-1:0);if(this.world.grabMode&&this.world.grabMode.grabbedObject){let e=this.controller.keyPressed.has(`KeyW`),t=this.controller.keyPressed.has(`KeyS`),n=this.controller.keyPressed.has(`KeyA`),r=this.controller.keyPressed.has(`KeyD`);s=(t?-1:0)+ +!!e,l=+!!n+(r?-1:0)}let u=s!==0||l!==0;'

replacement_str = '''let s=(n.forward?-1:0)+ +!!n.backward,l=+!!n.left+(n.right?-1:0);
if(this.world.grabMode&&this.world.grabMode.grabbedObject){
    let e=this.controller.keyPressed.has(`KeyW`),t=this.controller.keyPressed.has(`KeyS`),n=this.controller.keyPressed.has(`KeyA`),r=this.controller.keyPressed.has(`KeyD`);
    s=(t?-1:0)+ +!!e,l=+!!n+(r?-1:0);
}
// Camera-guided vehicle steering assist (Option A + B)
if(s < 0 && l === 0 && this.camera && this.camera.instance){
    let cam = this.camera.instance;
    let camDirX = -Math.sin(cam.rotation.y || 0);
    let camDirZ = -Math.cos(cam.rotation.y || 0);
    if(this.camera.mixedFocus && this.camera.instance.position){
        camDirX = this.camera.mixedFocus.x - this.camera.instance.position.x;
        camDirZ = this.camera.mixedFocus.z - this.camera.instance.position.z;
    } else if(this.camera.viewAFocus && this.camera.viewAPosition){
        camDirX = this.camera.viewAFocus.x - this.camera.viewAPosition.x;
        camDirZ = this.camera.viewAFocus.z - this.camera.viewAPosition.z;
    }
    let camLen = Math.hypot(camDirX, camDirZ);
    if(camLen > 0.001){
        camDirX /= camLen;
        camDirZ /= camLen;
        let p = this.getDirection();
        let tankYaw = Math.atan2(p.z, p.x);
        let camYaw = Math.atan2(camDirZ, camDirX);
        let diff = (camYaw - tankYaw) % (Math.PI * 2);
        if(diff < -Math.PI) diff += Math.PI * 2;
        if(diff > Math.PI) diff -= Math.PI * 2;
        if(Math.abs(diff) > 0.06){
            l = -Math.sign(diff) * Math.min(1.0, Math.abs(diff) * 2.8);
        }
    }
}
let u=s!==0||l!==0;'''

if target_str in b1_code:
    b1_code = b1_code.replace(target_str, replacement_str)
    with open("assets/B1Nq4Kq6.js", "w", encoding="utf-8") as f:
        f.write(b1_code)
    print("Successfully patched B1Nq4Kq6.js with camera-guided tank driving!")
else:
    print("Could not find target_str in B1Nq4Kq6.js")
