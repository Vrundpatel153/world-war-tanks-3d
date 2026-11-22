with open('assets/B1Nq4Kq6.js', 'r', encoding='utf-8', errors='ignore') as f:
    code = f.read()

pos_steer = code.find('if(s>0){l=-l;}')
print('Steering pos:', pos_steer)
if pos_steer != -1:
    print(code[pos_steer-40:pos_steer+60])

pos_cull = code.find('isInstancedTransformVisible')
print('Cull pos:', pos_cull)
if pos_cull != -1:
    print(code[pos_cull:pos_cull+350])
