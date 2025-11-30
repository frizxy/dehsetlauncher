from PyQt6.QtWidgets import QApplication, QWidget, QPushButton,QLineEdit,QMessageBox,QLabel,QProgressBar

from PyQt6.QtCore import QTimer

import threading

import sys

import requests

import launch

import json

import platform

import subprocess

import os
import traceback

import zerotierconnection

import zipfile

import shutil

import folder_update

import time

ROOT = os.path.dirname(os.path.abspath(__file__))

VERSIONS_DIR = os.path.join(ROOT, "versions")

VERSIONS_ZIP_URL = "https://github.com/frizxy/dehsetlauncher/releases/download/1.0.0/versions.zip"

VERSIONS_ZIP_PATH = os.path.join(ROOT, "versions.zip")


VERSION_URL = "https://raw.githubusercontent.com/frizxy/dehsetlauncher/main/update.txt"

UPDATER_VERSION_URL = "https://raw.githubusercontent.com/frizxy/dehsetlauncher/main/updater.txt"

VERSIONS_VERSION = "1.0.0"

VERSIONS_VERSION_URL = "https://raw.githubusercontent.com/frizxy/dehsetlauncher/main/versions_version.txt"

CURRENT_VERSION = "alpha-0.0.1"

UPDATER_VERSİON = "pre-alpha-0.0.1"



