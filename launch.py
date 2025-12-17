import os
import subprocess
import tempfile
import json

# ===== ANA DİZİN =====
MC_DIR = os.path.dirname(os.path.abspath(__file__))

# ===== JAVA =====
JAVA_PATH = os.path.join(MC_DIR, r"runtime\jdk-17.0.12\bin\java.exe")

# ===== SÜRÜMLER =====
VERSION = "1.20.1"
FABRIC_VERSION = "fabric-loader-0.17.3-1.20.1"
MAIN_CLASS = "net.fabricmc.loader.impl.launch.knot.KnotClient"


# ===== YOLLAR =====
LIBRARIES_DIR = os.path.join(MC_DIR, "libraries")
FABRIC_JSON = os.path.join(MC_DIR, "versions", FABRIC_VERSION, f"{FABRIC_VERSION}.json")
FABRIC_JAR = os.path.join(MC_DIR, "versions", FABRIC_VERSION, f"{FABRIC_VERSION}.jar")
NATIVES_DIR = os.path.join(MC_DIR, "versions", FABRIC_VERSION, "natives")


def set_username():
     with open(os.path.join(MC_DIR,"username.txt"), "r", encoding="utf-8") as f:
         
         icerik = f.read()
         return icerik.strip()

def set_ram():
    with open(os.path.join(MC_DIR,"ram.txt"), "r", encoding="utf-8") as f:
            icerik = f.read()
            return icerik.strip() + "G"
# ===== FABRIC JSON OKU =====
with open(FABRIC_JSON, "r", encoding="utf-8") as f:
    data = json.load(f)

libraries = data.get("libraries", [])
asset_index = data.get("assetIndex", {}).get("id", "26")

# ===== CLASSPATH TEMİZ TOPLA =====
classpath = []

# ✅ 1) JOPT-SIMPLE ZORUNLU VE EN BAŞTA
jopt_path = os.path.join(
    MC_DIR,
    "libraries", "net", "sf", "jopt-simple",
    "jopt-simple", "5.0.4",
    "jopt-simple-5.0.4.jar"
)

if not os.path.exists(jopt_path):
    print("❌ JOPT-SIMPLE YOK:", jopt_path)
    exit(1)

classpath.append(jopt_path)

# ✅ 2) JSON İÇİNDEKİ KÜTÜPHANELER
for lib in libraries:
    name = lib.get("name")
    if not name:
        continue

    group, artifact, ver = name.split(":")[:3]
    jar_name = f"{artifact}-{ver}.jar"

    jar_path = os.path.join(
        MC_DIR,
        "libraries",
        *group.split("."),
        artifact,
        ver,
        jar_name
    )

    if os.path.exists(jar_path):
        classpath.append(jar_path)

# ✅ 3) SADECE FABRIC LOADER JAR
if not os.path.exists(FABRIC_JAR):
    print("❌ FABRIC JAR YOK:", FABRIC_JAR)
    exit(1)

classpath.append(FABRIC_JAR)

# ===== ARGFILE (206 HATASI İÇİN) =====
argfile_content = "-cp\n" + ";".join(classpath)

argfile = tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8")
argfile.write(argfile_content)
argfile.close()

# ===== JAVA KOMUTU =====
cmd = [
    JAVA_PATH,
    f"-Xmx{set_ram()}",
    f"-Xms{set_ram()}",

    f"-Djava.library.path={NATIVES_DIR}",

    "@" + argfile.name,
    MAIN_CLASS,

    "--username", set_username(),
    "--version", VERSION,
    "--gameDir", MC_DIR,
    "--assetsDir", os.path.join(MC_DIR, "assets"),
    "--assetIndex", asset_index,
    "--uuid", "0",
    "--accessToken", "0",
    "--userType", "offline",
    "--versionType", "release",
    "--quickPlayMultiplayer", "172.23.17.183:25565"
]

print("✅ JAVA KOMUTU:")
print(" ".join(cmd))
def start_game():
    set_username()
    subprocess.run(cmd)

