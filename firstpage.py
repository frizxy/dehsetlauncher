import sys
from PyQt6.QtWidgets import QApplication, QWidget,QFrame,QLabel
from PyQt6.QtCore import Qt,pyqtSignal,QThread,QTimer,QMetaObject,Q_ARG
import os
import updates_checker
import threading
import time
import subprocess
import queue
update_queue = queue.Queue()
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
label.setObjectName("update_label")
label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
label.setWordWrap(True) 
label.setGeometry(100, 180, 200, 40)
frame.setGeometry(0, 0, 350, 400) 
update_result = None   # ✅ THREAD SONUCUNU BURAYA KOYACAĞIZ



def finish_update():
    subprocess.run([sys.executable, "launcher.py"])
    app.quit()

def process_queue():
    while not update_queue.empty():
        text = update_queue.get()
        label.setText(text)

    QTimer.singleShot(100, process_queue)
def update_worker():
    updates_checker.check_for_updates(update_queue)
QTimer.singleShot(100, process_queue)
thread= threading.Thread(target=update_worker, daemon=True)
thread.start()
def check_thread():
    if not thread.is_alive():
        QTimer.singleShot(2000, finish_update)
    else:
        QTimer.singleShot(100, check_thread)
        
QTimer.singleShot(100, check_thread)
window.show()

sys.exit(app.exec())
