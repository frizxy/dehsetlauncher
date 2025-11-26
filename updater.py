import sys, os, requests, time, shutil,subprocess




launcher_path = os.path.join(os.path.dirname(__file__), "launcher.py")

print(f"[UPDATER] Launcher güncelleniyor...")

# GitHub linki
launcher_url = "https://raw.githubusercontent.com/frizxy/dehsetlauncher/refs/heads/main/launcher.py"

# Geçici dosya
tmp_path = launcher_path + ".new"

# İndir
r = requests.get(launcher_url, stream=True)
with open(tmp_path, "wb") as f:
    shutil.copyfileobj(r.raw, f)

# Launcher kapandı mı diye bekle (Windows için)
while True:
    try:
        os.rename(tmp_path, launcher_path)
        break
    except PermissionError:
        time.sleep(1)

print("[UPDATER] Güncelleme tamamlandı. Launcher yeniden başlatılıyor...")
subprocess.Popen([launcher_path])
sys.exit()
