import os, subprocess

game_dir = r"C:\Users\Vrund Patel\Desktop\clone-game"
cq_path = os.path.join(game_dir, "assets", "CQl67Veh.js")

with open(cq_path, "r", encoding="utf-8") as f:
    cq = f.read()

target_str = "let r=1-Math.exp(-this.mousePanDampSpeed*e);"
idx1 = cq.find(target_str)
idx2 = cq.find("this.introCamera.active||this.introCamera.zoomScale>1.01){", idx1)

if idx1 != -1 and idx2 != -1:
    clean_replacement = """let r=1-Math.exp(-this.mousePanDampSpeed*e);
if(this.mousePanOffset.distanceToSquared(this.targetMousePan)<1e-6){
  this.mousePanOffset.copy(this.targetMousePan);
}else{
  this.mousePanOffset.lerp(this.targetMousePan,r);
}
let isAim=this.isAiming||this.isAimFixed;
let camElev=isAim?2.2:1.9;
let focusElev=isAim?1.5:1.2;
this.viewAPosition.copy(this.targetEased).add(n).add(this.mousePanOffset).add(this.panViewOffset).add(this.recoilOffset);
this.viewAPosition.y+=camElev;
this.viewAFocus.copy(this.targetEased).add(this.mousePanOffset).add(this.panViewOffset).add(this.recoilOffset);
let sinY_f=Math.sin(this._orbitYaw),cosY_f=Math.cos(this._orbitYaw);
this.forwardVec.set(-sinY_f,0,-cosY_f).normalize();
this.viewAFocus.addScaledVector(this.forwardVec,22);
this.viewAFocus.y+=focusElev;

if(this.introCamera.active||this.introCamera.zoomScale>1.01){"""
    
    cq = cq[:idx1] + clean_replacement + cq[idx2+len("this.introCamera.active||this.introCamera.zoomScale>1.01){"):]
    with open(cq_path, "w", encoding="utf-8") as f:
        f.write(cq)
    print("CQl67Veh.js camera block replaced cleanly.")
else:
    print("Could not find markers in CQl67Veh.js:", idx1, idx2)

cq_norm = cq_path.replace("\\", "/")
res = subprocess.run(["node", "--input-type=module", "-e", f'import "file:///{cq_norm}"'], capture_output=True, text=True)
if res.returncode == 0:
    print("=== CQl67Veh.js SYNTAX VERIFIED COMPLETELY CLEAN! ===")
else:
    print("CQl67Veh.js Error:\n", res.stderr[:500])
