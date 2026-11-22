const fs = require('fs');

console.log('--- APPLYING ZELDA-STYLE CONTROLS & CLEAN CENTER CROSSHAIR ---');

// ==========================================
// 1. PATCH B1Nq4Kq6.js (Cannon on front - W key, Q/E left-right buttons, no mouse move cannon)
// ==========================================
let b1 = fs.readFileSync('assets/B1Nq4Kq6.js', 'utf8');

const targetPointerVisual = `handlePointerVisual(e,t){this.rayCaster.setFromCamera(e.mouse,this.camera.instance);let n=null;this.turret.getWorldPosition(this.turretPos),this.groundPlane.constant=-this.turretPos.y,this.rayCaster.ray.intersectPlane(this.groundPlane,this.intersectPoint)&&(this.aimDir.set(this.intersectPoint.x-this.turretPos.x,0,this.intersectPoint.z-this.turretPos.z),this.aimDir.lengthSq()>this.aimLengthEpsilon&&(this.aimDir.normalize(),n=this.getTurretTargetQuat(this.aimDir))),this.applyTurretAim(n,t),this.aimRaycastAccumulator+=t,this.aimRaycastAccumulator>=.02&&(this.aimRaycastAccumulator=0,this.handleAiming(this.rayCaster))}`;

const replPointerVisual = `handlePointerVisual(e,t){this.turretManualAngle=this.turretManualAngle||0;let r=2.6;if(this.controller&&this.controller.keyPressed){(this.controller.keyPressed.has(\`KeyQ\`)||this.controller.keyPressed.has(\`ArrowLeft\`))&&(this.turretManualAngle+=r*t);(this.controller.keyPressed.has(\`KeyE\`)||this.controller.keyPressed.has(\`ArrowRight\`))&&(this.turretManualAngle-=r*t);(this.controller.keyPressed.has(\`KeyC\`)||this.controller.keyPressed.has(\`KeyX\`))&&(this.turretManualAngle=0)}let n=this.targetTurretQuat.setFromAxisAngle(this.yAxis,this.turretManualAngle);this.applyTurretAim(n,t),this.aimRaycastAccumulator+=t,this.aimRaycastAccumulator>=.02&&(this.aimRaycastAccumulator=0,this.handleAiming(this.rayCaster))}`;

if (!b1.includes(targetPointerVisual)) {
  throw new Error('targetPointerVisual not found in B1Nq4Kq6.js');
}
b1 = b1.replace(targetPointerVisual, replPointerVisual);
fs.writeFileSync('assets/B1Nq4Kq6.js', b1, 'utf8');
console.log('1. B1Nq4Kq6.js patched: Cannon fixed on front (W key), Q/E turn cannon, mouse does not move cannon.');

// ==========================================
// 2. PATCH CQl67Veh.js (Mouse look around like Zelda)
// ==========================================
let cq = fs.readFileSync('assets/CQl67Veh.js', 'utf8');

const targetOnMove = `const onMove = ev => {
            const isLocked = !!document.pointerLockElement;
            if(isLocked || this._isDragging){
                const dx = isLocked ? ev.movementX : (ev.clientX - this._lastPointerX);
                const dy = isLocked ? ev.movementY : (ev.clientY - this._lastPointerY);
                this._lastPointerX = ev.clientX;
                this._lastPointerY = ev.clientY;
                const sens = 0.0035;
                this._targetOrbitYaw -= dx * sens;
                this._targetOrbitPitch += dy * sens;
                this._targetOrbitPitch = Math.max(-0.08, Math.min(0.85, this._targetOrbitPitch));
                this._userLookTimer = 1.5;
            }
        };`;

