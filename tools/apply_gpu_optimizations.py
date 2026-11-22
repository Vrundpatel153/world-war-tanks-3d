import re

# 1. Update assets/BlAypStk.js
bl_path = r'C:\Users\Vrund Patel\Desktop\clone-game\assets\BlAypStk.js'
with open(bl_path, 'r', encoding='utf-8') as f:
    bl = f.read()

# A. Shadow map optimization: only update when tank actually moves > 2 meters, never on camera rotation!
old_shadow_check = 'let e=t.position.distanceToSquared(this.lastShadowCameraPosition),n=t.quaternion.angleTo(this.lastShadowCameraQuaternion);if((e>1e-4||n>.005)&&(this.lastShadowCameraPosition.copy(t.position),this.lastShadowCameraQuaternion.copy(t.quaternion),this.requestShadowMapUpdate()),this.shadowUpdateRequested){let e=this.time.elapsed;e-this.lastShadowUpdateTime>=this.shadowUpdateInterval&&(this.renderer.shadowMap.needsUpdate=!0,this.shadowUpdateRequested=!1,this.lastShadowUpdateTime=e)}'
new_shadow_check = 'let e=t.position.distanceToSquared(this.lastShadowCameraPosition);if(e>4.0&&(this.lastShadowCameraPosition.copy(t.position),this.requestShadowMapUpdate()),this.shadowUpdateRequested){let e=this.time.elapsed;e-this.lastShadowUpdateTime>=200&&(this.renderer.shadowMap.needsUpdate=!0,this.shadowUpdateRequested=!1,this.lastShadowUpdateTime=e)}'

assert old_shadow_check in bl, 'Could not find shadow update check in BlAypStk.js'
bl = bl.replace(old_shadow_check, new_shadow_check)
print('Optimized shadow map update check in BlAypStk.js')

# B. Pixel ratio cap to 1.0 native standard
old_ratio = 'getRenderPixelRatio(){return Math.min(window.devicePixelRatio,this.maxRenderPixelRatio)}'
new_ratio = 'getRenderPixelRatio(){return Math.min(window.devicePixelRatio||1,Math.min(1.0,this.maxRenderPixelRatio||1.0))}'

assert old_ratio in bl, 'Could not find getRenderPixelRatio in BlAypStk.js'
bl = bl.replace(old_ratio, new_ratio)
print('Optimized getRenderPixelRatio in BlAypStk.js')

# C. Optimize initial maxRenderPixelRatio and handleQualityChanged
bl = bl.replace('this.maxRenderPixelRatio=Math.min(typeof window!==\'undefined\'&&(window.devicePixelRatio||1),1.25)', 'this.maxRenderPixelRatio=1.0')
bl = bl.replace('this.maxRenderPixelRatio=t()?1.5:e?1.75:1', 'this.maxRenderPixelRatio=1.0')

# D. Optimize chromatic aberration pass: use direct scene pass texture node i
old_chroma = 'this.chromaticAberrationPass=y(()=>{let e=E(this.scenePass.getLinearDepthNode().toVar().sub(this.focusDistanceUniform)).toVar(),t=u(p(3),p(30),e).mul(.0035).mul(this.chromaticAberrationIntensity).toVar(),n=d(1,.5).normalize().mul(t),r=s().add(n).clamp(0,1),a=s(),o=s().sub(n).clamp(0,1),l=c(i,r).r,m=c(i,a).g,h=c(i,o).b;return f(l,m,h)})()'
new_chroma = 'this.chromaticAberrationPass=i'

if old_chroma in bl:
    bl = bl.replace(old_chroma, new_chroma)
    print('Optimized chromatic aberration pass to direct texture node')

with open(bl_path, 'w', encoding='utf-8') as f:
    f.write(bl)
print('Updated assets/BlAypStk.js successfully!')

# 2. Update index.html
html_path = r'C:\Users\Vrund Patel\Desktop\clone-game\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Remove backdrop-filter rules across index.html
html = re.sub(r'backdrop-filter:\s*blur\([^)]+\);?', '/* backdrop-filter optimized */', html)
print('Removed all backdrop-filter declarations in index.html')

# Normalize saved settings in localStorage so previously saved high renderScale does not lag the game
old_storage_load = '''      try {
        const saved = localStorage.getItem(SETTINGS_STORAGE_KEY);
        if (saved) {
          const parsed = JSON.parse(saved);
          currentSettings = Object.assign({}, defaultSettings, parsed);
        }
      } catch (e) { }'''

new_storage_load = '''      try {
        const saved = localStorage.getItem(SETTINGS_STORAGE_KEY);
        if (saved) {
          const parsed = JSON.parse(saved);
          currentSettings = Object.assign({}, defaultSettings, parsed);
          // Safety clamp: keep renderScale at 1.0 standard for 60 FPS performance
          if (currentSettings.renderScale > 1.0) currentSettings.renderScale = 1.0;
          if (currentSettings.shadowQuality === 'ultra') currentSettings.shadowQuality = 'med';
        }
      } catch (e) { }'''

if old_storage_load in html:
    html = html.replace(old_storage_load, new_storage_load)
    print('Added settings safety clamp to index.html')

# Ensure window.applyAllSettings clamps pixel ratio to 1.0 standard
old_apply_renderer = '''        if (app.renderer) {
          try {
            app.maxRenderPixelRatio = currentSettings.renderScale;
            app.renderer.setPixelRatio(currentSettings.renderScale);
            app.renderer.setSize(window.innerWidth, window.innerHeight);
          } catch(e) {}
        }'''

new_apply_renderer = '''        if (app.renderer) {
          try {
            const safeRatio = Math.min(window.devicePixelRatio || 1, Math.min(1.0, currentSettings.renderScale || 1.0));
            app.maxRenderPixelRatio = safeRatio;
            app.renderer.setPixelRatio(safeRatio);
            app.renderer.setSize(window.innerWidth, window.innerHeight);
          } catch(e) {}
        }'''

if old_apply_renderer in html:
    html = html.replace(old_apply_renderer, new_apply_renderer)
    print('Updated window.applyAllSettings in index.html')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print('Updated index.html successfully!')
