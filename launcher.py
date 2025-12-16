from PyQt6.QtWidgets import QApplication, QWidget, QPushButton,QLineEdit,QMessageBox,QLabel,QProgressBar,QSlider
from PyQt6.QtCore import QTimer,Qt
from PyQt6.QtGui import QIcon
import threading
import sys
import launch
import subprocess
import os
import zerotierconnection
import psutil



ram = psutil.virtual_memory()

print("Toplam RAM:", round(ram.total / 1024**3, 2)-1, "G")

launch.RAM = str(round(ram.total / 1024**3, 2)-1) + "G"
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

label2=QLabel("RAM:",window)
label2.move(250, 425)
label2.setStyleSheet("color:white;font-weight:bold;background:transparent;")

ramlabel=QLabel("RAM:",window)
ramlabel.move(380, 415)
ramlabel.setStyleSheet("color:white;font-weight:bold;background:transparent;")

# Dosyadan açılış değeri oku
ram_txt_path = os.path.join(ROOT, "ram.txt")
if not os.path.exists(ram_txt_path):
    with open(ram_txt_path, "w", encoding="utf-8") as f:
        f.write(str(int(round(ram.total / 1024**3, 2)-3)))  # varsayılan değer

with open(ram_txt_path, "r", encoding="utf-8") as f:
    try:
        initial_ram = int(f.read())
    except ValueError:
        initial_ram = int(round(ram.total / 1024**3, 2)-3)

slider = QSlider(window)
slider.setOrientation(Qt.Orientation.Horizontal)
slider.setGeometry(300, 420, 200, 30)
slider.setMinimum(2)
slider.setMaximum(int(round(ram.total / 1024**3, 2)-1))
slider.setSingleStep(1)  # Step-step
slider.setValue(initial_ram)  # txt’deki değeri başlangıç yap

def ramslider_changed(value):
    ramlabel.setText(f"{value}G")
    # Slider değiştikçe ram.txt güncellensin
    with open(ram_txt_path, "w", encoding="utf-8") as f:
        f.write(str(value))

slider.valueChanged.connect(ramslider_changed)

# Başlangıç label'ı
ramlabel.setText(f"{slider.value()}G")
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