const replOnMove = `const onMove = ev => {
            const isLocked = !!document.pointerLockElement;
            let dx = 0, dy = 0;
            if (isLocked) {
                dx = ev.movementX || 0;
                dy = ev.movementY || 0;
            } else {
                if (this._lastPointerX !== 0 && this._lastPointerY !== 0) {
                    dx = ev.clientX - this._lastPointerX;
                    dy = ev.clientY - this._lastPointerY;
                }
                this._lastPointerX = ev.clientX;
                this._lastPointerY = ev.clientY;
            }
            if (Math.abs(dx) > 160 || Math.abs(dy) > 160) { dx = 0; dy = 0; }
            if (dx !== 0 || dy !== 0) {
                const sens = 0.0032;
                this._targetOrbitYaw -= dx * sens;
                this._targetOrbitPitch += dy * sens;
                this._targetOrbitPitch = Math.max(-0.08, Math.min(0.85, this._targetOrbitPitch));
                this._userLookTimer = 8.0;
            }
        };`;

if (!cq.includes(targetOnMove)) {
  throw new Error('targetOnMove not found in CQl67Veh.js');
}
cq = cq.replace(targetOnMove, replOnMove);
fs.writeFileSync('assets/CQl67Veh.js', cq, 'utf8');
console.log('2. CQl67Veh.js patched: Mouse look around enabled freely like Zelda.');

// ==========================================
// 3. PATCH DPqB0RfP.js (White crosshair fixed middle center like Zelda)
// ==========================================
let dp = fs.readFileSync('assets/DPqB0RfP.js', 'utf8');

const targetUpdatePos = `updatePosition(e,t){this.root&&(this.root.style.left=\`\${e}px\`,this.root.style.top=\`\${t}px\`,(!this.isVisible||this.root.style.display===\`none\`)&&this.show())}`;
const replUpdatePos = `updatePosition(e,t){if(!this.root)return;this.root.style.left=\`50%\`,this.root.style.top=\`50%\`,this.root.style.transform=\`translate(-50%,-50%)\`,(!this.isVisible||this.root.style.display===\`none\`)&&this.show()}`;

if (!dp.includes(targetUpdatePos)) {
  throw new Error('targetUpdatePos not found in DPqB0RfP.js');
}
dp = dp.replace(targetUpdatePos, replUpdatePos);

// In triggerClickAnimation do not move left/top away from 50%
const targetClickPos = `Number.isFinite(e)&&Number.isFinite(t)&&(this.root.style.left=\`\${e}px\`,this.root.style.top=\`\${t}px\`),this.root.style.display=\`block\``;
const replClickPos = `this.root.style.left=\`50%\`,this.root.style.top=\`50%\`,this.root.style.display=\`block\``;
if (dp.includes(targetClickPos)) {
  dp = dp.replace(targetClickPos, replClickPos);
}

fs.writeFileSync('assets/DPqB0RfP.js', dp, 'utf8');
console.log('3. DPqB0RfP.js patched: White crosshair locked to center.');

// ==========================================
// 4. PATCH index.html (Remove duplicate cyan crosshair, style Zelda white reticle)
// ==========================================
let html = fs.readFileSync('index.html', 'utf8');

// Remove cyan crosshair div
const crosshairDiv = `<div class="tank-crosshair" id="tank-crosshair">
        <svg viewBox="0 0 64 64" fill="none" stroke="#00ffaa" stroke-width="2">
          <!-- Outer Circle -->
          <circle cx="32" cy="32" r="28" stroke-dasharray="6 4" opacity="0.6"/>
          <!-- Inner Precision Circle -->
          <circle cx="32" cy="32" r="10" stroke-width="1.5"/>
          <!-- Center Dot -->
          <circle cx="32" cy="32" r="2" fill="#00ffaa"/>
          <!-- Four Tactical Ticks -->
          <line x1="32" y1="4" x2="32" y2="16"/>
          <line x1="32" y1="48" x2="32" y2="60"/>
          <line x1="4" y1="32" x2="16" y2="32"/>
          <line x1="48" y1="32" x2="60" y2="32"/>
        </svg>
      </div>`;

if (html.includes(crosshairDiv)) {
  html = html.replace(crosshairDiv, '');
  console.log('Removed duplicate cyan tank-crosshair HTML.');
}

// Remove old .tank-crosshair CSS and add Zelda white crosshair CSS
const oldCssBlock = `      /* Central Reticle */
      .tank-crosshair {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 64px;
        height: 64px;
        pointer-events: none;
      }
      .tank-crosshair svg {
        width: 100%;
        height: 100%;
        filter: drop-shadow(0 0 4px rgba(0, 255, 170, 0.6));
      }`;

