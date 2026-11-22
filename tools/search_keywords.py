import os
import re

print("Searching for wasm, draco, basis across all downloaded files...")

for root, dirs, files in os.walk("."):
    if ".git" in root or "__pycache__" in root:
        continue
    for f in files:
        if f.endswith((".js", ".html", ".css", ".json")):
            p = os.path.join(root, f)
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as fp:
                    lines = fp.readlines()
                for idx, line in enumerate(lines):
                    for keyword in ["draco", "basis", ".wasm", "worker"]:
                        if keyword in line.lower():
                            # print excerpt around match
                            idx_pos = line.lower().find(keyword)
                            start = max(0, idx_pos - 80)
                            end = min(len(line), idx_pos + 120)
                            print(f"{p}:{idx+1} [{keyword}]: ...{line[start:end].strip()}...")
            except Exception as e:
                pass
