import os
import re

for filename in ["assets/B1Nq4Kq6.js", "assets/CQl67Veh.js"]:
    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    print(f"\n=== {filename} ({len(content)} bytes) ===")
    
    # Search for camera instances or camera follow methods
    keywords = ["camera.position", "lookAt", "orbit", "distance", "fov", "lerp", "targetPosition", "followTarget", "cameraOffset"]
    for kw in keywords:
        matches = [m.start() for m in re.finditer(re.escape(kw), content, re.IGNORECASE)]
        print(f"Keyword '{kw}': {len(matches)} occurrences")
        for idx in matches[:3]:
            start = max(0, idx - 60)
            end = min(len(content), idx + 100)
            print(f"   ...{content[start:end].strip()}...")
