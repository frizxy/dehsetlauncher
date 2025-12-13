
import subprocess
import os
import requests
import folder_update
import sys
import traceback
from PyQt6.QtWidgets import QMessageBox,QLabel
from PyQt6.QtCore import QTimer
import threading


UPDATER_VERSION_URL = "https://raw.githubusercontent.com/frizxy/dehsetlauncher/main/UPDATER_VERSION.txt"

CURRENT_UPDATER_VERSİON = "pre-alpha-0.0.1"
updater_path = os.path.join(os.path.dirname(__file__), "folder_update.py")

def update_updater(queue):

    # updater yoksa, GitHub’dan indir
    
    queue.put("Updater kontrol ediliyor...")
    if not os.path.exists(updater_path):
        
        queue.put("Updater yok, indiriliyor...")

        r = requests.get("https://raw.githubusercontent.com/frizxy/dehsetlauncher/main/folder_update.py", stream=True, timeout=30)
        r.raise_for_status()
        with open(updater_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        queue.put("Updater indirildi.")
  
    
    if CURRENT_UPDATER_VERSİON != requests.get(UPDATER_VERSION_URL).text.strip():

            queue.put("Updater güncel değil, güncelleniyor...")

            r = requests.get("https://raw.githubusercontent.com/frizxy/dehsetlauncher/main/folder_update.py", stream=True, timeout=30)
            r.raise_for_status()
            with open(updater_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            queue.put("Updater indirildi.")
   



def check_for_updates(queue):
    
    queue.put("Dosyalar kontrol ediliyor...")

    msg1 = folder_update.check_files_update(queue)
    msg2 = update_updater(queue)

    queue.put("✅ Güncellemeler tamamlandı.")