const zeldaCrosshairCss = `      /* Zelda-style Minimalist Fixed Center White Reticle */
      #aim-circle {
        position: fixed !important;
        top: 50% !important;
        left: 50% !important;
        transform: translate(-50%, -50%) !important;
        width: 26px !important;
        height: 26px !important;
        pointer-events: none !important;
        display: block !important;
        z-index: 99999 !important;
        opacity: 0.92;
        transition: transform 0.08s ease-out;
      }
      #aim-circle .aim-visual {
        position: absolute !important;
        inset: 0 !important;
        width: 100% !important;
        height: 100% !important;
      }
      #aim-circle .aim-part {
        width: 11px !important;
        height: 11px !important;
        background-size: contain !important;
        filter: drop-shadow(0 0 2px rgba(0, 0, 0, 0.9)) !important;
      }
      #aim-circle .aim-dot {
        --aim-dot-size: 4px !important;
        --aim-dot-border: 1px !important;
        background: #ffffff !important;
        box-shadow: 0 0 3px rgba(0, 0, 0, 0.9) !important;
      }
      #aim-circle .aim-top { top: 0 !important; left: 0 !important; }
      #aim-circle .aim-bottom { bottom: 0 !important; right: 0 !important; }
      #aim-circle .aim-left { bottom: 0 !important; left: 0 !important; }
      #aim-circle .aim-right { top: 0 !important; right: 0 !important; }`;

if (html.includes(oldCssBlock)) {
  html = html.replace(oldCssBlock, zeldaCrosshairCss);
  console.log('Replaced tank-crosshair CSS with Zelda-style #aim-circle CSS.');
}

// Update control hints
const oldHints = 'WASD TANK TREADS · MOUSE TURRET AIM & CAMERA · SPACE / L-CLICK FIRE · SHIFT BOOST · SCROLL ZOOM';
const newHints = 'WASD TANK DRIVE · MOUSE LOOK AROUND · Q / E ROTATE CANNON · C RE-CENTER · L-CLICK / SPACE FIRE · SHIFT BOOST · SCROLL ZOOM';
if (html.includes(oldHints)) {
  html = html.replace(oldHints, newHints);
  console.log('Updated tactical control hints banner.');
}

// Update screen recoil to kick #aim-circle
const oldRecoilCode = `const ch = document.querySelector('#tank-crosshair');
          if (ch) {
            ch.style.transform = 'translate(-50%, -55%) scale(1.15)';
            setTimeout(() => {
              ch.style.transform = 'translate(-50%, -50%) scale(1.0)';
            }, 120);
          }`;

const newRecoilCode = `const ch = document.querySelector('#aim-circle');
          if (ch) {
            ch.style.transform = 'translate(-50%, -54%) scale(1.2)';
            setTimeout(() => {
              ch.style.transform = 'translate(-50%, -50%) scale(1.0)';
            }, 100);
          }`;

if (html.includes(oldRecoilCode)) {
  html = html.replace(oldRecoilCode, newRecoilCode);
  console.log('Updated recoil animation to #aim-circle.');
}

// Add pointer lock click handler on canvas
const pointerLockSnippet = `        // Canvas click lock for seamless Zelda camera look
        window.addEventListener('click', function(e) {
          if (!e.target || e.target.closest('button, a, input, textarea')) return;
          const canvas = document.querySelector('canvas');
          if (canvas && document.pointerLockElement !== canvas) {
            canvas.requestPointerLock?.();
          }
        });`;

if (!html.includes('Canvas click lock for seamless Zelda camera look')) {
  const insertBefore = 'function triggerShoot() {';
  html = html.replace(insertBefore, pointerLockSnippet + '\n\n        ' + insertBefore);
  console.log('Added canvas pointer lock listener for seamless mouse look.');
}

fs.writeFileSync('index.html', html, 'utf8');
console.log('4. index.html updated successfully.');

console.log('--- ALL PATCHES APPLIED CLEANLY ---');
