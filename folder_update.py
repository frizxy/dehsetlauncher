import os, hashlib, json, requests, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
TARGET_PATHS = [
    "mods",
    "shaderpacks",
    "resourcepacks",
    "versions",
    "launcher.exe",
    "launch.py",
    "zerotierconnection.py",
    "launcher.py",
    "launcher.qss"
    "launcher_assets"
]

MANIFEST_URL = "https://raw.githubusercontent.com/frizxy/dehsetlauncher/refs/heads/main/manifest.json"
LOCAL_MANIFEST = os.path.join(ROOT, "manifest.json")

def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()

def load_manifest(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def download_file(url, local_path):
    r = requests.get(url, stream=True)
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, "wb") as f:
        shutil.copyfileobj(r.raw, f)

def check_files_update():
    # 1. Remote manifest indir
    r = requests.get(MANIFEST_URL)
    remote_manifest = r.json()

    # 2. Local manifest yükle
    local_manifest = load_manifest(LOCAL_MANIFEST)

    # 3. Değişen dosyaları kontrol et
    for rel_path, remote_hash in remote_manifest.items():
        local_path = os.path.join(ROOT, rel_path)
        if not os.path.exists(local_path) or file_hash(local_path) != remote_hash:
            print(f"[UPDATE] {rel_path} güncelleniyor...")
            download_file(f"https://github.com/frizxy/dehsetlauncher/raw/refs/heads/main/{rel_path}", local_path)
        else:
            print(f"[OK] {rel_path} güncel.")

    # 4. Local manifesti güncelle
    with open(LOCAL_MANIFEST, "w") as f:
        json.dump(remote_manifest, f, indent=4)

    print("[UPDATE] Tüm dosyalar kontrol edildi.")