import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import socket
import threading
import io

class CameraControlFrame(ttk.Frame):
    def __init__(self, container, dev, app, height=480, width=640):
        super().__init__(container, height=height, width=width)
        self.dev = dev
        self.dev_ip = dev
        self.app = app
        self.width = width
        self.height = height

        self.canvas = tk.Canvas(self, width=width, height=height, bg="black")
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
        self.thread = threading.Thread(target=self.receive_tcp_stream, daemon=True)
        self.thread.start()

    def receive_tcp_stream(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.dev_ip, 12345)) 
                self.status.config(text="Połączono z kamerą")

                buffer = b""
                while self.running:
                    data = s.recv(4096)
                    if not data:
                        break
                    buffer += data

                    if b"\xff\xd9" in buffer:
                        end = buffer.index(b"\xff\xd9") + 2
                        jpg_data = buffer[:end]
                        buffer = buffer[end:]

                        image = Image.open(io.BytesIO(jpg_data))
                        self.update_image(image)

        except Exception as e:
            self.status.config(text=f"Błąd: {e}")

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
        super().destroy()
