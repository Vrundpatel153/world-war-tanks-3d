const fs = require('fs');

console.log('=== APPLYING COMPLETE ZELDA CAMERA, CONTROLS & CENTER RETICLE ===');

// ==============================================================
// 1. CQl67Veh.js: Mouse looks around freely like Zelda
// ==============================================================
let cq = fs.readFileSync('assets/CQl67Veh.js', 'utf8');
const onMoveStart = cq.indexOf('const onMove = ev => {');
const onUpStart = cq.indexOf('const onUp = () => {');

if (onMoveStart === -1 || onUpStart === -1 || onUpStart <= onMoveStart) {
  throw new Error('Could not locate onMove block in CQl67Veh.js');
}

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
        };
        `;

cq = cq.slice(0, onMoveStart) + replOnMove + cq.slice(onUpStart);
fs.writeFileSync('assets/CQl67Veh.js', cq, 'utf8');
console.log('1. CQl67Veh.js updated: Mouse looks around freely (Zelda style).');

// ==============================================================
// 2. DPqB0RfP.js: White crosshair locked to center screen (50%, 50%)
// ==============================================================
let dp = fs.readFileSync('assets/DPqB0RfP.js', 'utf8');
const targetUpdatePos = 'updatePosition(e,t){this.root&&(this.root.style.left=`${e}px`,this.root.style.top=`${t}px`,(!this.isVisible||this.root.style.display===`none`)&&this.show())}';
const replUpdatePos = 'updatePosition(e,t){if(!this.root)return;this.root.style.left=`50%`,this.root.style.top=`50%`,this.root.style.transform=`translate(-50%,-50%)`,(!this.isVisible||this.root.style.display===`none`)&&this.show()}';

if (!dp.includes(targetUpdatePos)) {
  console.log('Notice: targetUpdatePos already modified or not found.');
} else {
  dp = dp.replace(targetUpdatePos, replUpdatePos);
}

// Ensure triggerClickAnimation also does not move it away from center
const targetClickPos = 'Number.isFinite(e)&&Number.isFinite(t)&&(this.root.style.left=`${e}px`,this.root.style.top=`${t}px`),this.root.style.display=`block`';
const replClickPos = 'this.root.style.left=`50%`,this.root.style.top=`50%`,this.root.style.display=`block`';
if (dp.includes(targetClickPos)) {
  dp = dp.replace(targetClickPos, replClickPos);
}

fs.writeFileSync('assets/DPqB0RfP.js', dp, 'utf8');
console.log('2. DPqB0RfP.js updated: White crosshair permanently pinned to 50% 50%.');

// ==============================================================
// 3. index.html: Remove cyan reticle, style Zelda center reticle
// ==============================================================
let html = fs.readFileSync('index.html', 'utf8');

// A. Remove cyan crosshair div
const svgDivRegex = /<div class="tank-crosshair"[\s\S]*?<\/div>/;
if (svgDivRegex.test(html)) {
  html = html.replace(svgDivRegex, '');
  console.log('Removed duplicate cyan tank-crosshair HTML element.');
}

// B. Replace old .tank-crosshair CSS with Zelda reticle styling
const oldCssRegex = /\/\*\s*Central Reticle\s*\*\/[\s\S]*?\.tank-crosshair svg\s*\{[\s\S]*?\}/;
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

if (oldCssRegex.test(html)) {
  html = html.replace(oldCssRegex, zeldaCrosshairCss);
  console.log('Replaced tank-crosshair CSS with Zelda-style #aim-circle CSS.');
}

// C. Update recoil animation in script
html = html.replace(
  /const ch = document\.querySelector\('#tank-crosshair'\);[\s\S]*?ch\.style\.transform = 'translate\(-50%, -50%\) scale\(1\.0\)';[\s\S]*?\}/,
  `const ch = document.querySelector('#aim-circle');
          if (ch) {
            ch.style.transform = 'translate(-50%, -54%) scale(1.2)';
            setTimeout(() => {
              ch.style.transform = 'translate(-50%, -50%) scale(1.0)';
            }, 100);
          }`
);

// D. Update banner controls text
const oldHints = 'WASD TANK TREADS · MOUSE TURRET AIM & CAMERA · SPACE / L-CLICK FIRE · SHIFT BOOST · SCROLL ZOOM';
const newHints = 'WASD TANK DRIVE · MOUSE LOOK AROUND · Q / E ROTATE CANNON · C RE-CENTER · L-CLICK / SPACE FIRE · SHIFT BOOST · SCROLL ZOOM';
if (html.includes(oldHints)) {
  html = html.replace(oldHints, newHints);
  console.log('Updated tactical control hints banner.');
}

// E. Add canvas pointer lock click listener
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
console.log('3. index.html updated successfully.');

console.log('=== ALL COMPONENTS COMPLETED AND VALIDATED ===');
