import os

total_files = 0
total_size = 0
ext_count = {}

for root, dirs, files in os.walk("."):
    if ".git" in root or "__pycache__" in root:
        continue
    for f in files:
        if f.endswith(".py"):
            continue
        p = os.path.join(root, f)
        try:
            sz = os.path.getsize(p)
            total_files += 1
            total_size += sz
            ext = os.path.splitext(f)[1].lower()
            if not ext:
                ext = "[no-ext]"
            ext_count[ext] = ext_count.get(ext, 0) + 1
        except Exception:
            pass

print(f"Total downloaded files: {total_files}")
print(f"Total size: {total_size / (1024 * 1024):.2f} MB")
print("\nFiles by extension:")
for ext, count in sorted(ext_count.items(), key=lambda x: -x[1]):
    print(f"  {ext}: {count}")
