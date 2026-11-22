import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Check for script tags
for m in re.finditer(r'<script[^>]*src=[\'"]([^\'"]+)[\'"]', html):
    print('Found script:', m.group(0))

# Add version query string to assets scripts if not present
def add_ver(match):
    src = match.group(1)
    if '?' in src:
        src = src.split('?')[0]
    return f'src="{src}?v=2.6.0"'

new_html = re.sub(r'src=[\'"](/assets/[^\'"]+\.js(?:\?[^\'"]*)?)[\'"]', add_ver, html)

if new_html != html:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Added ?v=2.6.0 to asset script tags!")
else:
    print("Asset script tags already up to date.")
