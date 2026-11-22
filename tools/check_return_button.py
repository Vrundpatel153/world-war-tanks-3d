import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

matches = [m.start() for m in re.finditer(r'id=[\'"]btn-return-menu[\'"]', html)]
for pos in matches:
    print(html[pos-50:pos+250])
