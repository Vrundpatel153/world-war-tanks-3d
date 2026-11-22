import os
import requests

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://longhoang-lyo.com/",
    "Origin": "https://longhoang-lyo.com"
})

BASE_URL = "https://longhoang-lyo.com"

# Check combinations of art characters
chars = ["player", "fodder", "boss", "npc"]
directions = ["left", "right", "front", "back"]
states = ["active", "inactive"]

urls_to_test = [
    "/assets/work/thumbnail/locked-thumb.ktx2"
]

for c in chars:
    for d in directions:
        for s in states:
            urls_to_test.append(f"/assets/art/characters/{c}-{d}-{s}.webp")
            urls_to_test.append(f"/assets/art/characters/{c}-{d}-{s}.png")
            urls_to_test.append(f"/assets/art/characters/{c}-{s}.webp")

# Ambient loops
for time in ["morning", "noon", "afternoon", "evening", "day", "night", "dawn", "dusk"]:
    urls_to_test.append(f"/assets/audio/ambient/{time}-loop.mp3")
    urls_to_test.append(f"/assets/audio/ambient/{time}.mp3")

# Sound effects
sfx_categories = ["object", "vfx", "grab-mode", "ui", "character", "vehicle"]
for cat in sfx_categories:
    for num in range(1, 10):
        urls_to_test.append(f"/assets/audio/sfx/{cat}/click-0{num}.mp3")
        urls_to_test.append(f"/assets/audio/sfx/{cat}/switch-0{num}.mp3")
        urls_to_test.append(f"/assets/audio/sfx/{cat}/victory-0{num}.mp3")
        urls_to_test.append(f"/assets/audio/sfx/{cat}/hit-0{num}.mp3")

print(f"Testing {len(urls_to_test)} candidate asset URLs...")

found = 0
for path in urls_to_test:
    url = BASE_URL + path
    local_path = os.path.normpath(path.lstrip("/"))
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        continue
    try:
        r = session.get(url, timeout=10)
        if r.status_code == 200:
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            with open(local_path, "wb") as fp:
                fp.write(r.content)
            print(f"[FOUND & DOWNLOADED] {url} ({len(r.content)} bytes)")
            found += 1
    except Exception as e:
        pass

print(f"Done. Found {found} new asset files.")
