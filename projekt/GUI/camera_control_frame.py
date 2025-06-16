import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import socket
import threading
import io
import time

class CameraControlFrame(ttk.Frame):
    def __init__(self, container, dev, app, height=480, width=640):
        super().__init__(container, height=height, width=width)
        self.dev = dev
        self.app = app
        self.width = width
        self.height = height

        self.canvas = tk.Canvas(self, bg="black")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.sidebar = ttk.Frame(self)
        self.sidebar.grid(row=0, column=1, sticky="ns", padx=10)

        # Opcje z boku
        self.motion_var = tk.BooleanVar()
        self.motion_chk = ttk.Checkbutton(self.sidebar, text="Wykrywanie ruchu", variable=self.motion_var)
        self.motion_chk.pack(anchor="w", pady=5)

        self.status = ttk.Label(self.sidebar, text="Status: brak połączenia")
        self.status.pack(anchor="w", pady=5)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.image_on_canvas = None

        # Rozpocznij odbiór po TCP
        self.running = True
        self.app.clear_buffer = False
        thread = threading.Thread(target=self.receive_commands_from_server, daemon=True)
        thread.start()

    def receive_commands_from_server(self):
        while self.running:
            # Iteruj po wszystkich frame'ach w kolejce serwera
            while self.app.server.recv_queue:
                frame_info = self.app.server.recv_queue.pop(0)  # weź pierwszy

                # Sprawdź, czy ten frame jest dla device, który nas interesuje (np. po fd)
                fd = frame_info['fd']

                if fd != self.dev['fd']:
                    continue  # pomiń, jeśli nie dotyczy
                if(frame_info['command'] == 3):
                    data = frame_info['data']

                    # Pierwsze 4 bajty to długość ramki (big endian)
                    size_bytes = data[:4]
                    frame_size = int.from_bytes(size_bytes, byteorder='big')

                    # JPEG 
                    jpeg_data = data[4:4+frame_size]
                    image = Image.open(io.BytesIO(jpeg_data))
                    self.update_image(self, image)
            time.sleep(0.06)

    def update_image(self, pil_image):
        # Przeskaluj z zachowaniem proporcji i centrowaniem
        img_w, img_h = pil_image.size
        scale = min(self.width / img_w, self.height / img_h)
        new_w, new_h = int(img_w * scale), int(img_h * scale)
        resized = pil_image.resize((new_w, new_h), Image.ANTIALIAS)

        self.tk_image = ImageTk.PhotoImage(resized)

        x = (self.width - new_w) // 2
        y = (self.height - new_h) // 2

        self.canvas.delete("all")
        self.image_on_canvas = self.canvas.create_image(x, y, anchor="nw", image=self.tk_image)

    def destroy(self):
        self.running = False
        self.app.clear_buffer = True
        super().destroy()
