import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import socket
import threading
import io
import time
import cv2

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
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor="nw")
        # Rozpocznij odbiór po TCP
        self.running = True
        self.app.clear_buffer = False
        thread = threading.Thread(target=self.receive_commands_from_server, daemon=True)
        thread.start()
        self.tk_image = None
        self.after(50, self.update_now)

    def receive_commands_from_server(self):
        while self.running:
            # Iteruj po wszystkich frame'ach w kolejce serwera
            while self.app.server.recv_queue:
                frame_info = self.app.server.recv_queue.pop(0) 

                # Sprawdź, czy ten frame jest dla device
                fd = frame_info['fd']

                if fd != self.dev['fd']:
                    print(fd)
                    print(self.dev['fd'])
                    continue  # pomiń, jeśli nie dotyczy
                if(frame_info['command'] == 3):
                    data = frame_info['data']
                    if data is None:
                        break
                    rgb_frame = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
                    pil_image = Image.fromarray(rgb_frame)

                    self.update_image(pil_image)
 
            time.sleep(0.06)

    def update_image(self, pil_image):
        img_w, img_h = pil_image.size
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()

        # Gdy rozmiar canvas jest 0, wartosci domyslne
        if canvas_w <= 0 or canvas_h <= 0:
            canvas_w = self.width
            canvas_h = self.height

        scale = min(canvas_w / img_w, canvas_h / img_h)

        # Oblicz nowe rozmiary obrazka
        new_w = max(1, int(img_w * scale)) 
        new_h = max(1, int(img_h * scale))

        # Skaluj obraz
        resized = pil_image.resize((new_w, new_h), Image.Resampling.LANCZOS)

        self.tk_image = ImageTk.PhotoImage(resized)

        # Wyśrodkuj obraz na canvasie
        x = (canvas_w - new_w) // 2
        y = (canvas_h - new_h) // 2

        self.canvas.coords(self.image_on_canvas, x, y)

    def update_now(self):
        if self.running:
            self.image_for_now = self.tk_image
            self.canvas.itemconfig(self.image_on_canvas, image=self.image_for_now)
            self.after(50, self.update_now)

    def destroy(self):
        self.running = False
        self.app.clear_buffer = True
        super().destroy()
