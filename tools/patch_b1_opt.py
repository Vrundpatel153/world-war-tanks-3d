with open('assets/B1Nq4Kq6.js', 'r', encoding='utf-8', errors='ignore') as f:
    b1 = f.read()

# 1. Reverse steering fix
pos_steer = b1.find('if(s>0){l=-l;}')
if pos_steer != -1:
    print('Found reverse steering inverted check at', pos_steer)
    b1_new = b1.replace('if(s>0){l=-l;}', '/* natural reverse */')
    print('Replaced steering successfully!')
else:
    print('Warning: if(s>0){l=-l;} not found')

# 2. shouldSkipInstancePacking
pos_skip = b1.find('shouldSkipInstancePacking(e,t){return true}')
if pos_skip != -1:
    print('Found shouldSkipInstancePacking at', pos_skip)
    # restore original skip logic:
    # shouldSkipInstancePacking(e,t){return!e||!t||!t.userData||e.role===`blockWall`?!0:t.userData.skipInstanceViewportPack===!0}
    b1_new = b1_new.replace(
        'shouldSkipInstancePacking(e,t){return true}',
        'shouldSkipInstancePacking(e,t){return!e||!t||!t.userData||e.role===`blockWall`?!0:t.userData.skipInstanceViewportPack===!0}'
    )
    print('Restored shouldSkipInstancePacking')

# 3. isInstancedTransformVisible: add 90m distance cull + safe margin
pos_inst = b1.find('isInstancedTransformVisible(e,t,n,r){if(!this.isInstancedInstanceActive(e,r))return!1;if(!this.enabled)return!0;')
if pos_inst != -1:
    print('Found isInstancedTransformVisible at', pos_inst)
    old_inst = 'isInstancedTransformVisible(e,t,n,r){if(!this.isInstancedInstanceActive(e,r))return!1;if(!this.enabled)return!0;if(!t||!t.position)return!1;let i=t.scale||this.tempScale,a=n*Math.max(i.x,i.y,i.z)+this.mainCameraVisibilityCullPadding,o=t.position;return this.intersectsSphereFast(o.x,o.y,o.z,a)}'
    new_inst = 'isInstancedTransformVisible(e,t,n,r){if(!this.isInstancedInstanceActive(e,r))return!1;if(!t||!t.position)return!1;let cam=this.areaManager&&this.areaManager.camera?this.areaManager.camera.activeInstance||this.areaManager.camera.instance:null;if(cam){let dx=t.position.x-cam.position.x,dz=t.position.z-cam.position.z;if(dx*dx+dz*dz>90*90)return!1;}if(!this.enabled)return!0;let i=t.scale||this.tempScale,a=n*Math.max(i.x,i.y,i.z)+this.mainCameraVisibilityCullPadding+8.0,o=t.position;return this.intersectsSphereFast(o.x,o.y,o.z,a)}'
    if old_inst in b1_new:
        b1_new = b1_new.replace(old_inst, new_inst)
        print('Updated isInstancedTransformVisible with distance culling!')
    else:
        print('Warning: old_inst exact match not found')

with open('assets/B1Nq4Kq6.js', 'w', encoding='utf-8') as f:
    f.write(b1_new)

print('B1Nq4Kq6.js saved.')
