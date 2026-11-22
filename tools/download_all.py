import os
import re
import sys
import json
import struct
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

BASE_URL = "https://longhoang-lyo.com"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://longhoang-lyo.com/",
    "Origin": "https://longhoang-lyo.com"
}

WORKSPACE = r"C:\Users\Vrund Patel\Desktop\clone-game"
os.chdir(WORKSPACE)

# Load URLs from DevTools network capture
devtools_outputs = [
    r"C:\Users\Vrund Patel\.gemini\antigravity\brain\5a8457f3-84ca-459d-b814-355d1a1198dc\.system_generated\steps\39\output.txt",
    r"C:\Users\Vrund Patel\.gemini\antigravity\brain\5a8457f3-84ca-459d-b814-355d1a1198dc\.system_generated\steps\63\output.txt"
]

initial_urls = set()

for output_file in devtools_outputs:
    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            for line in f:
                m = re.search(r'GET\s+(https?://[^\s]+)\s+\[(\d+)\]', line)
                if m:
                    initial_urls.add(m.group(1))

print(f"Loaded {len(initial_urls)} initial URLs from DevTools captures.")

# Additional known static assets from index.html
extra_assets = [
    "/favicon.ico",
    "/site.webmanifest",
    "/assets/elements/app-icon.svg",
    "/assets/elements/icon-192.png",
    "/assets/elements/hud/title-intro.svg",
    "/assets/elements/icons/secondary-settings.svg",
    "/assets/elements/hud/progress-bar.svg",
    "/assets/meta/og-preview.png",
    "/assets/fonts/Crocante-Medium.woff2",
    "/assets/fonts/Crocante-Medium.woff",
    "/assets/vYUQZzfX.js",
    "/assets/C0xwqhbh.js",
    "/assets/DrDnj3Lb.js",
    "/assets/BW6YWG0R.js",
    "/assets/Co_82n2H.js",
    "/assets/t1WzwXnd.js",
    "/assets/D9JAKPuk.js",
    "/assets/CozVMRND.js",
    "/assets/DADMk73e.js",
    "/assets/BcJjgNcx.css"
]

for p in extra_assets:
    initial_urls.add(urllib.parse.urljoin(BASE_URL, p))

# Queue and set of processed URLs
queued_urls = set(initial_urls)
downloaded_urls = set()
failed_urls = set()

session = requests.Session()
session.headers.update(HEADERS)

def url_to_local_path(url):
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc == "longhoang-lyo.com" or parsed.netloc == "":
        path = parsed.path
        if not path or path == "/":
            return "index.html"
        # strip leading slash
        path = path.lstrip("/")
        return os.path.normpath(path)
    elif "fonts.googleapis.com" in parsed.netloc or "fonts.gstatic.com" in parsed.netloc:
        # Save fonts into a fonts/ directory or keep track
        path = parsed.path.lstrip("/")
        return os.path.normpath(os.path.join("external", parsed.netloc, path))
    else:
        path = parsed.path.lstrip("/")
        return os.path.normpath(os.path.join("external", parsed.netloc, path))

def download_one(url):
    local_path = url_to_local_path(url)
    if os.path.exists(local_path) and os.path.getsize(local_path) > 0:
        return url, local_path, True, "Already exists"
    
    os.makedirs(os.path.dirname(local_path) if os.path.dirname(local_path) else ".", exist_ok=True)
    
    try:
        resp = session.get(url, timeout=30)
        if resp.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(resp.content)
            return url, local_path, True, len(resp.content)
        else:
            return url, local_path, False, f"HTTP {resp.status_code}"
    except Exception as e:
        return url, local_path, False, str(e)

