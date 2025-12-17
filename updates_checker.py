
import subprocess
import os
import requests
import folder_update
import sys
import traceback
from PyQt6.QtWidgets import QMessageBox,QLabel
from PyQt6.QtCore import QTimer
import threading
import hashlib


updater_path = os.path.join(os.path.dirname(__file__), "folder_update.py")
UPDATER_URL = "https://raw.githubusercontent.com/frizxy/dehsetlauncher/main/folder_update.py"
updater_path = os.path.join(os.path.dirname(__file__), "folder_update.py")

def file_hash(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()

def remote_hash(url):
    h = hashlib.sha256()
    r = requests.get(url, stream=True, timeout=30)
    r.raise_for_status()
    for chunk in r.iter_content(chunk_size=1024 * 1024):
        if chunk:
            h.update(chunk)
    return h.hexdigest()


def download_updater():
    r = requests.get(UPDATER_URL, stream=True, timeout=30)
    r.raise_for_status()
    with open(updater_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                
                
def update_updater(queue):
    queue.put("Updater kontrol ediliyor...")

    try:
        remote_h = remote_hash(UPDATER_URL)
    except Exception as e:
        queue.put(f"[ERROR] Updater hash alınamadı: {e}")
        return

    # Updater yoksa indir
    if not os.path.exists(updater_path):
        queue.put("Updater yok, indiriliyor...")
        download_updater()
        queue.put("Updater indirildi.")
        return

    try:
        local_h = file_hash(updater_path)
    except Exception as e:
        queue.put(f"[ERROR] Local updater okunamadı: {e}")
        return

    if local_h == remote_h:
        queue.put("Updater güncel.")
        return

    # Hash farklıysa güncelle
    queue.put("Updater değişmiş, güncelleniyor...")
    download_updater()
    queue.put("Updater güncellendi.")


def check_for_updates(queue):
    
    queue.put("Dosyalar kontrol ediliyor...")

    msg1 = folder_update.check_files_update(queue)
    msg2 = update_updater(queue)

    queue.put("✅ Güncellemeler tamamlandı.")
