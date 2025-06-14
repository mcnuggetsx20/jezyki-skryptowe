from tkinter import Frame, ttk, filedialog
import tkinter as tk
from PIL import Image, ImageTk

class MenuBar(Frame):
    def __init__(self, container, app, height = 10):
        super().__init__(container, height=height)

        self.app = app

        self.pack(side="top", fill="x")
        ttk.Button(self, text="Settings", command=self.menu_bar_settings).pack(side="left", padx=5)
        
    def menu_bar_settings(self):
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Manage floors", command=lambda: self.manage_floors())
        self.context_menu.add_command(label="Set floor's background", command=lambda: self.set_floor_background())
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Usuń z piętra", command=lambda: self.remove_device_from_floor(dev))
        self.context_menu.tk_popup(self.winfo_rootx(), self.winfo_rooty() + self.winfo_height())
    
    def manage_floors(self):
        win = tk.Toplevel(self)
        win.title("Manage floors")
        win.transient(self.app)
        win.grab_set()

        floor_list_frame = ttk.Frame(win)
        floor_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        floor_vars = [tk.StringVar(value=name) for name in self.app.floor_names]

        def refresh_floor_list():
            for widget in floor_list_frame.winfo_children():
                widget.destroy()

            for idx, var in enumerate(floor_vars):
                row = ttk.Frame(floor_list_frame)
                row.pack(fill="x", pady=2)

                entry = ttk.Entry(row, textvariable=var)
                entry.pack(side="left", fill="x", expand=True)

                btns = ttk.Frame(row)
                btns.pack(side="right")

                arrow_frame = ttk.Frame(btns)
                arrow_frame.pack(side="left")

                if idx > 0:
                    ttk.Button(arrow_frame, text="↑", width=2, command=lambda i=idx: move_up(i)).pack(side="top")
                if idx < len(floor_vars) - 1:
                    ttk.Button(arrow_frame, text="↓", width=2, command=lambda i=idx: move_down(i)).pack(side="top")

                ttk.Button(btns, text="❌", width=2, command=lambda i=idx: remove_floor(i)).pack(side="left", padx=(5,0))

        def move_up(i):
            floor_vars[i - 1], floor_vars[i] = floor_vars[i], floor_vars[i - 1]
            refresh_floor_list()

        def move_down(i):
            floor_vars[i], floor_vars[i + 1] = floor_vars[i + 1], floor_vars[i]
            refresh_floor_list()

        def remove_floor(i):
            if len(floor_vars) > 1:
                del floor_vars[i]
                refresh_floor_list()

        def add_floor():
            floor_vars.append(tk.StringVar(value=f"Nowe piętro {len(floor_vars)}"))
            refresh_floor_list()

        def apply_settings():
            names = [var.get().strip() for var in floor_vars if var.get().strip()]
            if names:
                self.app.floor_names = names
                self.app.total_floors = len(names)
                self.app.floor = min(self.app.floor, len(names) - 1)
                self.app.floor_label.config(text=f"Piętro: {self.app.floor_names[self.app.floor]}")
                self.app.draw_devices_on_canvas()
                self.app.save_layout_to_file("layout.json")
            win.destroy()

        ttk.Button(win, text="Dodaj piętro", command=add_floor).pack(pady=(5, 0))
        ttk.Button(win, text="Zastosuj", command=apply_settings).pack(pady=10)

        refresh_floor_list()

    
    def set_floor_background(self):
        win = tk.Toplevel(self)
        win.title("Ustaw tło piętra")
        win.transient(self) 
        win.grab_set()

        # Dropdown do wyboru piętra
        tk.Label(win, text="Wybierz piętro:").pack(pady=5)
        floor_name_var = tk.StringVar(value=self.app.floor_names[self.app.floor])
        floor_menu = ttk.Combobox(
            win,
            textvariable=floor_name_var,
            values=self.app.floor_names,
            state="readonly"
        )
        floor_menu.pack(pady=5)

        def choose_file():
            filepath = filedialog.askopenfilename(filetypes=[("Obrazy", "*.png *.jpg *.jpeg *.bmp")])
            if filepath:
                canvas_width = self.app.canvas.winfo_width() or self.app.winfo_width()
                canvas_height = self.app.canvas.winfo_height() or self.app.winfo_height()

                try:
                    img = Image.open(filepath).resize((canvas_width, canvas_height))
                    photo = ImageTk.PhotoImage(img)
                except Exception as e:
                    tk.messagebox.showerror("Błąd", f"Nie udało się załadować obrazu:\n{e}")
                    return

                try:
                    floor = self.app.floor_names.index(floor_name_var.get())
                except ValueError:
                    tk.messagebox.showerror("Błąd", "Nieprawidłowe piętro.")
                    return

                self.app.loaded_background_images[floor] = photo
                self.app.floor_backgrounds[floor] = filepath

                if self.app.floor == floor:
                    self.app.draw_devices_on_canvas()

                self.app.save_layout_to_file("layout.json")
                win.destroy()

        ttk.Button(win, text="Wybierz obraz...", command=choose_file).pack(pady=10)
        ttk.Button(win, text="Anuluj", command=win.destroy).pack(pady=5)


