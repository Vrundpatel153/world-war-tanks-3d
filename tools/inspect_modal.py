with open(r'C:\Users\Vrund Patel\Desktop\clone-game\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('modal-options')
pos_end = text.find('// CLEAN SEPARATION', pos)
print('Length of modal section:', pos_end - pos)
print(text[pos:pos_end])
