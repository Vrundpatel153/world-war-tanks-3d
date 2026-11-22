html_path = r'C:\Users\Vrund Patel\Desktop\clone-game\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace from #game-home-screen { to #btn-return-menu {
start_str = '    #game-home-screen {\n      position: fixed !important;'
end_str = '    /* In-game return to menu button */'

pos_start = html.find(start_str)
pos_end = html.find(end_str)

if pos_start == -1 or pos_end == -1:
    print(f"Error finding anchors! start: {pos_start}, end: {pos_end}")
    exit(1)

deck_css = """    /* =========================================================
       AUTHENTIC AAA VIDEO GAME COMMAND DECK & HOME SCREEN
       ========================================================= */
    #game-home-screen {
      position: fixed !important;
      inset: 0 !important;
      z-index: 100000 !important;
      display: flex !important;
      flex-direction: column !important;
      justify-content: space-between !important;
      align-items: center !important;
      padding: 36px 48px 24px 48px !important;
      box-sizing: border-box !important;
      pointer-events: auto !important;
      /* Genuine AAA Military Dark Slate Steel & Tactical Vignette */
      background: 
        radial-gradient(circle at 50% 25%, rgba(28, 36, 54, 0.85) 0%, rgba(13, 16, 24, 0.98) 65%, #080a0f 100%),
        linear-gradient(rgba(199, 255, 114, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(199, 255, 114, 0.03) 1px, #080a0f 1px) !important;
      background-size: 100% 100%, 40px 40px, 40px 40px !important;
      opacity: 1;
      visibility: visible;
      transition: opacity 0.35s cubic-bezier(0.16, 1, 0.3, 1), visibility 0.35s ease;
      font-family: "Rajdhani", "Barlow Condensed", sans-serif;
      user-select: none;
      overflow: hidden;
    }

    #game-home-screen.menu-hidden {
      opacity: 0 !important;
      visibility: hidden !important;
      pointer-events: none !important;
    }

    /* Top Command Header */
    .deck-top-bar {
      width: 100%;
      max-width: 1320px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(199, 255, 114, 0.25);
      padding-bottom: 14px;
      box-sizing: border-box;
    }

    .deck-brand {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .deck-badge {
      padding: 4px 12px;
      background: #c7ff72;
      color: #080a0f;
      font-size: 13px;
      font-weight: 800;
      letter-spacing: 0.14em;
      border-radius: 3px;
    }

    .deck-sector {
      font-size: 13px;
      font-weight: 700;
      color: #8f9bb3;
      letter-spacing: 0.12em;
      text-transform: uppercase;
    }

    .deck-telemetry {
      display: flex;
      align-items: center;
      gap: 16px;
      font-size: 12px;
      font-weight: 700;
      letter-spacing: 0.1em;
      color: #68758d;
    }

    .deck-status-active {
      color: #00ffaa;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .deck-status-active::before {
      content: "";
      width: 8px;
      height: 8px;
      background: #00ffaa;
      border-radius: 50%;
      box-shadow: 0 0 8px #00ffaa;
      animation: status-blink 2s infinite ease-in-out;
    }

    @keyframes status-blink {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
    }

    /* Main Deck Layout: 2 High-Tech Columns */
    .deck-body {
      width: 100%;
      max-width: 1320px;
      display: grid;
      grid-template-columns: 460px 1fr;
      gap: 48px;
      align-items: center;
      margin: auto 0;
    }

    /* Left Column: Command & Deploy */
    .deck-left-col {
      display: flex;
      flex-direction: column;
      gap: 22px;
    }

    .deck-hero-title {
      font-family: "Rajdhani", "Barlow Condensed", sans-serif;
      font-size: 58px;
      font-weight: 900;
      line-height: 0.95;
      letter-spacing: 0.05em;
      color: #ffffff;
      text-transform: uppercase;
      text-shadow: 0 4px 20px rgba(0, 0, 0, 0.9);
      margin: 0;
    }

    .deck-hero-title span {
      color: #c7ff72;
      text-shadow: 0 0 24px rgba(199, 255, 114, 0.45);
    }

    .deck-hero-sub {
      font-size: 14px;
      font-weight: 700;
      color: #8f9bb3;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      margin-top: 6px;
    }

    /* Massive Primary DEPLOY CTA Button */
    .btn-deck-deploy {
      position: relative;
      width: 100%;
      padding: 20px 32px;
      background: linear-gradient(135deg, #c7ff72 0%, #a2e846 100%);
      color: #080a0f;
      border: none;
      clip-path: polygon(0 0, calc(100% - 16px) 0, 100% 16px, 100% 100%, 16px 100%, 0 calc(100% - 16px));
      font-family: "Rajdhani", "Barlow Condensed", sans-serif;
      font-size: 26px;
      font-weight: 900;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      gap: 4px;
      box-shadow: 0 8px 32px rgba(199, 255, 114, 0.3), inset 0 2px 0 rgba(255, 255, 255, 0.6);
      transition: all 0.15s ease;
      overflow: hidden;
    }

    .btn-deck-deploy:hover {
      background: linear-gradient(135deg, #d8ff8a 0%, #b4f757 100%);
      transform: translateY(-2px);
      box-shadow: 0 12px 40px rgba(199, 255, 114, 0.5), inset 0 2px 0 rgba(255, 255, 255, 0.8);
    }

    .btn-deck-deploy:active {
      transform: translateY(2px);
      box-shadow: 0 4px 16px rgba(199, 255, 114, 0.3);
    }

    .btn-deploy-main {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 28px;
      line-height: 1;
    }

    .btn-deploy-sub {
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.18em;
      color: #1e3302;
      opacity: 0.85;
    }

    /* Tactical Action Buttons */
    .deck-actions-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-top: 4px;
    }

    .btn-deck-action {
      width: 100%;
      padding: 14px 20px;
      background: rgba(19, 23, 34, 0.85);
      border: 1px solid #272f42;
      clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 10px, 100% 100%, 10px 100%, 0 calc(100% - 10px));
      color: #d1d5db;
      font-family: "Rajdhani", "Barlow Condensed", sans-serif;
      font-size: 14px;
      font-weight: 700;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      transition: all 0.12s ease;
    }

    .btn-deck-action:hover {
      background: #1b2130;
      border-color: #c7ff72;
      color: #ffffff;
      transform: translateX(4px);
      box-shadow: 0 0 16px rgba(199, 255, 114, 0.15);
    }

    .action-num {
      color: #c7ff72;
      font-weight: 800;
      margin-right: 12px;
    }

    .action-arrow {
      color: #8f9bb3;
      font-size: 16px;
      transition: transform 0.12s ease;
    }

    .btn-deck-action:hover .action-arrow {
      color: #c7ff72;
      transform: translateX(4px);
    }

    /* Right Column: Tactical Armor Spec Sheet & Hologram */
    .deck-right-col {
      display: flex;
      flex-direction: column;
    }

    .tactical-spec-card {
      background: rgba(14, 18, 27, 0.92);
      border: 1px solid #242c3d;
      border-top: 3px solid #c7ff72;
      clip-path: polygon(0 0, 100% 0, 100% calc(100% - 16px), calc(100% - 16px) 100%, 0 100%);
      padding: 24px 28px;
      display: flex;
      flex-direction: column;
      gap: 18px;
      box-shadow: 0 16px 48px rgba(0, 0, 0, 0.7);
    }

    .spec-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      border-bottom: 1px solid #242c3d;
      padding-bottom: 14px;
    }

    .spec-asset-tag {
      font-size: 11px;
      font-weight: 800;
      color: #c7ff72;
      letter-spacing: 0.18em;
      text-transform: uppercase;
    }

    .spec-asset-name {
      font-size: 28px;
      font-weight: 900;
      color: #ffffff;
      letter-spacing: 0.08em;
      margin-top: 2px;
    }

    .spec-status-pill {
      padding: 4px 10px;
      background: rgba(0, 255, 170, 0.12);
      border: 1px solid #00ffaa;
      border-radius: 4px;
      color: #00ffaa;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.12em;
    }

    /* Telemetry Grid */
    .spec-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 14px 20px;
    }

    .spec-item {
      display: flex;
      flex-direction: column;
      gap: 3px;
      background: rgba(8, 10, 15, 0.55);
      border-left: 2px solid #363e52;
      padding: 8px 12px;
      border-radius: 0 4px 4px 0;
    }

    .spec-label {
      font-size: 11px;
      font-weight: 800;
      color: #727e96;
      letter-spacing: 0.12em;
      text-transform: uppercase;
    }

    .spec-value {
      font-size: 13px;
      font-weight: 700;
      color: #e2e8f0;
      letter-spacing: 0.06em;
    }

    .spec-value.highlight {
      color: #c7ff72;
    }

    .spec-footer-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: rgba(199, 255, 114, 0.06);
      border: 1px solid rgba(199, 255, 114, 0.15);
      padding: 10px 14px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 800;
      color: #c7ff72;
      letter-spacing: 0.1em;
    }

    /* Bottom Command Deck Footer */
    .deck-footer {
      width: 100%;
      max-width: 1320px;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 18px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      padding-top: 14px;
      font-size: 12px;
      color: #717d96;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      box-sizing: border-box;
      flex-wrap: wrap;
    }

    .deck-footer span {
      color: #c7ff72;
      font-weight: 800;
      background: rgba(199, 255, 114, 0.1);
      border: 1px solid rgba(199, 255, 114, 0.25);
      padding: 2px 6px;
      border-radius: 3px;
      margin-right: 4px;
    }
\n"""

html = html[:pos_start] + deck_css + html[pos_end:]

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Successfully replaced home CSS with AAA Video Game Command Deck CSS!")