def download_versions():

    print("[UPDATE] versions.zip indiriliyor...")
    try:
        r = requests.get(VERSIONS_ZIP_URL, stream=True, timeout=30)
        r.raise_for_status()
        with open(VERSIONS_ZIP_PATH, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print("[UPDATE] versions.zip indirildi.")
    except Exception as e:
        print(f"[ERROR] versions.zip indirilemedi: {e}")
        try:
            if os.path.exists(VERSIONS_ZIP_PATH):
                os.remove(VERSIONS_ZIP_PATH)
        except Exception:
            pass
        raise



def extract_versions():

    tmp_dir = VERSIONS_DIR + ".new"
    try:
        with zipfile.ZipFile(VERSIONS_ZIP_PATH, 'r') as zip_ref:
            print("[UPDATE] versions klasörü güncelleniyor...")
            if os.path.exists(tmp_dir):
                shutil.rmtree(tmp_dir)
            zip_ref.extractall(tmp_dir)

        # If the zip contained a top-level 'versions' directory (nested), flatten it
        nested = os.path.join(tmp_dir, 'versions')
        if os.path.isdir(nested):
            try:
                for name in os.listdir(nested):
                    src = os.path.join(nested, name)
                    dst = os.path.join(tmp_dir, name)
                    shutil.move(src, dst)
                shutil.rmtree(nested)
            except Exception as e:
                print(f"[WARN] Nested versions flattening failed: {e}")

        # Replace existing folder atomically
        if os.path.exists(VERSIONS_DIR):
            shutil.rmtree(VERSIONS_DIR)
        os.rename(tmp_dir, VERSIONS_DIR)
        print("[UPDATE] versions klasörü güncellendi.")
    except zipfile.BadZipFile:
        print("[ERROR] İndirilen versions.zip geçerli bir zip değil!")
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
    except Exception as e:
        print(f"[ERROR] versions çıkarılırken hata: {e}")
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        raise
    finally:
        if os.path.exists(VERSIONS_ZIP_PATH):
            try:
                os.remove(VERSIONS_ZIP_PATH)
            except Exception:
                pass





def update_versions():

    download_versions()

    extract_versions()


# If the versions metadata or folders are missing, start a background download of versions.zip
try:
    _fabric_json = os.path.join(VERSIONS_DIR, "fabric-loader-0.17.3-1.21.10", "fabric-loader-0.17.3-1.21.10.json")
    if not os.path.exists(_fabric_json):
        print(f"[INFO] Eksik versions içeriği tespit edildi: {_fabric_json} — versions.zip indirilecek (arka planda).")
        threading.Thread(target=update_versions, daemon=True).start()
except Exception as _e:
    print(f"[WARN] versions başlangıç kontrolü başarısız: {_e}")


# Repair an existing nested `versions/versions/` that may have been created by older extracts
try:
    nested_existing = os.path.join(VERSIONS_DIR, 'versions')
    if os.path.isdir(nested_existing):
        print(f"[INFO] Nested versions folder detected at {nested_existing}; repairing...")
        for name in os.listdir(nested_existing):
            src = os.path.join(nested_existing, name)
            dst = os.path.join(VERSIONS_DIR, name)
            try:
                shutil.move(src, dst)
            except Exception as e:
                print(f"[WARN] move failed for {src} -> {dst}: {e}")
        try:
            shutil.rmtree(nested_existing)
            print("[INFO] Nested versions folder repaired.")
        except Exception as e:
            print(f"[WARN] Could not remove nested folder: {e}")
except Exception as e:
    print(f"[WARN] Nested versions repair check failed: {e}")









def check_for_updates():

    folder_update.check_files_update()

    server_version = requests.get(VERSION_URL).text.strip()

    if server_version != CURRENT_VERSION:

        run_updater()

        sys.exit()

    else:

        print("Launcher güncel.")

        

    if VERSIONS_VERSION != requests.get(VERSIONS_VERSION_URL).text.strip():

        print("[UPDATE] versions klasörü güncel değil, güncelleniyor...")

        update_versions()

        print("[UPDATE] versions klasörü güncellendi.")



def run_updater(latest_version):

    updater_path = os.path.join(os.path.dirname(__file__), "updater.py")

    

    # updater yoksa, GitHub’dan indir

    if not os.path.exists(updater_path):

        print("[UPDATE] Updater yok, indiriliyor...")

        r = requests.get("https://raw.githubusercontent.com/frizxy/dehsetlauncher/main/updater.py", stream=True, timeout=30)
        r.raise_for_status()
        with open(updater_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print("[UPDATE] Updater indirildi.")

        

    if UPDATER_VERSİON != requests.get(UPDATER_VERSION_URL).text.strip():

        print("[UPDATE] Updater güncel değil, güncelleniyor...")

        r = requests.get("https://raw.githubusercontent.com/frizxy/dehsetlauncher/main/updater.py", stream=True, timeout=30)
        r.raise_for_status()
        with open(updater_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print("[UPDATE] Updater indirildi.")

        

    # Updater’i başlat
    try:
        subprocess.Popen([sys.executable, updater_path, latest_version])
    except Exception:
        traceback.print_exc()








    





def when_opened(text):

    # Do not start update checks automatically on every startup —
    # this prevents the launcher/updater restart loop. If you want
    # to check for updates, run `folder_update.check_files_update()`
    # or call `run_updater()` manually.

    # Start a safe background update check that prompts the user
    # if a launcher update exists (prevents automatic restart loops).
    threading.Thread(target=check_updates_background, daemon=True).start()

    with open(os.path.join(ROOT,"username.txt"), "r", encoding="utf-8") as f:

         icerik = f.read()

    if icerik == "":

        launch.username = text

        with open(os.path.join(ROOT,"username.txt"), "w", encoding="utf-8") as f:

            f.write(text)

    else:

        textbox.setText(icerik)


def check_updates_background():
    """Background worker: checks remote launcher version and prompts user on main thread if needed."""
    try:
        server_version = requests.get(VERSION_URL, timeout=15).text.strip()
    except Exception:
        # network failed — fallback to file updates only
        try:
            folder_update.check_files_update()
        except Exception:
            pass
        return

    if server_version != CURRENT_VERSION:
        # schedule dialog on main thread
        QTimer.singleShot(0, lambda: ask_user_and_update(server_version))
    else:
        # no launcher update; perform file updates
        try:
            folder_update.check_files_update()
        except Exception:
            pass
        # Also check versions.zip version and update via zip if needed
        try:
            remote_versions_version = requests.get(VERSIONS_VERSION_URL, timeout=15).text.strip()
            if VERSIONS_VERSION != remote_versions_version:
                print("[UPDATE] versions klasörü güncel değil, zip üzerinden güncelleniyor...")
                try:
                    update_versions()
                    print("[UPDATE] versions klasörü güncellendi.")
                except Exception as e:
                    print(f"[ERROR] versions.zip ile güncelleme başarısız: {e}")
        except Exception:
            # ignore network errors for versions check
            pass


def ask_user_and_update(server_version):
    reply = QMessageBox.question(None, "Güncelleme bulundu",
                                 "Yeni bir launcher sürümü bulundu. Güncellemek ister misiniz?",
                                 QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
    if reply == QMessageBox.StandardButton.Yes:
        try:
            run_updater(server_version)
        except Exception:
            traceback.print_exc()
        os._exit(0)

def when_closed(text):

    with open(os.path.join(ROOT,"username.txt"), "r", encoding="utf-8") as f:

         icerik = f.read()

    if text != icerik:

        launch.username = text

        with open(os.path.join(ROOT,"username.txt"), "w", encoding="utf-8") as f:

            f.write(text)



    

    



def start_minecraft_here():

    progress.setValue(0)



    prog_timer = QTimer()

    prog_timer.setInterval(50)



    def increase():

        val = progress.value()

        if val < 100:

            progress.setValue(val + 1)

        else:

            prog_timer.stop()



    prog_timer.timeout.connect(increase)

    prog_timer.start()

    def run_game():

        creationflags = subprocess.CREATE_NO_WINDOW

        proc = subprocess.Popen(launch.build_cmd(),creationflags=creationflags)



        proc.wait()  # Minecraft kapanana kadar bekle

        button.setEnabled(False)

        # Ana thread'de butonu aktif et

        if progress.value() == 100:

            QTimer.singleShot(0, lambda: (

                button.setEnabled(True),

                progress.setValue(0)

            ))

        

    threading.Thread(target=run_game, daemon=True).start()



app = QApplication(sys.argv)

with open(os.path.join(ROOT,"launcher.qss"), "r") as f:

    style = f.read()



app.setStyleSheet(style)



window = QWidget()

window.setWindowTitle("DEHŞET LAUNCHER")



window.setFixedSize(800, 500)



textbox = QLineEdit(window)

textbox.setObjectName("usernameBox")

textbox.resize(200, 40)

textbox.move(300, 200)

QLabel("Kullanıcı Adı:",window).move(200,210)

button = QPushButton("Başlat", window)

button.setObjectName("startButton")

button.resize(200, 100)

button.move(300, 300)

button.clicked.connect(lambda: start_minecraft_here()) 

progress = QProgressBar(window)

progress.setObjectName("progress")

progress.setGeometry(0, 470, 800, 30)

progress.setRange(0, 100)

progress.setValue(0)





QTimer.singleShot(0, lambda:when_opened(textbox.text()))

app.aboutToQuit.connect(lambda:when_closed(textbox.text()))

def zerotiercontrol(button):

    QTimer.singleShot(0, lambda: zerotierconnection.update_label(button))

    timer = QTimer(window)

    timer.setInterval(1000)

    timer.timeout.connect(lambda: zerotierconnection.update_label(button))

    timer.start()

    return timer





window.show()

zerotiercontrol(button)

sys.exit(app.exec())

app.exit()