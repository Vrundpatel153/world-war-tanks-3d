import re

with open("assets/CQl67Veh.js", "r", encoding="utf-8") as f:
    code = f.read()

# Let's inspect constructor
m = re.search(r'constructor\s*\((.*?)\)\s*\{(.*?)\}\s*init', code, re.DOTALL)
if m:
    print("Constructor arguments:", m.group(1))
    print("Constructor body (first 1000 chars):")
    print(m.group(2)[:1000])

# Let's inspect methods and their order
method_matches = re.finditer(r'([a-zA-Z0-9_$]+)\s*\((.*?)\)\s*\{', code)
print("\n--- Methods in class ---")
for mm in method_matches:
    name = mm.group(1)
    args = mm.group(2)
    # filter out js keywords
    if name not in ['if', 'for', 'while', 'switch', 'catch', 'function']:
        print(f"  {name}({args})")
