import glob
import difflib
import re

with open('index.html', 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

print('=== SCRIPT TAGS IN INDEX.HTML ===')
for m in re.finditer(r'<script[^>]*src=["\']([^"\']+)["\']', html):
    print(m.group(0))

print('\n=== SCRIPT TAGS MODULEPRELOAD ===')
for m in re.finditer(r'<link[^>]*href=["\']([^"\']+\.js[^"\']*)["\']', html):
    print(m.group(0))

print('\n=== CHECKING MODIFIED JS FILES VS BAK ===')
for bak in glob.glob('assets/*.bak'):
    orig = bak[:-4]
    print(f'Checking {orig} vs {bak}')
    try:
        with open(orig, 'r', encoding='utf-8', errors='ignore') as f1, open(bak, 'r', encoding='utf-8', errors='ignore') as f2:
            s1, s2 = f1.read(), f2.read()
        if s1 != s2:
            print(f'  DIFFERENCE FOUND in {orig}! Lengths: {len(s1)} vs {len(s2)}')
            diffs = list(difflib.unified_diff(s2.splitlines(), s1.splitlines(), lineterm=''))
            for diff in diffs[:15]:
                if diff.startswith(('+', '-')):
                    print('   ', diff[:120])
        else:
            print(f'  Identical')
    except Exception as e:
        print(f'  Error: {e}')
