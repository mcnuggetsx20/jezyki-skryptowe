import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os
import json
import time
import operator

# local imports
from menu_bar import MenuBar

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
        self.dragging_device = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        self.load_icons()
        self.create_layout()
        self.load_layout_from_file("layout.json")

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

        # Menu na górze
        self.menu_option = MenuBar(self.container, self, height=20)

        # Frame na resztę: canvas + sidebar
        self.main_frame = ttk.Frame(self.container)
        self.main_frame.pack(side="top", fill="both", expand=True)

        # Canvas (główna część)
        self.canvas = tk.Canvas(self.main_frame, bg="white", width=800, height=768)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.image_refs = []


        style = ttk.Style()
        style.configure("Blue.TFrame", background="#add8e6")  # jasny niebieski

        self.sidebar = ttk.Frame(self.main_frame, width=200, style="Blue.TFrame")
        self.sidebar.pack(side="right", fill="y")

        ttk.Label(self.sidebar, text="Wszystkie urządzenia:", anchor="center", background="#add8e6").pack(pady=10)
        self.device_list_frame = ttk.Frame(self.sidebar, style="Blue.TFrame")
        self.device_list_frame.pack(fill="both", expand=True)

        # Dodawanie nowych urządzeń (w sidebar)
        ttk.Label(self.sidebar, text="Dodaj urządzenie:").pack(pady=(10,2))
        self.new_dev_name = tk.StringVar()
        self.new_dev_type = tk.StringVar(value="bulb")

        ttk.Entry(self.sidebar, textvariable=self.new_dev_name).pack(padx=5)
        ttk.OptionMenu(self.sidebar, self.new_dev_type, "bulb", *ICON_PATHS.keys()).pack(padx=5, pady=2)
        ttk.Button(self.sidebar, text="Dodaj", command=self.add_new_device).pack(pady=5)

        nav_frame = ttk.Frame(self.sidebar)
        nav_frame.pack(pady=10)
        ttk.Button(nav_frame, text="Piętro ↑", command=self.go_up_floor).pack(side="left", padx=5)
        ttk.Button(nav_frame, text="↓", command=self.go_down_floor).pack(side="right", padx=5)

        self.floor_label = ttk.Label(self.sidebar, text=f"Piętro: {self.floor}")
        self.floor_label.pack()

        # Bind canvas events for click/drag and right-click
        self.canvas.bind("<ButtonPress-1>", self.on_canvas_left_press)
        self.canvas.bind("<B1-Motion>", self.on_canvas_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_left_release)
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)

        # Do śledzenia kliknięć
        self.click_start_time = 0
        self.clicked_device = None

    def refresh_device_list(self):
        for widget in self.device_list_frame.winfo_children():
            widget.destroy()

        columns = 3  # liczba ikon w jednym wierszu
        row = 0
        col = 0

        for i, dev in enumerate(self.devices):
            frame = ttk.Frame(self.device_list_frame, relief="raised", padding=4)
            frame.grid(row=row, column=col, padx=5, pady=5)

            icon = self.device_icons.get(dev['type'])
            if icon:
                label = tk.Label(frame, image=icon)
                label.image = icon  
                label.pack()
                label.bind("<ButtonPress-1>", lambda e, d=dev: self.open_device_panel(e,d))  
                label.bind("<Button-3>", lambda event, dev=dev: self.on_device_list_right_click(event, dev))
            tk.Label(frame, text=dev['name'], wraplength=120).pack()

            col += 1
            if col >= columns:
                col = 0
                row += 1
    

    def on_device_list_right_click(self, event, dev):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Add to floor", command=lambda dev=dev: self.add_to_floor_device(dev))
        self.context_menu.tk_popup(event.x_root, event.y_root)
    
    def add_to_floor_device(self, dev):
        dev["x"] = 100
        dev["y"] = 100
        dev["floor"] = self.floor_names[self.floor]
        self.draw_devices_on_canvas()

    def draw_devices_on_canvas(self):
        self.canvas.delete("all")
        self.canvas.image_refs.clear()

        # Rysuj tło piętra
        bg_path = self.floor_backgrounds.get(self.floor)
        if bg_path and os.path.exists(bg_path):
            if self.floor not in self.loaded_background_images:
                img = Image.open(bg_path).resize((800, 768))
                self.loaded_background_images[self.floor] = ImageTk.PhotoImage(img)
            bg_img = self.loaded_background_images[self.floor]
            self.canvas.create_image(0, 0, image=bg_img, anchor="nw")
            self.canvas.image_refs.append(bg_img)
        else:
            self.canvas.config(bg="white")

        # Rysuj tylko urządzenia na aktualnym piętrze
        for dev in self.devices:
            if dev["floor"] != self.floor_names[self.floor]:
                continue
            icon = self.device_icons.get(dev['type'])
            if icon:
                img_id = self.canvas.create_image(dev['x'], dev['y'], image=icon, anchor="center", tags=("device",))
                self.canvas.image_refs.append(icon)
                # Taguj obrazek id urządzenia dla odniesienia
                self.canvas.tag_bind(img_id, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
                self.canvas.tag_bind(img_id, "<Leave>", lambda e: self.canvas.config(cursor=""))
                # Bindy na canvas mamy globalnie (obsługiwane niżej)

    def find_device_by_canvas_coords(self, x, y):
        # Szuka urządzenia pod wskazanymi współrzędnymi (w promieniu 30 pikseli)
        for dev in self.devices:
            if dev["floor"] != self.floor_names[self.floor]:
                continue
            dx = dev['x'] - x
            dy = dev['y'] - y
            if dx*dx + dy*dy <= 30*30:
                return dev
        return None

    def on_canvas_left_press(self, event):
        self.click_start_time = time.time()
        dev = self.find_device_by_canvas_coords(event.x, event.y)
        if dev:
            self.dragging_device = dev
            self.drag_offset_x = event.x - dev['x']
            self.drag_offset_y = event.y - dev['y']
            self.clicked_device = dev
        else:
            self.dragging_device = None
            self.clicked_device = None

    def on_canvas_left_drag(self, event):
        if self.dragging_device:
            # Przesuwanie urządzenia, aktualizacja pozycji
            new_x = event.x - self.drag_offset_x
            new_y = event.y - self.drag_offset_y
            self.dragging_device['x'] = max(0, min(new_x, 800))
            self.dragging_device['y'] = max(0, min(new_y, 768))
            self.draw_devices_on_canvas()

    def on_canvas_left_release(self, event):
            self.save_layout_to_file("layout.json")

    def on_canvas_right_click(self, event):
        # Usuwanie urządzenia pod kursorem z aktualnego piętra
        dev = self.find_device_by_canvas_coords(event.x, event.y)
        if dev and dev.get("floor", 0) == self.floor:
            self.context_menu = tk.Menu(self, tearoff=0)
            self.context_menu.add_command(label="Opcja 1", command=lambda: print("Opcja 1"))
            self.context_menu.add_command(label="Opcja 2", command=lambda: print("Opcja 2"))
            self.context_menu.add_separator()
            self.context_menu.add_command(label="Usuń z piętra", command=lambda: operator.setitem(dev, "floor", None))
            self.context_menu.tk_popup(event.x_root, event.y_root)
            self.devices.remove(dev)
            self.refresh_device_list()
            self.draw_devices_on_canvas()
            self.save_layout_to_file("layout.json")


    def open_device_panel(self, event, device):
        print('cios')

    def go_up_floor(self):
        if self.floor < self.total_floors - 1:
            self.floor += 1
            self.update_floor_label()
            self.draw_devices_on_canvas()

    def go_down_floor(self):
        if self.floor > 0:
            self.floor -= 1
            self.update_floor_label()
            self.draw_devices_on_canvas()

    def save_layout_to_file(self, filename):
        data = {
            "floors": self.total_floors,
            "floor_names": self.floor_names,   
            "devices": self.devices,
            "backgrounds": self.floor_backgrounds
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)


    def load_layout_from_file(self, filename):
        if os.path.exists(filename):
            with open(filename) as f:
                data = json.load(f)
            self.total_floors = data.get("floors", 1)
            self.floor_names = data.get("floor_names", [f"Piętro {i}" for i in range(self.total_floors)])
            self.devices = data.get("devices", [])
            self.floor_backgrounds = data.get("backgrounds", {})
        else:
            self.total_floors = 2
            self.floor_names = ["Ogrod", "Parter"]
            self.devices = [
                {"name": "Żarówka 1", "type": "bulb", "x": 100, "y": 150, "floor": 0},
                {"name": "Kamera wejście", "type": "camera", "x": 300, "y": 200, "floor": 0},
                {"name": "Wyświetlacz LCD", "type": "display", "x": 500, "y": 300, "floor": 1}
            ]
        self.loaded_background_images.clear()
        self.floor = 0
        self.update_floor_label()
        self.refresh_device_list()
        self.draw_devices_on_canvas()
    
    def update_floor_label(self):
        if 0 <= self.floor < len(self.floor_names):
            name = self.floor_names[self.floor]
        else:
            name = f"Piętro {self.floor}"
        self.floor_label.config(text=f"Floor: {name}")



    def add_new_device(self):
        name = self.new_dev_name.get().strip()
        typ = self.new_dev_type.get()
        if name and typ in ICON_PATHS:
            # Dodaj urządzenie na środku kanwy piętra
            dev = {"name": name, "type": typ, "x": 400, "y": 384, "floor": None}
            self.devices.append(dev)
            self.refresh_device_list()
            self.draw_devices_on_canvas()
            self.new_dev_name.set("")
            self.save_layout_to_file("layout.json")


if __name__ == '__main__':
    app = SmartHomeGUI()
    app.mainloop()
