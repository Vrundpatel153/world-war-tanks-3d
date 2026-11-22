import os
import re

keywords = [
    "Long Hoang", "Lyo", "Designer & Developer", "Nam Tu Liem", "longhoang.0816",
    "2300+", "AI prompt", "Hanzii", "Mazii", "Todaii", "Niubii", "Behance",
    "LET'S COLLAB", "collab", "case-study", "statue-page", "about-page",
    "meet the creator", "Skip gameplay", "view-mode"
]

results = {k: [] for k in keywords}

for root, dirs, files in os.walk("."):
    if ".git" in root or "__pycache__" in root or "tools" in root or root.endswith(".bak"):
        continue
    for f in files:
        if f.endswith((".html", ".js", ".css", ".json", ".webmanifest")):
            p = os.path.join(root, f)
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as fp:
                    content = fp.read()
                for kw in keywords:
                    if kw.lower() in content.lower():
                        results[kw].append(p)
            except Exception:
                pass

print("=== PORTFOLIO AUDIT REPORT ===")
for kw, matched_files in results.items():
    print(f"\nKeyword: '{kw}' ({len(matched_files)} files)")
    for f in matched_files[:8]:
        print(f"  - {f}")
