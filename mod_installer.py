import requests
import zipfile
import os
import shutil
import hashlib
import requests
import json
ROOT = os.path.dirname(os.path.abspath(__file__))
MANIFEST_URL ="https://raw.githubusercontent.com/frizxy/dehsetlauncher/main/mod_manifest.json"
MODS_URL = "https://github.com/frizxy/dehsetlaunchermods/releases/download/1/Desktop.zip"
LOCAL_MANIFEST_PATH = os.path.join(ROOT, "mod_manifest.json")

def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def load_manifest(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}



def check_mods_update(queue):
  

    queue.put("Modlar kontrol ediliyor...")
    
    # 1. Remote manifest indir
    try:
        r = requests.get(MANIFEST_URL, timeout=30)
        r.raise_for_status()
        remote_manifest = r.json()
    except Exception as e:
        queue.put(f"[ERROR] Manifest indirilemedi: {e}")
        return

    # 2. Local manifest yükle
    local_manifest = load_manifest(LOCAL_MANIFEST_PATH)

    # 3. Değişen dosyaları kontrol et
    for rel_path, remote_hash in remote_manifest.items():
        local_path = os.path.join(ROOT, rel_path)
        if not os.path.exists(local_path) or file_hash(local_path) != remote_hash:
            queue.put(f"[UPDATE] modlar güncelleniyor...")
           
            try:
                indir_ac_sil(MODS_URL,os.path.join(ROOT,"mods"))
            except Exception:
                queue.put(f"[ERROR] {rel_path} indirilemedi.")
        else:
              queue.put(f"[OK] {rel_path} güncel.")

    # 4. Local manifesti güncelle
    with open(LOCAL_MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(remote_manifest, f, indent=4)

    queue.put("[UPDATE] Tüm modlar kontrol edildi.")

   

def klasoru_temizle(path):
    if os.path.exists(path):
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
            else:
                shutil.rmtree(item_path)
def indir_ac_sil(zip_url, hedef_klasor):
    os.makedirs(hedef_klasor, exist_ok=True)

    print("Klasör temizleniyor...")
    klasoru_temizle(hedef_klasor)

    zip_yolu = os.path.join(hedef_klasor, "temp.zip")

    print("Zip indiriliyor...")
    r = requests.get(zip_url, stream=True)
    r.raise_for_status()

    with open(zip_yolu, "wb") as f:
        for chunk in r.iter_content(1024 * 1024):
            if chunk:
                f.write(chunk)

    print("Zip açılıyor...")
    with zipfile.ZipFile(zip_yolu, "r") as z:
        z.extractall(hedef_klasor)

    print("Zip siliniyor...")
    os.remove(zip_yolu)

    print("Bitti.")

