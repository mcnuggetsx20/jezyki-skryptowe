import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os
import json
import time
import operator
import socket
import threading


# local imports
from menu_bar import MenuBar
from camera_control_frame import CameraControlFrame
from main_frame import MainFrame

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from server import Server

ICON_PATHS = {
    "bulb": "icons/bulb.png",
    "camera": "icons/camera.png",
    "display": "icons/display.png"
}

TYPE_TO_NAME = {
    0: 'camera',
    1: 'bulb',
    2: 'display'
}

class SmartHomeGUI(tk.Tk):
    def __init__(self, server):
        super().__init__()
        self.title("Smart Home GUI")
        self.geometry("1024x768")

        self.floor_names = ["Ogrod","Parter"]
        self.floor = 0
        self.total_floors = 2
        self.device_icons = {}
        self.floor_backgrounds = {}
        self.loaded_background_images = {}

        self.devices = []

        self.create_layout()

        self.clear_buffer = True
        self.server = server
        self.after(500, self.update_devices_from_sockarr)

    def load_icons(self):
        for name, path in ICON_PATHS.items():
            if os.path.exists(path):
                img = Image.open(path).resize((48, 48))
                self.device_icons[name] = ImageTk.PhotoImage(img)
            else:
                self.device_icons[name] = None

    def create_layout(self):
        # Główny kontener: układ pionowy
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # Menu 
        self.menu_option = MenuBar(self.container, self, height=20)

        # Wyswietlanie pierwsze MainFrame
        self.frame_seen = MainFrame(self.container, self, height=800, width=768)
        self.main_frame = self.frame_seen

    def open_device_panel(self, device):
        if self.frame_seen:
            self.frame_seen.pack_forget() 
        
        # Panel urządzenia
        self.device_panel = CameraControlFrame(
            container=self.container,
            dev=device,
            app=self,
            height=768,
            width=1024
        )
        self.device_panel.pack(fill="both", expand=True)
    
    def save_layout_to_file(self, filename):
        devices_clean = []
        for dev in self.devices:
            dev_copy = {k: v for k, v in dev.items() if k != 'sock'}
            devices_clean.append(dev_copy)

        data = {
            "floors": self.total_floors,
            "floor_names": self.floor_names,
            "devices": devices_clean,
            "backgrounds": self.floor_backgrounds
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

    
    def detect_devices_in_network(self):
        self.server.sendBroadcast()
    
    def go_to_menu(self):
        # Usuwanie panelu urzadzenia
        if hasattr(self, 'device_panel') and self.device_panel:
            self.device_panel.pack_forget()
            self.device_panel.destroy()
            self.device_panel = None

        # Pokaz glownego frame
        if self.main_frame:
            self.main_frame.pack(fill="both", expand=True)

    def update_devices_from_sockarr(self):
        sockarr = self.server.sockets
        for fd, sock in sockarr.sock_dct.items():
            name = sockarr.getName(fd)
            dev_type = sockarr.getType(fd)

            if name is None:
                continue  # pomiń niezinicjalizowane urządzenia

            # Znajdź urządzenie w liście po nazwie
            device = next((d for d in self.devices if d['name'] == name), None)

            if device:
                # Aktualizuj istniejące urządzenie
                device['fd'] = fd
                device['type'] = TYPE_TO_NAME[dev_type]
                device['sock'] = sock
            else:
                # Dodaj nowe urządzenie
                self.frame_seen.add_new_device({
                    'name': name,
                    'fd': fd,
                    'type': TYPE_TO_NAME[dev_type],
                    'sock': sock,
                    'x': 1,
                    'y': 1,
                    'floor': None,
                })
        if self.clear_buffer:
            self.server.recv_queue.clear()
        self.after(500, self.update_devices_from_sockarr)

if __name__ == '__main__':
    server = Server()
    thread = threading.Thread(target=server.main_loop, daemon=True)
    thread.start()
    app = SmartHomeGUI(server)
    app.mainloop()
