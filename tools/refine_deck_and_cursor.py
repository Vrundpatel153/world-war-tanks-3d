import re

html_path = r'C:\Users\Vrund Patel\Desktop\clone-game\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Make initial cursor position visible at center of screen
html = html.replace(
    'transform: translate3d(-100px, -100px, 0);',
    'transform: translate3d(50vw, 50vh, 0);'
)

# Also ensure on smaller laptop screens (under 1200px), deck-body scales gracefully
responsive_deck_css = """    @media (max-width: 1200px) {
      .deck-body {
        grid-template-columns: 380px 1fr !important;
        gap: 24px !important;
      }
      .deck-hero-title {
        font-size: 44px !important;
      }
      .spec-asset-name {
        font-size: 22px !important;
      }
      .spec-grid {
        gap: 10px 14px !important;
      }
    }

    @media (max-height: 800px) {
      #game-home-screen {
        padding: 18px 36px 14px 36px !important;
      }
      .deck-hero-title {
        font-size: 40px !important;
      }
      .btn-deck-deploy {
        padding: 14px 24px !important;
      }
      .btn-deck-action {
        padding: 10px 16px !important;
      }
      .tactical-spec-card {
        padding: 16px 20px !important;
        gap: 12px !important;
      }
    }
"""

if '@media (max-width: 1200px)' not in html:
    pos_deck_end = html.find('/* Bottom Command Deck Footer */')
    if pos_deck_end != -1:
        html = html[:pos_deck_end] + responsive_deck_css + "\n    " + html[pos_deck_end:]
        print("Added responsive scaling for laptop screens")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated index.html successfully!")
