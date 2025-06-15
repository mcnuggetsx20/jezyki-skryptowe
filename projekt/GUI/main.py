import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os
import json
import time
import operator
import socket

# local imports
from menu_bar import MenuBar
from camera_control_frame import CameraControlFrame
from main_frame import MainFrame

ICON_PATHS = {
    "bulb": "icons/bulb.png",
    "camera": "icons/camera.png",
    "display": "icons/display.png"
}

class SmartHomeGUI(tk.Tk):
    def __init__(self):
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
        self.frame_seen = MainFrame(self.container, self)
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
        data = {
            "floors": self.total_floors,
            "floor_names": self.floor_names,
            "devices": self.devices,
            "backgrounds": self.floor_backgrounds
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
    
    def detect_devices_in_network(self):
        return
    
    def go_to_menu(self):
        # Ukryj panel urządzenia
        if hasattr(self, 'device_panel') and self.device_panel:
            self.device_panel.pack_forget()
            self.device_panel.destroy()
            self.device_panel = None

        # Pokaż z powrotem main_frame
        if self.main_frame:
            self.main_frame.pack(fill="both", expand=True)

if __name__ == '__main__':
    app = SmartHomeGUI()
    app.mainloop()
