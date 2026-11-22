with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

old_cur_sel = """    body.in-menu-mode,
    body.in-menu-mode * {"""

new_cur_sel = """    body.in-menu-mode,
    body.in-menu-mode *,
    #game-home-screen,
    #game-home-screen *,
    .menu-modal-overlay,
    .menu-modal-overlay * {"""

if old_cur_sel in html:
    html = html.replace(old_cur_sel, new_cur_sel, 1)
    print("Expanded default cursor selector")

old_ptr_sel = """    body.in-menu-mode button,
    body.in-menu-mode a,
    body.in-menu-mode input,
    body.in-menu-mode select,
    body.in-menu-mode .btn-deck-deploy,
    body.in-menu-mode .btn-deck-action,
    body.in-menu-mode .preset-card,
    body.in-menu-mode .settings-tab-btn,
    body.in-menu-mode .opt-btn,
    body.in-menu-mode .menu-modal-close,
    body.in-menu-mode [role="button"] {"""

new_ptr_sel = """    body.in-menu-mode button,
    body.in-menu-mode a,
    body.in-menu-mode input,
    body.in-menu-mode select,
    body.in-menu-mode .btn-deck-deploy,
    body.in-menu-mode .btn-deck-action,
    body.in-menu-mode .preset-card,
    body.in-menu-mode .settings-tab-btn,
    body.in-menu-mode .opt-btn,
    body.in-menu-mode .menu-modal-close,
    body.in-menu-mode [role="button"],
    #game-home-screen button,
    #game-home-screen [role="button"],
    .menu-modal-overlay button,
    .menu-modal-overlay [role="button"],
    .menu-modal-overlay input,
    .menu-modal-overlay select {"""

if old_ptr_sel in html:
    html = html.replace(old_ptr_sel, new_ptr_sel, 1)
    print("Expanded pointer cursor selector")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Updated index.html cursor selectors.")
