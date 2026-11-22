import os

print("Checking binary files for fake HTML fallbacks...")
fake_files = []

binary_exts = {".glb", ".ktx2", ".wasm", ".mp3", ".mp4", ".webm", ".bin", ".woff", ".woff2", ".png", ".webp", ".ico"}

for root, dirs, files in os.walk("."):
    if ".git" in root or "__pycache__" in root:
        continue
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in binary_exts:
            p = os.path.join(root, f)
            try:
                with open(p, "rb") as fp:
                    head = fp.read(50)
                if b"<!doctype" in head.lower() or b"<html" in head.lower():
                    fake_files.append((p, os.path.getsize(p)))
            except Exception as e:
                pass

print(f"Total fake binary files found: {len(fake_files)}")
for p, sz in fake_files:
    print(f"  {p} ({sz} bytes)")
