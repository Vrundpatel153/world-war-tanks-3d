with open(r'C:\Users\Vrund Patel\Desktop\clone-game\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('_tacticalCursor')
if idx != -1:
    print(text[idx-100:idx+400])
else:
    print("NOT FOUND!")
