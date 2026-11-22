with open(r'C:\Users\Vrund Patel\Desktop\clone-game\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1370, min(len(lines), 1410)):
    print(f"{i+1}: {lines[i]}", end='')
