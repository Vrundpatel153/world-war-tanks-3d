with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

old_dismiss = """      function dismissLoaderAndShowMenu() {
        const intro = document.getElementById('startup-intro');
        if (intro && !intro.classList.contains('loading-dismissed')) {
          intro.classList.add('loading-dismissed');
          setTimeout(() => {
            intro.style.display = 'none';
          }, 450);
        }
        const menu = document.getElementById('game-home-screen');
        if (menu) {
          menu.classList.remove('menu-hidden');
        }
      }"""

new_dismiss = """      function dismissLoaderAndShowMenu() {
        if (window._hasDismissedLoader) return;
        window._hasDismissedLoader = true;
        const intro = document.getElementById('startup-intro');
        if (intro && !intro.classList.contains('loading-dismissed')) {
          intro.classList.add('loading-dismissed');
          setTimeout(() => {
            intro.style.display = 'none';
          }, 450);
        }
        if (!window._hasStartedGame) {
          window.openGameMenu();
        }
      }"""

if old_dismiss in html:
    html = html.replace(old_dismiss, new_dismiss)
    print("Replaced dismissLoaderAndShowMenu successfully")
else:
    print("Warning: old_dismiss not found")

# Also add window._hasStartedGame = true to startGameFromMenu
old_start = """      window.startGameFromMenu = function() {
        window.isGameMenuOpen = false;"""

new_start = """      window.startGameFromMenu = function() {
        window.isGameMenuOpen = false;
        window._hasStartedGame = true;"""

if old_start in html:
    html = html.replace(old_start, new_start)
    print("Added _hasStartedGame flag to startGameFromMenu")
else:
    print("Warning: old_start not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("index.html updated.")
