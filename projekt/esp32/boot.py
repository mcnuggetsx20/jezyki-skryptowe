import network
import socket
import machine
import time
import os
import gc

def save_wifi_credentials(ssid, password):
    with open("wifi.txt", "w") as f:
        f.write(f"{ssid}\n{password}")

def save_name(name):
    with open("name.txt", "w") as f:
        f.write(name)

def load_wifi_credentials():
    try:
        with open("wifi.txt", "r") as f:
            ssid = f.readline().strip()
            password = f.readline().strip()
            return ssid, password
    except:
        return None, None

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    print("📶 Łączenie z Wi-Fi:", ssid)

    for i in range(15):
        if wlan.isconnected():
            print("✅ Połączono z Wi-Fi:", ssid)
            print("📡 IP:", wlan.ifconfig()[0])
            return True
        time.sleep(1)

    print("❌ Nie udało się połączyć z Wi-Fi.")
    return False

def start_ap_mode():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='SmartHomeConfig', password='12345678')
    print("📡 AP uruchomiony: SmartHomeConfig (192.168.4.1)")
    return ap

def serve_config_page():
    html = """<!DOCTYPE html>
<html>
  <head><title>Ustaw Wi-Fi</title></head>
  <body>
    <h2>Konfiguracja Wi-Fi</h2>
    <form action="/save">
      SSID: <input name="ssid"><br>
      Haslo: <input name="pass" type="password"><br>
      Name <input name="name"<br>
      <input type="submit" value="Zapisz">
    </form>
  </body>
</html>"""

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("🌐 Serwer gotowy na http://192.168.4.1")

    while True:
        try:
            cl, addr = s.accept()
            req = cl.recv(1024).decode()
            print("📥 Żądanie od:", addr)
            print("🔹 Zawartość:", req)

            if "GET /save?" in req:
                try:
                    query = req.split(" ")[1].split("?")[1].split(" ")[0]
                    parts = query.split("&")
                    data = {}
                    for part in parts:
                        k, v = part.split("=")
                        data[k] = v.replace("+", " ")
                    ssid = data["ssid"]
                    password = data["pass"]
                    name = data["name"]
                    if name == "":
                        name = "led10"
                    print(ssid)
                    print(password)
                    print(name)
                    save_wifi_credentials(ssid,password)
                    save_name(name)
                    cl.send("HTTP/1.1 200 OK\r\n\r\nDane zapisane. Restart...")
                    cl.close()
                    time.sleep(3)
                    machine.reset()
                except Exception as e:
                    cl.send("HTTP/1.1 400 Bad Request\r\n\r\nBłąd danych: {}".format(str(e)))
                    cl.close()
            else:
                cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + html)
                cl.close()

        except Exception as e:
            print("❗ Błąd obsługi klienta:", str(e))
        finally:
            gc.collect()

# debug
def run_normal_mode():
    print("🎯 Tryb normalny – tu możesz uruchomić swoją aplikację!")
    # np. rozpocznij odczyt sensorów, uruchom serwer itp.
    # Póki co tylko print co 2 sekundy:
    print("🏠 System działa, połączony z Wi-Fi")

def main():
    ssid, password = load_wifi_credentials()
    if ssid and password:
        if connect_to_wifi(ssid, password):
            run_normal_mode()
            return
    # W przeciwnym razie – konfiguracja
    start_ap_mode()
    serve_config_page()

main()
