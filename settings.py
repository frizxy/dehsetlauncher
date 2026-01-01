from PyQt6.QtWidgets import QApplication, QWidget, QPushButton,QLineEdit,QLabel,QSlider,QTabWidget,QVBoxLayout,QHBoxLayout,QTabBar,QComboBox,QMessageBox
from PyQt6.QtCore import QTimer,Qt
from PyQt6.QtGui import QIcon
import os
import psutil
import launch
app = QApplication([])


low_end = [
    "optimization_sets/low-end/options.txt",
    "optimization_sets/low-end/optionsof.txt",
    "optimization_sets/low-end/optionsshaders.txt"
]

high_end = [
    "optimization_sets/high-end/options.txt",
    "optimization_sets/high-end/optionsof.txt",
    "optimization_sets/high-end/optionsshaders.txt"
]
opti =[
    "options.txt",
    "optionsof.txt",
    "optionsshaders.txt"
]




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


optimization_sets_combobox = QComboBox(window)
optimization_sets_combobox.setObjectName("optimizationSetsComboBox")
optimization_sets_combobox.resize(200, 40)
optimization_sets_combobox.move(300, 250)
optimization_sets_combobox.addItems(["bad pc","good pc","custom settings"])
optimization_sets_combobox.setStyleSheet("color:black;font-weight:bold;background:transparent;")




def apply_optimization():
    selected_option = optimization_sets_combobox.currentText()
    if selected_option == "bad pc":
        kaynak_liste = low_end
    elif selected_option == "good pc":
        kaynak_liste = high_end
    else:
        return

    for kaynak, hedef in zip(kaynak_liste, opti):
        hedef_yol = os.path.join(ROOT, hedef)

        if not os.path.exists(kaynak):
            QMessageBox.warning(
                
                "Hata",
                "Optimization dosyaları bulunamadı!"
            )
            return

        with open(kaynak, "r", encoding="utf-8") as f:
            icerik = f.read()

        with open(hedef_yol, "w", encoding="utf-8") as f:
            f.write(icerik)
optimization_sets_combobox.currentTextChanged.connect(apply_optimization)