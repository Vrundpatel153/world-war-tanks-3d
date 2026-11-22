import requests
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
r = requests.get('https://longhoang-lyo.com/assets/B1Nq4Kq6.js', headers=HEADERS)
print('Status:', r.status_code)
print('First 1000 chars:')
print(r.text[:1000])
with open('assets/B1Nq4Kq6.remote.js', 'w', encoding='utf-8') as f:
    f.write(r.text)
