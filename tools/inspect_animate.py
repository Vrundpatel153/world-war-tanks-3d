with open("assets/CQl67Veh.js", "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find("this.onEvent(`animate`")
if idx != -1:
    print(code[idx:idx+2500])
