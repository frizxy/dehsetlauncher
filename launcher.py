from PyQt6.QtWidgets import QApplication, QWidget, QPushButton,QLineEdit,QMessageBox,QLabel,QProgressBar,QSlider,QComboBox
from PyQt6.QtCore import QTimer,Qt
from PyQt6.QtGui import QIcon
import threading
import sys
import launch
import subprocess
import os
import zerotierconnection
import psutil
import settings


ram = psutil.virtual_memory()

print("Toplam RAM:", round(ram.total / 1024**3, 2)-1, "G")


ROOT = os.path.dirname(os.path.abspath(__file__))


def when_opened(text):
    
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

        launch.start_game()




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
window.setWindowIcon(QIcon(os.path.join(ROOT,"launcher_assets/icon.ico")))
window.setWindowTitle("DEHŞET LAUNCHER")



window.setFixedSize(800, 500)



textbox = QLineEdit(window)

textbox.setObjectName("usernameBox")

textbox.resize(200, 40)

textbox.move(300, 200)
textbox.setStyleSheet("color:white;font-weight:bold;background:transparent;")
label=QLabel("Kullanıcı Adı:",window)
label.move(200, 210)
label.setStyleSheet("color:white;font-weight:bold;background:transparent;")
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

progress.setStyleSheet("color:white;font-size:20px;font-weight:bold;background:transparent;")


setting_button = QPushButton("Ayarlar", window)
setting_button.setObjectName("settingButton")
setting_button.resize(100, 40)
setting_button.clicked.connect(lambda: settings.window.show())





QTimer.singleShot(0, lambda:when_opened(textbox.text()))

    

app.aboutToQuit.connect(lambda:when_closed(textbox.text()))



ui_timer = QTimer(window)
ui_timer.timeout.connect(lambda: zerotierconnection.update_label(button))
ui_timer.start(500)

threading.Thread(
    target=zerotierconnection.zerotier_ping_thread,
    daemon=True
).start()

window.show()


sys.exit(app.exec())