def extract_urls_from_text(content, source_url):
    found = set()
    
    # 1. Look for asset strings: e.g. "assets/..." or "/assets/..."
    patterns = [
        r'["\'](/assets/[^"\'\s\?#]+)["\']',
        r'["\'](\.?/assets/[^"\'\s\?#]+)["\']',
        r'["\'](assets/[^"\'\s\?#]+)["\']',
        r'url\([\'"]?([^"\'\)]+)[\'"]?\)',
        r'href=[\'"]?([^"\'\s>]+)[\'"]?',
        r'src=[\'"]?([^"\'\s>]+)[\'"]?',
        r'["\']([a-zA-Z0-9_\-\/]+\.(?:glb|gltf|bin|ktx2|png|jpg|jpeg|webp|svg|mp3|wav|ogg|wasm|woff2|woff|ttf|json|css|js))["\']'
    ]
    
    for pat in patterns:
        for match in re.findall(pat, content):
            match = match.strip()
            if match.startswith("data:") or match.startswith("blob:") or match.startswith("#"):
                continue
            # Build full URL
            if match.startswith("http://") or match.startswith("https://"):
                if "longhoang-lyo.com" in match or "fonts.gstatic.com" in match:
                    found.add(match)
            else:
                full_url = urllib.parse.urljoin(BASE_URL, match)
                found.add(full_url)
                
    return found

def extract_urls_from_glb(filepath):
    found = set()
    try:
        with open(filepath, "rb") as f:
            header = f.read(12)
            if len(header) < 12:
                return found
            magic, version, length = struct.unpack("<4sII", header)
            if magic != b"glTF":
                return found
            # Read first chunk (JSON chunk)
            chunk_header = f.read(8)
            if len(chunk_header) < 8:
                return found
            chunk_length, chunk_type = struct.unpack("<II", chunk_header)
            if chunk_type == 0x4E4F534A: # JSON
                json_bytes = f.read(chunk_length)
                json_str = json_bytes.decode("utf-8", errors="ignore")
                data = json.loads(json_str)
                # Check buffers
                for buf in data.get("buffers", []):
                    if "uri" in buf:
                        found.add(urllib.parse.urljoin(BASE_URL + "/assets/", buf["uri"]))
                # Check images
                for img in data.get("images", []):
                    if "uri" in img:
                        found.add(urllib.parse.urljoin(BASE_URL + "/assets/", img["uri"]))
    except Exception as e:
        pass
    return found

print(f"Starting initial download queue with {len(queued_urls)} URLs...")

scanned_files = set()

while queued_urls:
    current_batch = list(queued_urls)
    queued_urls.clear()
    
    print(f"\n--- Processing batch of {len(current_batch)} URLs ---")
    with ThreadPoolExecutor(max_workers=12) as executor:
        futures = {executor.submit(download_one, u): u for u in current_batch}
        for future in as_completed(futures):
            u = futures[future]
            try:
                url, local_path, success, info = future.result()
                if success:
                    downloaded_urls.add(url)
                    print(f"[OK] {url} -> {local_path} ({info})")
                else:
                    failed_urls.add(url)
                    print(f"[FAIL] {url}: {info}")
            except Exception as exc:
                failed_urls.add(u)
                print(f"[ERROR] {u}: {exc}")
                
    # Now scan downloaded files for new links
    print("\nScanning files for referenced assets...")
    newly_discovered = set()
    for root, dirs, files in os.walk("."):
        if ".git" in root or "node_modules" in root:
            continue
        for file in files:
            filepath = os.path.join(root, file)
            if filepath in scanned_files:
                continue
            scanned_files.add(filepath)
            
            ext = os.path.splitext(file)[1].lower()
            if ext in [".js", ".css", ".html", ".json", ".webmanifest"]:
                try:
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                    found = extract_urls_from_text(content, BASE_URL)
                    for u in found:
                        if u not in downloaded_urls and u not in failed_urls and u not in queued_urls:
                            newly_discovered.add(u)
                except Exception as e:
                    pass
            elif ext == ".glb":
                found = extract_urls_from_glb(filepath)
                for u in found:
                    if u not in downloaded_urls and u not in failed_urls and u not in queued_urls:
                        newly_discovered.add(u)
                        
    print(f"Discovered {len(newly_discovered)} new URLs from scanned files.")
    queued_urls.update(newly_discovered)

print(f"\n================ DOWNLOAD FINISHED ================")
print(f"Total downloaded: {len(downloaded_urls)}")
print(f"Total failed: {len(failed_urls)}")
if failed_urls:
    print("Failed URLs:")
    for f in failed_urls:
        print("  -", f)
