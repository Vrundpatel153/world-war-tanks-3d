import re

html_path = r'C:\Users\Vrund Patel\Desktop\clone-game\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add id="btn-home-play-txt" to the Play button span
html = html.replace(
    '<button class="btn-home-play" onclick="window.startGameFromMenu()">\n            <span>▶ PLAY</span>\n          </button>',
    '<button class="btn-home-play" onclick="window.startGameFromMenu()">\n            <span id="btn-home-play-txt">▶ PLAY</span>\n          </button>'
)

# 2. Add white-space: nowrap to .tank-controls-bar
html = html.replace(
    '.tank-controls-bar {\n      position: absolute;\n      bottom: 12px;\n      left: 50%;\n      transform: translateX(-50%);\n      font-size: 11px;\n      color: rgba(255, 255, 255, 0.6);\n      background: rgba(0, 0, 0, 0.5);\n      padding: 4px 14px;\n      border-radius: 20px;\n      letter-spacing: 0.06em;\n    }',
    '.tank-controls-bar {\n      position: absolute;\n      bottom: 12px;\n      left: 50%;\n      transform: translateX(-50%);\n      font-size: 11px;\n      color: rgba(255, 255, 255, 0.8);\n      background: rgba(17, 18, 26, 0.85);\n      border: 1px solid #272935;\n      padding: 5px 16px;\n      border-radius: 20px;\n      letter-spacing: 0.06em;\n      white-space: nowrap;\n      z-index: 100;\n    }'
)

# 3. In openGameMenu & startGameFromMenu: Update pause badge
html = html.replace(
    "const playBtnTxt = document.querySelector('#btn-home-play-txt');\n        if (playBtnTxt) playBtnTxt.textContent = '▶ RESUME BATTLE';",
    "const playBtnTxt = document.querySelector('#btn-home-play-txt');\n        if (playBtnTxt) playBtnTxt.textContent = '▶ RESUME BATTLE';\n        const badge = document.querySelector('.home-badge');\n        if (badge) badge.textContent = '• ⏸️ COMBAT SIMULATION PAUSED •';"
)

html = html.replace(
    "window.startGameFromMenu = function() {\n        window.isGameMenuOpen = false;",
    "window.startGameFromMenu = function() {\n        window.isGameMenuOpen = false;\n        const badge = document.querySelector('.home-badge');\n        if (badge) badge.textContent = '• COMBAT SIMULATOR - FREE ROAM ALPHA •';"
)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Applied final UI polish successfully!")
