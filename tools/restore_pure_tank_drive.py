with open("assets/B1Nq4Kq6.js", "r", encoding="utf-8") as f:
    code = f.read()

# Find our previous steering assist replacement
idx = code.find("// Camera-guided vehicle steering assist")
if idx != -1:
    end_idx = code.find("let u=s!==0||l!==0;", idx)
    if end_idx != -1:
        # Restore pure World War Tank WASD track driving
        clean_tank_drive = """// Pure World War Tank Track Driving (Hull independent from Turret)
// W = forward along hull, S = reverse along hull, A/D = track pivot steering
let u=s!==0||l!==0;"""
        code = code[:idx] + clean_tank_drive + code[end_idx + len("let u=s!==0||l!==0;"):]
        with open("assets/B1Nq4Kq6.js", "w", encoding="utf-8") as f:
            f.write(code)
        print("Restored pure World War Tank movement in B1Nq4Kq6.js!")
else:
    print("Could not find previous steering assist block in B1Nq4Kq6.js")
