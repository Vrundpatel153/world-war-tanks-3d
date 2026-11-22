with open(r'C:\Users\Vrund Patel\Desktop\clone-game\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1255, min(len(lines), 1275)):
    print(f"{i+1}: {lines[i]}", end='')
