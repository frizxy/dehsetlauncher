import os, hashlib, json, requests, shutil

import os
import hashlib
import json
import requests
import shutil


ROOT = os.path.dirname(os.path.abspath(__file__))


TARGET_PATHS = [
    "mods",
    "shaderpacks",
    "resourcepacks",
    "zerotierconnection.py",
    "launcher.qss",
    "launcher.py",
    "firstpage.qss",
    "firstpage.py",
    "launch.py",
    "launcher_assets"
]


MANIFEST_URL = "https://raw.githubusercontent.com/frizxy/dehsetlauncher/main/manifest.json"


LOCAL_MANIFEST = os.path.join(ROOT, "manifest.json")


TEXT_EXTENSIONS = {".py", ".qss", ".txt", ".json"}


def file_hash(path):
    h = hashlib.sha256()
    # Read raw bytes in chunks (no newline normalization) to match manifest generation
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()



def load_manifest(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}



def download_file(url, local_path):
    """Download a remote file and write raw bytes to disk (chunked).

    Always write binary contents to preserve exact bytes so hashes match.
    """
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    try:
        r = requests.get(url, stream=True, timeout=30)
        r.raise_for_status()
    except Exception as e:
        update_label = (f"[ERROR] İndirme hatası: {url} -> {e}")
        raise

    with open(local_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)


def check_files_update(queue):
    queue.put("Dosyalar kontrol ediliyor...")
    
    # 1. Remote manifest indir
    try:
        r = requests.get(MANIFEST_URL, timeout=30)
        r.raise_for_status()
        remote_manifest = r.json()
    except Exception as e:
        queue.put(f"[ERROR] Manifest indirilemedi: {e}")
        return

    # 2. Local manifest yükle
    local_manifest = load_manifest(LOCAL_MANIFEST)

    # 3. Değişen dosyaları kontrol et
    for rel_path, remote_hash in remote_manifest.items():
        local_path = os.path.join(ROOT, rel_path)
        if not os.path.exists(local_path) or file_hash(local_path) != remote_hash:
            queue.put(f"[UPDATE] {rel_path} güncelleniyor...")
            download_url = f"https://raw.githubusercontent.com/frizxy/dehsetlauncher/main/{rel_path}"
            try:
                download_file(download_url, local_path)
            except Exception:
                queue.put(f"[ERROR] {rel_path} indirilemedi.")
        else:
              queue.put(f"[OK] {rel_path} güncel.")

    # 4. Local manifesti güncelle
    with open(LOCAL_MANIFEST, "w", encoding="utf-8") as f:
        json.dump(remote_manifest, f, indent=4)

    queue.put("[UPDATE] Tüm dosyalar kontrol edildi.")

   
