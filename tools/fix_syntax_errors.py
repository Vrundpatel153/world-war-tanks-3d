import os, subprocess

game_dir = r"C:\Users\Vrund Patel\Desktop\clone-game"

# 1. Fix CQl67Veh.js
cq_path = os.path.join(game_dir, "assets", "CQl67Veh.js")
with open(cq_path, "r", encoding="utf-8") as f:
    cq = f.read()

bad_snippet = ":this.mousePanOffset.lerp(this.targetMousePan,r),let isAim=this.isAiming||this.isAimFixed;"
good_snippet = ":this.mousePanOffset.lerp(this.targetMousePan,r);let isAim=this.isAiming||this.isAimFixed;"

if bad_snippet in cq:
    cq = cq.replace(bad_snippet, good_snippet)
    print("Fixed comma-let in CQl67Veh.js.")
else:
    print("bad_snippet not found, checking...")
    idx = cq.find("let isAim=this.isAiming")
    if idx != -1:
        print("Surrounding:", cq[max(0, idx-50):idx+50])
        cq = cq[:idx-1] + ";" + cq[idx:]

with open(cq_path, "w", encoding="utf-8") as f:
    f.write(cq)

# 2. Fix DPqB0RfP.js: safe navigation for this.world and this.world.tutorial
dp_path = os.path.join(game_dir, "assets", "DPqB0RfP.js")
with open(dp_path, "r", encoding="utf-8") as f:
    dp = f.read()

idx_start = dp.find("shouldBlockShoot(){")
idx_end = dp.find("return!!(", idx_start)

if idx_start != -1 and idx_end != -1:
    end_of_func = dp.find("}", idx_end)
    safe_should_block = "shouldBlockShoot(){let cam=this.world&&this.world.camera;if(cam&&!cam.isAiming&&!cam.isAimFixed)return!0;if(!this.world||!this.world.robot||this.world.robot.isDead)return!0;if(this.world.tutorial&&typeof this.world.tutorial.hasCardAppeared==`function`&&!this.world.tutorial.hasCardAppeared(`shoot`))return!0;if(this.world.grabMode&&(this.world.grabMode.monitoredObjects&&this.world.grabMode.monitoredObjects.length>0||this.world.grabMode.grabbedObject))return!0;if(this.world.revealScreen&&this.world.revealScreen.isActive)return!0;if(this.world.transitionScreen&&this.world.transitionScreen.isFastTravelActive)return!0;return!1}"
    dp = dp[:idx_start] + safe_should_block + dp[end_of_func+1:]
    print("Fixed shouldBlockShoot safe navigation in DPqB0RfP.js.")

with open(dp_path, "w", encoding="utf-8") as f:
    f.write(dp)

cq_norm = cq_path.replace("\\", "/")
dp_norm = dp_path.replace("\\", "/")

print("Running check_syntax...")
res = subprocess.run(["node", "--input-type=module", "-e", f'import "file:///{cq_norm}"'], capture_output=True, text=True)
if res.returncode == 0:
    print("CQl67Veh.js SYNTAX VERIFIED CLEAN!")
else:
    print("CQl67Veh.js Error:\n", res.stderr[:500])

res2 = subprocess.run(["node", "--input-type=module", "-e", f'import "file:///{dp_norm}"'], capture_output=True, text=True)
if res2.returncode == 0:
    print("DPqB0RfP.js SYNTAX VERIFIED CLEAN!")
else:
    print("DPqB0RfP.js Error:\n", res2.stderr[:500])
