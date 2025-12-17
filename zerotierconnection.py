
import os
import socket
import time
network_id = "48d6023c46ed9ac3"   # ZeroTier ağ ID
path = fr"C:\ProgramData\ZeroTier\One\networks.d\48d6023c46ed9ac3.conf"
server_acik = False
zt_bagli = False

def zerotier_ping_thread():
    global zt_bagli, server_acik

    while True:
        # ZeroTier kontrol
        zt_bagli = os.path.exists(path)

        # Server ping
        try:
            s = socket.create_connection(("172.23.17.183", 25565), 0.7)
            s.close()
            server_acik = True
        except:
            server_acik = False

        time.sleep(1)

def update_label(button):
    if not zt_bagli:
        button.setText("ZeroTier'a Bağlı Değil!")
        button.setEnabled(False)
    elif server_acik:
        button.setText("Sunucu Açık!")
        button.setEnabled(True)
    else:
        button.setText("Sunucu Kapalı!")
        button.setEnabled(False)
    
   