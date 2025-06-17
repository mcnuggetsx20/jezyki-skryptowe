import tkinter as tk
from tkinter import ttk, colorchooser

CMD_SET_COLOR = 1
CMD_TOGGLE_ON_OFF = 2
CMD_SET_HOLIDAY = 3

class BulbControlFrame(ttk.Frame):
    def __init__(self, container, dev, app, height=480, width=640):
        super().__init__(container, height=height, width=width)
        self.dev = dev
        self.app = app
        self.width = width
        self.height = height

        self.configure(padding=10)
        self.grid_propagate(False)
        self.columnconfigure(0, weight=1)

        self.current_color = (0, 0, 0)

        # Przycisk wyboru koloru
        self.color_btn = ttk.Button(self, text="Wybierz kolor", command=self.pick_color)
        self.color_btn.grid(row=0, column=0, pady=10, sticky="ew")

        # Przycisk ON/OFF
        self.toggle_btn = ttk.Button(self, text="Włącz/Wyłącz", command=self.toggle)
        self.toggle_btn.grid(row=1, column=0, pady=10, sticky="ew")

        # Tryb świąteczny
        self.holiday_var = tk.BooleanVar()
        self.holiday_check = ttk.Checkbutton(
            self, text="Tryb świąteczny", variable=self.holiday_var, command=self.toggle_holiday
        )
        self.holiday_check.grid(row=2, column=0, pady=10, sticky="w")

        # Podglad koloru
        self.color_preview = tk.Canvas(self, width=100, height=50, bg="#000000", highlightthickness=1, highlightbackground="black")
        self.color_preview.grid(row=3, column=0, pady=10)

    def pick_color(self):
        color_code = colorchooser.askcolor(title="Wybierz kolor")[0]
        if color_code:
            r, g, b = map(int, color_code)
            self.current_color = (r, g, b)
            self.send_color(r, g, b)
            hex_color = f'#{r:02x}{g:02x}{b:02x}'
            self.color_preview.configure(bg=hex_color)

    def send_color(self, r, g, b):
        msg = bytes([CMD_SET_COLOR, r, g, b])
        self.app.server.send_to_client(self.dev["ip"], msg)


    def toggle(self):
        msg = bytes([CMD_TOGGLE_ON_OFF])
        self.app.server.send_to_client(self.dev["ip"], msg)

    def toggle_holiday(self):
        value = 1 if self.holiday_var.get() else 0
        msg = bytes([CMD_SET_HOLIDAY, value])
        self.app.server.send_to_client(self.dev["ip"], msg)
