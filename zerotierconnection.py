
import os
network_id = "48d6023c46ed9ac3"   # ZeroTier ağ ID
path = fr"C:\ProgramData\ZeroTier\One\networks.d\48d6023c46ed9ac3.conf"

def checkzerotier():
    if not os.path.exists(path):
        return "bağlı değil"
    return "bağlı"

def update_label(button):
    status = checkzerotier()
    if status == "bağlı":
        button.setText("Başlat")
        button.setEnabled(True)
    else:
        button.setText(f"ZeroTier Durumu: {status}")
        button.setEnabled(False)