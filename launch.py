import json

import os

import platform

import sys

# Minecraft dizini ve sürüm





def resource_path(relative_path):

    if getattr(sys, "frozen", False):

        # EXE ile aynı dizin

        base_path = os.path.dirname(sys.executable)

    else:

        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

# Örnek: JSON dosyasına erişim

json_path = resource_path("versions/fabric-loader-0.17.3-1.21.10/fabric-loader-0.17.3-1.21.10.json")

minecraft_dir = resource_path("")

version = "fabric-loader-0.17.3-1.21.10"



# Kullanıcı bilgileri

username =""

uuid = "00000000-0000-0000-0000-000000000000"

access_token = "0"



# OS bilgisi

current_os = platform.system().lower()  # 'windows', 'linux', 'darwin' (MacOS)



# JSON dosyasını aç

with open(json_path, "r") as f:

    data = json.load(f)



main_class = data.get("mainClass")

libraries = data.get("libraries", [])



classpath = []

classing="qaa"

for lib in libraries:

    lib_name = lib["name"]

    parts = lib_name.split(":")

    if len(parts) < 3:

        print(f"Skipping invalid library entry: {lib_name}")

        continue



    group, artifact, version_lib = parts[0], parts[1], parts[2]

    jar_name = f"{artifact}-{version_lib}.jar"



    classifier = ""

    if len(parts) > 3:

        classifier = parts[3]

        # OS uyumsuz native dosyaları atla

        if classifier.startswith("natives-") and current_os not in classifier:

            continue

        jar_name = f"{artifact}-{version_lib}-{classifier}.jar"



    jar_path = os.path.join(minecraft_dir, "libraries", *group.split("."), artifact, version_lib, jar_name)

    if os.path.exists(jar_path):

        classpath.append(jar_path)

    else:

        # sadece gerekli native dosya Windows için uyarı ver

        if "natives" in jar_name and current_os not in jar_name:

            continue

        print(f"Warning: {jar_path} bulunamadı")



# Fabric loader JAR

fabric_jar = os.path.join(minecraft_dir, "versions", version, f"{version}.jar")

classpath.append(fabric_jar)



natives_dir = os.path.join(minecraft_dir, "versions", version, "natives")



jvm_args = [

    "-Xmx4G",

    "-XX:+UseG1GC",

    "-Dfile.encoding=UTF-8",

    f"-Djava.library.path={natives_dir}",

    f"-Dio.netty.native.workdir={natives_dir}"

]

def get_minecraft_args():

    return  [

        "--username", username,

        "--version", version,

        "--gameDir", minecraft_dir,

        "--assetsDir", os.path.join(minecraft_dir, "assets"),

        "--assetIndex", "5",

        "--uuid", uuid,

        "--accessToken", access_token,

        "--userType", "mojang",

        "--versionType", "release"

    ]





def build_cmd():

    return[

    r"runtime\jdk-21\bin\java.exe",  # kendi Java yolunu ayarla

    *jvm_args,

    "-cp", os.pathsep.join(classpath),

    main_class,

    *get_minecraft_args()

]







