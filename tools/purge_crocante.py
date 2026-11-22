html_path = r'C:\Users\Vrund Patel\Desktop\clone-game\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Remove Crocante @font-face
old_crocante_fontface = """    @font-face {
      font-family: "Crocante";
      src:
        url("/assets/fonts/Crocante-Medium.woff2") format("woff2"),
        url("/assets/fonts/Crocante-Medium.woff") format("woff");
      font-weight: 400 900;
      font-style: normal;
      font-display: swap;
      ascent-override: 115%;
      descent-override: 23%;
      line-gap-override: 0%;
    }"""

if old_crocante_fontface in html:
    html = html.replace(old_crocante_fontface, '')
    print("Removed Crocante @font-face")

# Remove Crocante preload
html = html.replace('<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/Crocante-Medium.woff2" crossorigin="anonymous" />', '')

# Replace dummy font loader
html = html.replace('<div class="font crocante" data-font="800 20px Crocante">&nbsp;</div>', '<div class="font rajdhani" data-font="700 20px Rajdhani">&nbsp;</div>')

# Ensure all Barlow fallbacks have Rajdhani or Barlow Condensed
html = html.replace('font-family: "Barlow", sans-serif;', 'font-family: "Rajdhani", "Barlow Condensed", -apple-system, sans-serif;')

# Ensure body and global font is sleek tactical
html = html.replace('font-family: "Barlow", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;', 'font-family: "Rajdhani", "Barlow Condensed", "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Purged Crocante and upgraded all font declarations successfully!")
