import requests, re
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
r = requests.get('https://longhoang-lyo.com/', headers=HEADERS)
print('Live status:', r.status_code)
for s in re.finditer(r'<script[^>]*src="([^"]+)"', r.text):
    print('src:', s.group(1))

# Also search for B1N or world bundle in live text
for s in re.finditer(r'assets/[a-zA-Z0-9_\-]+\.js', r.text):
    print('asset JS:', s.group(0))
