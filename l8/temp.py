
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.geometry("960x600")
root.configure(bg="lightgray")

# Górny pasek
top_frame = tk.Frame(root, bg="lightgray")
top_frame.pack(fill='x', pady=5)

tk.Label(top_frame, text="Log File:", bg="lightgray").pack(side="left", padx=5)

filepath_var = tk.StringVar(value="No file chosen")
tk.Label(top_frame, textvariable=filepath_var, bg="lightgray", anchor='w').pack(side="left", fill='x', expand=True)

tk.Button(top_frame, text="Choose file").pack(side="right", padx=5)
tk.Button(top_frame, text="Zamknij", command=root.destroy).pack(side="right", padx=5)

# Środkowy panel z metadanymi + logiem
main_frame = tk.Frame(root, bg="lightgray")
main_frame.pack(fill='both', expand=True, padx=10)

# Lewa kolumna z metadanymi
meta_frame = tk.Frame(main_frame, bg="lightgray")
meta_frame.pack(side="left", anchor='n', padx=5)

# Przykład danych
data_fields = {
    "ts": "2012-03-16 12:30:00",
    "uid": "CHEt7z3AzG4gyCNgci",
    "id.orig_h": "192.168.202.79",
    "id.resp_h": "192.168.229.251",
    "status_code": 404,
}

for i, (key, value) in enumerate(data_fields.items()):
    tk.Label(meta_frame, text=key + ":", bg="lightgray", anchor='w').grid(row=i, column=0, sticky='w')
    tk.Label(meta_frame, text=value, bg="lightgray", anchor='w').grid(row=i, column=1, sticky='w')

# Prawa część: strzałki + Text
log_frame = tk.Frame(main_frame)
log_frame.pack(side="left", fill='both', expand=True)

# Przyciski strzałek
nav_frame = tk.Frame(log_frame)
nav_frame.pack()

tk.Button(nav_frame, text="<-").pack(side='left', padx=5)
tk.Button(nav_frame, text="->").pack(side='left', padx=5)

# Pole logu
log_text = tk.Text(log_frame, wrap='none', height=25)
log_text.pack(fill='both', expand=True)

root.mainloop()
