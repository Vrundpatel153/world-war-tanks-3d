import os
import re

print("Auditing JS for WASM, Draco, Basis, KTX2, Audio, Models, etc.")

for root, dirs, files in os.walk("assets"):
    for f in files:
        if f.endswith(".js"):
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8", errors="ignore") as fp:
                c = fp.read()
            
            # Check for paths and file names
            matches = re.findall(r'["\']([^"\'\s\?#<>]+?\.(?:wasm|bin|glb|gltf|ktx2|mp3|webm|mp4|png|webp|svg))["\']', c)
            if matches:
                print(f"\nIn {f}:")
                for m in set(matches):
                    # Check if file exists locally
                    local_p = m.lstrip("/").replace("/", os.sep)
                    exists = os.path.exists(local_p)
                    print(f"  {'[EXISTS]' if exists else '[MISSING]'} {m} (local: {local_p})")
