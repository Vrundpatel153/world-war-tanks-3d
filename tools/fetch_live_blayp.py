import requests, re
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
r = requests.get('https://longhoang-lyo.com/assets/BlAypStk.js', headers=HEADERS)
print('BlAypStk status:', r.status_code)
for s in re.finditer(r'import\([^\)]+\)', r.text):
    print('import:', s.group(0))

for s in re.finditer(r'assets/[a-zA-Z0-9_\-]+\.js', r.text):
    print('asset JS in BlAypStk:', s.group(0))
