with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

target = "let reloadTimer = 0;"
replacement = """let reloadTimer = 0;

        // Auto dismiss intro overlay upon enter click
        document.addEventListener('click', function(e) {
          const btn = e.target.closest('.startup-intro__enter');
          if (btn) {
            const intro = document.querySelector('.startup-intro');
            if (intro) {
              intro.classList.add('startup-intro--dismissed');
              intro.style.display = 'none';
            }
          }
        });"""

if target in c and "Auto dismiss intro overlay" not in c:
    c = c.replace(target, replacement, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Enhanced HUD script with auto-dismiss")
else:
    print("Already enhanced or target not found")
