with open(r'C:\Users\Vrund Patel\Desktop\clone-game\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for i, l in enumerate(text.splitlines()):
    if 'btn-return-menu' in l or 'MENU' in l or '⚙' in l:
        print(f"{i+1}: {l.strip()[:100]}")
