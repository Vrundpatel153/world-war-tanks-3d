import re

html_path = r'C:\Users\Vrund Patel\Desktop\clone-game\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace .settings-tabs-bar and .settings-tab-btn CSS
old_tabs_css = """    /* Settings Modal Navigation Tabs */
    .settings-tabs-bar {
      display: flex;
      gap: 8px;
      border-bottom: 2px solid #272935;
      padding-bottom: 12px;
      margin-bottom: 16px;
      overflow-x: auto;
    }

    .settings-tab-btn {
      background: #11121a;
      border: 1px solid #272935;
      color: #8f93a5;
      font-family: "Barlow", sans-serif;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      padding: 8px 16px;
      border-radius: 6px;
      transition: all 0.15s ease;
      white-space: nowrap;
    }"""

new_tabs_css = """    /* Settings Modal Navigation Tabs */
    .settings-tabs-bar {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 8px;
      border-bottom: 2px solid #272935;
      padding-bottom: 12px;
      margin-bottom: 16px;
      overflow: visible;
    }

    .settings-tab-btn {
      background: #11121a;
      border: 1px solid #272935;
      color: #8f93a5;
      font-family: "Barlow", sans-serif;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      padding: 10px 6px;
      border-radius: 6px;
      transition: all 0.15s ease;
      white-space: nowrap;
      display: flex;
      align-items: center;
      justify-content: center;
      box-sizing: border-box;
      width: 100%;
    }"""

if old_tabs_css in html:
    html = html.replace(old_tabs_css, new_tabs_css)
    print("Replaced tabs CSS with grid layout")
else:
    print("Warning: old_tabs_css not found exactly")

# Add custom scrollbars for .menu-modal
old_menu_modal = """    .menu-modal {
      background: #191b24;
      border: 2px solid #272935;
      border-radius: 12px;
      width: 100%;
      max-width: 560px;
      padding: 28px 32px;
      box-shadow: 0 20px 48px rgba(0, 0, 0, 0.75);
      display: flex;
      flex-direction: column;
      gap: 20px;
      color: #dfdfe2;
      font-family: "Barlow", sans-serif;
    }"""

new_menu_modal = """    .menu-modal {
      background: #191b24;
      border: 2px solid #272935;
      border-radius: 12px;
      width: 100%;
      max-width: 560px;
      padding: 28px 32px;
      box-shadow: 0 20px 48px rgba(0, 0, 0, 0.75);
      display: flex;
      flex-direction: column;
      gap: 20px;
      color: #dfdfe2;
      font-family: "Barlow", sans-serif;
      box-sizing: border-box;
      scrollbar-width: thin;
      scrollbar-color: #272935 #11121a;
    }

    .menu-modal::-webkit-scrollbar {
      width: 6px;
    }
    .menu-modal::-webkit-scrollbar-track {
      background: #11121a;
      border-radius: 4px;
    }
    .menu-modal::-webkit-scrollbar-thumb {
      background: #272935;
      border-radius: 4px;
    }
    .menu-modal::-webkit-scrollbar-thumb:hover {
      background: #c7ff72;
    }"""

if old_menu_modal in html:
    html = html.replace(old_menu_modal, new_menu_modal)
    print("Added custom scrollbar styles to .menu-modal")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved index.html successfully!")
