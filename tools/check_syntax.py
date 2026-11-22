import subprocess

p = "C:/Users/Vrund Patel/Desktop/clone-game/assets/CQl67Veh.js"
res = subprocess.run(["node", "--input-type=module", "-e", f'import "file:///{p}"'], capture_output=True, text=True)
lines = res.stderr.splitlines()
for l in lines[-25:]:
    print(l)
