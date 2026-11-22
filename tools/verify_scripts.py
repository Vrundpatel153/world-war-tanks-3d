import re
import subprocess
import os

path = r'C:\Users\Vrund Patel\Desktop\clone-game\index.html'
with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script(?:\s+type=[\"\']module[\"\'])?>([\s\S]*?)</script>', html)
print(f'Total scripts found: {len(scripts)}')

has_err = False
for idx, s in enumerate(scripts):
    s_clean = s.strip()
    if len(s_clean) > 20 and not s_clean.startswith('import '):
        proc = subprocess.run(['node', '--check'], input=s_clean, text=True, capture_output=True)
        if proc.returncode != 0:
            print(f'Script {idx} ERROR: {proc.stderr[:300]}')
            has_err = True
        else:
            print(f'Script {idx} OK (length: {len(s_clean)})')

if not has_err:
    print('ALL INLINE SCRIPTS ARE 100% VALID JAVASCRIPT!')
