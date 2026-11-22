with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """              <button class="opt-btn" onclick="window.toggleFullscreen()">TOGGLE FULLSCREEN [F11]</button>
            </div>
          </div>
        </div>

        <!-- TAB 3: AUDIO -->"""

replacement = """              <button class="opt-btn" onclick="window.toggleFullscreen()">TOGGLE FULLSCREEN [F11]</button>
            </div>
          </div>

          <!-- Keybindings & Combat Operations Field Manual -->
          <div class="setting-row">
            <div class="setting-label-row">
              <span class="setting-title">FIELD MANUAL &amp; KEYBOARD BINDINGS</span>
              <span class="setting-current-val">STANDARD PROTOCOL</span>
            </div>
            <div style="margin-top: 10px; display: grid; grid-template-columns: 140px 1fr; gap: 8px 16px; background: rgba(0,0,0,0.3); padding: 14px; border: 1px solid rgba(255,255,255,0.08); border-radius: 4px; font-size: 13px;">
              <span style="color: #00ffaa; font-weight: 700;">W / A / S / D</span>
              <span style="color: #c9cdd4;">Drive Caterpillar Treads (Forward, Steer Left, Reverse, Steer Right)</span>

              <span style="color: #00ffaa; font-weight: 700;">MOUSE MOVE</span>
              <span style="color: #c9cdd4;">360&deg; Commander View &amp; Turret Traversal</span>

              <span style="color: #00ffaa; font-weight: 700;">HOLD RIGHT-CLICK</span>
              <span style="color: #c9cdd4;">High-Precision Optical Aim (Aligns Cannon)</span>

              <span style="color: #00ffaa; font-weight: 700;">LEFT-CLICK</span>
              <span style="color: #c9cdd4;">Fire 88mm KwK High-Velocity Cannon</span>

              <span style="color: #00ffaa; font-weight: 700;">Q / E KEYS</span>
              <span style="color: #c9cdd4;">Manual Turret Slew Override</span>

              <span style="color: #00ffaa; font-weight: 700;">LEFT SHIFT</span>
              <span style="color: #c9cdd4;">Engage Turbo Boost Turbine</span>

              <span style="color: #00ffaa; font-weight: 700;">ESC KEY</span>
              <span style="color: #c9cdd4;">Pause Combat Simulation &amp; Access Tactical Command Deck</span>
            </div>
          </div>
        </div>

        <!-- TAB 3: AUDIO -->"""

if target in html:
    html = html.replace(target, replacement)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Field manual added to tab-controls successfully')
else:
    print('Target not found')
