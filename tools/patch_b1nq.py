import os
import subprocess

with open('assets/B1Nq4Kq6.remote.js', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Neutralize skipGameplay class init
target_skip = "this.content=_.skipGameplay,this.init()}init(){this.initDOM(),this.bindEvents()}"
repl_skip = "this.content=_.skipGameplay,this.init()}init(){return;}"
assert target_skip in c, "target_skip not found"
c = c.replace(target_skip, repl_skip, 1)
print("1. Patched skipGameplay -> no-op")

# 2. Disable socialBox initialization (replace expression with 0)
target_social = "this.socialBox&&this.socialBox.init(r?r.scene:n)"
repl_social = "0"
assert target_social in c, "target_social not found"
c = c.replace(target_social, repl_social, 1)
print("2. Patched socialBox.init -> disabled")

# 3. Disable StatueActionAnchor
target_statue = "initStatuePlaceholderPoint(t){t&&Jt({scene:this.scene,source:t,name:`StatueActionAnchor`,type:`OPEN`,handler:()=>{e.emit(`about-page:open`)}})}"
repl_statue = "initStatuePlaceholderPoint(t){return;}"
assert target_statue in c, "target_statue not found"
c = c.replace(target_statue, repl_statue, 1)
print("3. Patched initStatuePlaceholderPoint -> disabled")

# 4. Disable PowerCoreMonitorAnchor (portfolio case study billboard)
target_pc = "this.powerCoreMonitorAnchor=Jt({scene:this.scene,position:t,name:`PowerCoreMonitorAnchor`,handler:()=>{e.emit(`aboutproject:start-camera-sequence`,{targetPosition:t})}})"
repl_pc = "this.powerCoreMonitorAnchor=null"
assert target_pc in c, "target_pc not found"
c = c.replace(target_pc, repl_pc, 1)
print("4. Patched PowerCoreMonitorAnchor -> disabled")

# 5. Disable EB_Transition_Anchor (BTS portfolio slide anchor)
target_eb = "this.transitionAnchor=Jt({scene:this.scene,position:t,name:`EB_Transition_Anchor`,type:`OPEN`,key:`F`,distance:5,handler:()=>{e.emit(`page:bts:open`)}})"
repl_eb = "this.transitionAnchor=null"
assert target_eb in c, "target_eb not found"
c = c.replace(target_eb, repl_eb, 1)
print("5. Patched EB_Transition_Anchor -> disabled")

# 6. Dusk filter opacity 0
target_dusk = "viewportFilterColor:`#ff8181`,viewportFilterOpacity:.15"
repl_dusk = "viewportFilterColor:`#ff8181`,viewportFilterOpacity:0"
assert target_dusk in c, "target_dusk not found"
c = c.replace(target_dusk, repl_dusk, 1)
print("6. Patched dusk viewportFilterOpacity -> 0")

# Test syntax with Node before saving
res = subprocess.run(['node', '--input-type=module', '--check'], input=c, capture_output=True, text=True)
if res.returncode != 0:
    print("SYNTAX ERROR in generated code:", res.stderr)
    exit(1)

with open('assets/B1Nq4Kq6.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("SUCCESS: assets/B1Nq4Kq6.js verified and written cleanly!")
