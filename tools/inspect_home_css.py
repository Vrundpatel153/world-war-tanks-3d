with open(r'C:\Users\Vrund Patel\Desktop\clone-game\index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '.home-center {' in l:
        print(f"Center CSS at line {i+1}:")
        for j in range(i, min(len(lines), i + 85)):
            print(f"{j+1}: {lines[j]}", end='')
        break
