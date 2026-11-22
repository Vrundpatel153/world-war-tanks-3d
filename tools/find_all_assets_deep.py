import os
import re
import urllib.parse
import requests

BASE_URL = "https://longhoang-lyo.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://longhoang-lyo.com/",
    "Origin": "https://longhoang-lyo.com"
}

session = requests.Session()
session.headers.update(HEADERS)

print("Starting deep scan of all JS, CSS, and HTML files for any asset paths...")

candidates = set()

# Regex to find any string containing asset paths or extensions
# Examples: /assets/videos/bts-page-1080p.mp4, model/object/forklift.glb, /audio/..., etc.
patterns = [
    r'/(assets/[a-zA-Z0-9_\-\./]+\.(?:mp4|webm|glb|gltf|bin|ktx2|png|jpg|jpeg|webp|svg|mp3|wav|ogg|wasm|woff2|woff|ttf|json|css|js))',
    r'["\']((?:assets|model|basis|draco|audio)/[a-zA-Z0-9_\-\./]+\.(?:mp4|webm|glb|gltf|bin|ktx2|png|jpg|jpeg|webp|svg|mp3|wav|ogg|wasm|woff2|woff|ttf|json|css|js))["\']',
    r'["\'](/[a-zA-Z0-9_\-\./]+\.(?:mp4|webm|glb|gltf|bin|ktx2|png|jpg|jpeg|webp|svg|mp3|wav|ogg|wasm|woff2|woff|ttf|json|css|js))["\']',
    r'([a-zA-Z0-9_\-]+/[a-zA-Z0-9_\-\./]+\.(?:mp4|webm|glb|gltf|bin|ktx2|png|jpg|jpeg|webp|svg|mp3|wav|ogg|wasm|woff2|woff|ttf|json|css|js))',
    r'/assets/([a-zA-Z0-9_\-\./]+)',
]

for root, dirs, files in os.walk("."):
    if ".git" in root or "__pycache__" in root or "external" in root:
        continue
    for f in files:
        if f.endswith((".js", ".css", ".html", ".json")):
            p = os.path.join(root, f)
            try:
                with open(p, "r", encoding="utf-8", errors="ignore") as fp:
                    content = fp.read()
                
                # Check for video files explicitly
                for v in re.findall(r'/assets/videos/[a-zA-Z0-9_\-\.]+', content):
                    candidates.add(v)
                
                # General regex
                for pat in patterns:
                    for match in re.findall(pat, content):
                        if isinstance(match, tuple):
                            match = match[0]
                        match = match.strip()
                        if any(c in match for c in [' ', '<', '>', '{', '}', '$', '`', ';', '(', ')', '[', ']', '\\', '"', "'"]):
                            continue
                        if match.startswith("http"):
                            continue
                        # sanitize
                        if not match.startswith("/"):
                            match = "/" + match
                        candidates.add(match)
            except Exception:
                pass

print(f"Found {len(candidates)} potential asset paths.")

downloaded = 0
already_exists = 0
failed = 0

for path in sorted(candidates):
    # Clean up path
    clean_path = path.lstrip("/")
    # Filter out obvious false positives
    if not clean_path or clean_path.count("/") == 0 and "." not in clean_path:
        continue
    
    local_path = os.path.normpath(clean_path)
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        already_exists += 1
        continue
    
    # Try downloading
    url = urllib.parse.urljoin(BASE_URL, path)
    try:
        resp = session.get(url, timeout=15)
        if resp.status_code == 200:
            os.makedirs(os.path.dirname(local_path) if os.path.dirname(local_path) else ".", exist_ok=True)
            with open(local_path, "wb") as f:
                f.write(resp.content)
            downloaded += 1
            print(f"[DOWNLOADED] {url} -> {local_path} ({len(resp.content)} bytes)")
        else:
            failed += 1
            # print(f"[404] {url}")
    except Exception as e:
        failed += 1
        print(f"[ERROR] {url}: {e}")

print(f"\nScan complete: {already_exists} existing, {downloaded} newly downloaded, {failed} 404/failed.")
