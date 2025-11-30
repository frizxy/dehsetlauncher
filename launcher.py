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

import zerotierconnection

import zipfile

import shutil

import folder_update

import time

ROOT = os.path.dirname(os.path.abspath(__file__))

VERSIONS_DIR = os.path.join(ROOT, "versions")

VERSIONS_ZIP_URL = "https://github.com/frizxy/dehsetlauncher/releases/download/1.0.0/versions.zip"

VERSIONS_ZIP_PATH = os.path.join(ROOT, "versions.zip")

VERSION_URL = "https://raw.githubusercontent.com/frizxy/dehsetlauncher/refs/heads/main/update.txt"

UPDATER_VERSION_URL = "https://raw.githubusercontent.com/frizxy/dehsetlauncher/refs/heads/main/updater.txt"

VERSIONS_VERSION = "1.0.0"

VERSIONS_VERSION_URL = "https://raw.githubusercontent.com/frizxy/dehsetlauncher/refs/heads/main/versions_version.txt"

CURRENT_VERSION = "alpha-0.0.1"

UPDATER_VERSİON = "pre-alpha-0.0.1"



def download_versions():

    print("[UPDATE] versions.zip indiriliyor...")

    r = requests.get(VERSIONS_ZIP_URL, stream=True)

    r.raise_for_status()

    with open(VERSIONS_ZIP_PATH, "wb") as f:

        for chunk in r.iter_content(chunk_size=8192):

            f.write(chunk)

    print("[UPDATE] versions.zip indirildi.")



def extract_versions():

    try:

        with zipfile.ZipFile(VERSIONS_ZIP_PATH, 'r') as zip_ref:

            print("[UPDATE] versions klasörü güncelleniyor...")

            # Eski klasörü sil

            if os.path.exists(VERSIONS_DIR):

                shutil.rmtree(VERSIONS_DIR)

            zip_ref.extractall(ROOT)

        print("[UPDATE] versions klasörü güncellendi.")

    except zipfile.BadZipFile:

        print("[ERROR] İndirilen versions.zip geçerli bir zip değil!")

    finally:

        if os.path.exists(VERSIONS_ZIP_PATH):

            os.remove(VERSIONS_ZIP_PATH)





def update_versions():

    download_versions()

    extract_versions()









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

        r = requests.get("https://raw.githubusercontent.com/frizxy/dehsetlauncher/refs/heads/main/updater.py", stream=True)

        with open(updater_path, "wb") as f:

            shutil.copyfileobj(r.raw, f)

        print("[UPDATE] Updater indirildi.")

        

    if UPDATER_VERSİON != requests.get(UPDATER_VERSION_URL).text.strip():

        print("[UPDATE] Updater güncel değil, güncelleniyor...")

        r = requests.get("https://raw.githubusercontent.com/frizxy/dehsetlauncher/refs/heads/main/updater.py", stream=True)

        with open(updater_path, "wb") as f:

            shutil.copyfileobj(r.raw, f)

        print("[UPDATE] Updater indirildi.")

        

    # Updater’i başlat

    subprocess.Popen([updater_path, latest_version, sys.executable])







    





def when_opened(text):

    threading.Thread(target=check_for_updates, daemon=True).start()

    threading.Thread(target=lambda: run_updater(UPDATER_VERSİON), daemon=True).start()

    with open(os.path.join(ROOT,"username.txt"), "r", encoding="utf-8") as f:

         icerik = f.read()

    if icerik == "":

        launch.username = text

        with open(os.path.join(ROOT,"username.txt"), "w", encoding="utf-8") as f:

            f.write(text)

    else:

        textbox.setText(icerik)

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