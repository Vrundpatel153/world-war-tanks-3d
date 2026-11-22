import re

with open("assets/B1Nq4Kq6.js", "r", encoding="utf-8") as f:
    code = f.read()

# Look for robot update / movement
keywords = ["currentLeftSpeed", "currentRightSpeed", "keyboard", "input", "steering", "moveForward", "moveBackward"]
for kw in keywords:
    matches = [m.start() for m in re.finditer(re.escape(kw), code)]
    print(f"Keyword '{kw}': {len(matches)} occurrences")
    for idx in matches[:2]:
        start = max(0, idx - 100)
        end = min(len(code), idx + 200)
        print(f"   ...{code[start:end].strip()}...")
