from tkinter import Frame, ttk, filedialog
import tkinter as tk
from PIL import Image, ImageTk
import os
import json
import operator

ICON_PATHS = {
    "bulb": "icons/bulb.png",
    "camera": "icons/camera.png",
    "display": "icons/display.png"
}

class MainFrame(ttk.Frame):
    def __init__(self, container, app, height=480, width=640):
        super().__init__(container, height=height, width=width)
        self.app = app
        self.container = container
        self.device_icons = {}
        self.loaded_background_images = {}
        self.dragging_device = None
        self.clicked_device = None
        self.main_frame = None  
        self.canvas_width = 800
        self.canvas_height = 768

        self.load_icons()
        self.create_layout()
        self.load_layout_from_file("layout.json")

    def create_layout(self):
        self.pack(side="top", fill="both", expand=True)

        self.canvas = tk.Canvas(self, bg="white", width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.image_refs = []

        style = ttk.Style()
        style.configure("Blue.TFrame", background="#add8e6")

        self.sidebar = ttk.Frame(self, width=230, style="Blue.TFrame")
        self.sidebar.pack(side="right", fill="y", expand=False)

        ttk.Label(self.sidebar, text="Wszystkie urządzenia:", anchor="center", background="#add8e6").pack(pady=10)
        self.create_scrollable_device_list("Blue.TFrame")


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

        self.floor_label = ttk.Label(self.sidebar, text=f"Piętro: {self.app.floor}")
        self.floor_label.pack()

        self.canvas.bind("<ButtonPress-1>", self.on_canvas_left_press)
        self.canvas.bind("<B1-Motion>", self.on_canvas_left_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_left_release)
        self.canvas.bind("<Button-3>", self.on_canvas_right_click)

        self.bind("<Configure>", self.on_resize)
        
        self.update_idletasks()
        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()

        self.refresh_device_list()
        self.draw_devices_on_canvas()

    def create_scrollable_device_list(self, style):
        container = ttk.Frame(self.sidebar)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="#add8e6", highlightthickness=0, width=210)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.device_list_frame = ttk.Frame(canvas, style=style)

        self.device_list_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.device_list_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="y", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.device_canvas = canvas


    def load_icons(self):
        for name, path in ICON_PATHS.items():
            if os.path.exists(path):
                img = Image.open(path).resize((48, 48))
                self.device_icons[name] = ImageTk.PhotoImage(img)
            else:
                self.device_icons[name] = None

    def refresh_device_list(self):
        for widget in self.device_list_frame.winfo_children():
            widget.destroy()

        columns = 3
        row = 0
        col = 0

        for dev in self.app.devices:
            frame = ttk.Frame(self.device_list_frame, relief="raised", padding=4)
            frame.grid(row=row, column=col, padx=5, pady=5)

            icon = self.device_icons.get(dev['type'])
            if icon:
                label = tk.Label(frame, image=icon)
                label.image = icon
                label.pack()
                label.bind("<ButtonPress-1>", lambda e, d=dev: self.open_device_panel(e,d))
                label.bind("<Button-3>", lambda event, dev=dev: self.on_device_list_right_click(event, dev))
            tk.Label(frame, text=dev['name'], wraplength=50).pack()

            col += 1
            if col >= columns:
                col = 0
                row += 1

    def on_device_list_right_click(self, event, dev):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Add to floor", command=lambda dev=dev: self.add_to_floor_device(dev))
        self.context_menu.tk_popup(event.x_root, event.y_root)

    def add_to_floor_device(self, dev):
        dev["x"] = 0.5
        dev["y"] = 0.5
        dev["floor"] = self.app.floor_names[self.app.floor]
        self.draw_devices_on_canvas()

    def draw_devices_on_canvas(self):
        self.canvas.delete("all")
        self.canvas.image_refs.clear()

        bg_path = self.app.floor_backgrounds.get(self.app.floor)
        if bg_path and os.path.exists(bg_path):
            if self.app.floor not in self.loaded_background_images:
                img = Image.open(bg_path).resize((self.canvas_width, self.canvas_height))
                self.loaded_background_images[self.app.floor] = ImageTk.PhotoImage(img)
            bg_img = self.loaded_background_images[self.app.floor]
            self.canvas.create_image(0, 0, image=bg_img, anchor="nw")
            self.canvas.image_refs.append(bg_img)
        else:
            self.canvas.config(bg="white")

        for dev in self.app.devices:
            if dev["floor"] != self.app.floor_names[self.app.floor]:
                continue
            icon = self.device_icons.get(dev['type'])
            if icon:
                x = int(dev['x'] * self.canvas_width)
                y = int(dev['y'] * self.canvas_height)
                img_id = self.canvas.create_image(x, y, image=icon, anchor="center", tags=("device",))
                self.canvas.image_refs.append(icon)
                self.canvas.tag_bind(img_id, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
                self.canvas.tag_bind(img_id, "<Leave>", lambda e: self.canvas.config(cursor=""))

    def find_device_by_canvas_coords(self, x, y):
        for dev in self.app.devices:
            if dev["floor"] != self.app.floor_names[self.app.floor]:
                continue
            dx = dev['x'] * self.canvas_width - x
            dy = dev['y'] * self.canvas_height - y
            if dx*dx + dy*dy <= 30*30:
                return dev
        return None

    def on_canvas_left_press(self, event):
        dev = self.find_device_by_canvas_coords(event.x, event.y)
        if dev:
            self.dragging_device = dev
            self.drag_offset_x = event.x - dev['x'] * self.canvas_width
            self.drag_offset_y = event.y - dev['y'] * self.canvas_height
            self.clicked_device = dev
        else:
            self.dragging_device = None
            self.clicked_device = None

    def on_canvas_left_drag(self, event):
        if self.dragging_device:
            new_x = (event.x - self.drag_offset_x) / self.canvas_width
            new_y = (event.y - self.drag_offset_y) / self.canvas_height
            self.dragging_device['x'] = max(0, min(new_x, 1))
            self.dragging_device['y'] = max(0, min(new_y, 1))
            self.draw_devices_on_canvas()

    def on_canvas_left_release(self, event):
        self.app.save_layout_to_file("layout.json")

    def on_canvas_right_click(self, event):
        dev = self.find_device_by_canvas_coords(event.x, event.y)
        if dev and dev["floor"] == self.app.floor_names[self.app.floor]:
            self.context_menu = tk.Menu(self, tearoff=0)
            self.context_menu.add_command(label="Usuń z piętra", command=lambda dev=dev: self.remove_from_floor(dev))
            self.context_menu.tk_popup(event.x_root, event.y_root)

    def remove_from_floor(self, dev):
        dev["floor"] = None
        self.draw_devices_on_canvas()
        self.app.save_layout_to_file("layout.json")

    def open_device_panel(self, event, device):
        self.app.open_device_panel(device)

    def go_up_floor(self):
        if self.app.floor < self.app.total_floors - 1:
            self.app.floor += 1
            self.update_floor_label()
            self.draw_devices_on_canvas()

    def go_down_floor(self):
        if self.app.floor > 0:
            self.app.floor -= 1
            self.update_floor_label()
            self.draw_devices_on_canvas()

    def update_floor_label(self):
        if 0 <= self.app.floor < len(self.app.floor_names):
            name = self.app.floor_names[self.app.floor]
        else:
            name = f"Piętro {self.app.floor}"
        self.floor_label.config(text=f"Piętro: {name}")

    def add_new_device(self):
        name = self.new_dev_name.get().strip()
        typ = self.new_dev_type.get()
        if name and typ in ICON_PATHS:
            dev = {"name": name, "type": typ, "x": 0.5, "y": 0.5, "floor": None}
            self.app.devices.append(dev)
            self.refresh_device_list()
            self.draw_devices_on_canvas()
            self.new_dev_name.set("")
            self.app.save_layout_to_file("layout.json")

    def load_layout_from_file(self, filename):
        if os.path.exists(filename):
            with open(filename) as f:
                data = json.load(f)
            self.app.total_floors = data.get("floors", 1)
            self.app.floor_names = data.get("floor_names", [f"Piętro {i}" for i in range(self.app.total_floors)])
            self.app.devices = data.get("devices", [])
            self.app.floor_backgrounds = data.get("backgrounds", {})
        else:
            self.app.total_floors = 1
            self.app.floor_names = ["Piętro 0"]
            self.app.devices = []
            self.app.floor_backgrounds = {}

        self.loaded_background_images.clear()
        self.floor = 0
        self.update_floor_label()
        self.refresh_device_list()
        self.draw_devices_on_canvas()
    
    def on_resize(self, event):
        if event.widget == self:
            self.update_idletasks()
            self.canvas_width = self.canvas.winfo_width()
            self.canvas_height = self.canvas.winfo_height()

            self.draw_devices_on_canvas()
