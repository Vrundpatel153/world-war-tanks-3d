with open(r'C:\Users\Vrund Patel\Desktop\clone-game\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('.menu-modal-overlay {')
if idx == -1:
    idx = text.find('.menu-modal-overlay{')
if idx != -1:
    print(text[idx:idx+350])
else:
    print("NOT FOUND")
