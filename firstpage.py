import sys
from PyQt6.QtWidgets import QApplication, QWidget,QFrame,QLabel
from PyQt6.QtCore import Qt
import os
import updates_checker
ROOT = os.path.dirname(os.path.abspath(__file__))


with open(os.path.join(ROOT,"firstpage.qss"), "r") as f:
    style = f.read()
    
    
    
    
app = QApplication(sys.argv)
window = QWidget()
window.setWindowFlags(Qt.WindowType.FramelessWindowHint)
window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
window.resize(350, 400)
app.setStyleSheet(style)
frame = QFrame(window)
label = QLabel("Dehşet Launcher",frame)
label.setStyleSheet("color:white;font-size:20px;font-weight:bold;background:transparent;")
label.setGeometry(100, 180, 500, 40)
frame.setGeometry(0, 0, 350, 400) 

window.show()

sys.exit(app.exec())
