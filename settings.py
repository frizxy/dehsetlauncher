from PyQt6.QtWidgets import QApplication, QWidget, QPushButton,QLineEdit,QLabel,QSlider,QTabWidget,QVBoxLayout,QHBoxLayout,QTabBar
from PyQt6.QtCore import QTimer,Qt
from PyQt6.QtGui import QIcon
import os
import psutil
import launch
app = QApplication([])





window = QWidget()



window.setWindowTitle("Launcher ayarları")
ROOT = os.path.dirname(os.path.abspath(__file__))
ram = psutil.virtual_memory()
launch.RAM = str(round(ram.total / 1024**3, 2)-1) + "G"

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


label2=QLabel("RAM:",window)
label2.move(250, 425)
label2.setStyleSheet("color:white;font-weight:bold;background:transparent;")

ramlabel=QLabel("RAM:",window)
ramlabel.move(380, 415)
ramlabel.setStyleSheet("color:white;font-weight:bold;background:transparent;")

def ramslider_changed(value):
    ramlabel.setText(f"{value}G")
    # Slider değiştikçe ram.txt güncellensin
    with open(ram_txt_path, "w", encoding="utf-8") as f:
        f.write(str(value))

slider.valueChanged.connect(ramslider_changed)

# Başlangıç label'ı
ramlabel.setText(f"{slider.value()}G")