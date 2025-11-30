import sys
import os
import requests
import time
import shutil
import subprocess
import hashlib


launcher_path = os.path.join(os.path.dirname(__file__), "launcher.py")

print(f"[UPDATER] Launcher güncelleniyor...")

# GitHub linki (raw)
launcher_url = "https://raw.githubusercontent.com/frizxy/dehsetlauncher/main/launcher.py"

# Geçici dosya
tmp_path = launcher_path + ".new"


def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        data = f.read().replace(b"\r\n", b"\n")
    h.update(data)
    return h.hexdigest()


# İndir (stream, timeout)
try:
    r = requests.get(launcher_url, stream=True, timeout=30)
    r.raise_for_status()
    with open(tmp_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
except Exception as e:
    print(f"[UPDATER] Launcher indirilemedi: {e}")
    # Try to launch existing launcher if present
    if os.path.exists(launcher_path):
        subprocess.Popen([sys.executable, launcher_path])
    sys.exit(1)

# Eğer mevcut launcher yoksa doğrudan değiştir
if os.path.exists(launcher_path):
    try:
        new_hash = file_hash(tmp_path)
        old_hash = file_hash(launcher_path)
        if new_hash == old_hash:
            print("[UPDATER] Launcher zaten güncel.")
            os.remove(tmp_path)
            # Başlat ve çık
            subprocess.Popen([sys.executable, launcher_path])
            sys.exit(0)
    except Exception:
        # devam et değiştirmeye
        pass

# Launcher kapandı mı diye bekle (Windows için) ve değiştir
while True:
    try:
        if os.path.exists(launcher_path):
            os.remove(launcher_path)  # önce sil → rename daha temiz çalışır
        break
    except PermissionError:
        time.sleep(1)

os.rename(tmp_path, launcher_path)
print("[UPDATER] Güncelleme tamamlandı.")

# Başlat (Python ile) ve çık
try:
    subprocess.Popen([sys.executable, launcher_path])
except Exception as e:
    print(f"[UPDATER] Launcher başlatılamadı: {e}")
sys.exit(0)
