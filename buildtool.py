import os, hashlib, json

ROOT = os.path.dirname(os.path.abspath(__file__))

TARGET_PATHS = [
    "mods",
    "shaderpacks",
    "resourcepacks",
    "launch.py",
    "zerotierconnection.py",
    "launcher.qss",
    "folder_update.py",
    "launcher_assets"
]

def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()

manifest = {}

for target in TARGET_PATHS:
    full_path = os.path.join(ROOT, target)

    if not os.path.exists(full_path):
        print("YOK:", target)
        continue

    if os.path.isfile(full_path):
        # Tek dosya
        manifest[target] = file_hash(full_path)

    else:
        # Klasör
        for root, dirs, files in os.walk(full_path):
            for f in files:
                fp = os.path.join(root, f)
                rel = os.path.relpath(fp, ROOT).replace("\\", "/")
                manifest[rel] = file_hash(fp)

with open("manifest.json", "w") as f:
    json.dump(manifest, f, indent=4)

print("manifest hazır!")