import tkinter
from tkinter import filedialog
from tkinter import ttk
from l3 import lib

class App:

    class InnerElement:
        def __init__(self, user_text, root):
            self.text= tkinter.StringVar()
            self.text.set(user_text)

            self.label = tkinter.Label(root, textvariable=self.text)
            return

    def __init__(self, title):
        self.root = tkinter.Tk()
        self.root.title(title)

        self.file_data = None

        self.root.grid_columnconfigure(0, weight = 1)
        self.root.grid_columnconfigure(1, weight = 2)
        self.root.grid_columnconfigure(2, weight = 1)

        self.file_path = self.InnerElement("No file chosen", self.root)
        self.file_path.label.grid(row=0, column=1,sticky='ew')

        self.text_field = tkinter.Text(self.root, wrap='none')
        self.text_field.grid(row=1, column=1)
        self.text_field.bind("<Key>", lambda _: 'break')

        tkinter.Label(self.root, text='Log File:').grid(row=0, column=0,sticky='w')
        tkinter.Button(self.root, text="Choose file", command=self.choose_file).grid(row=0, column=2, sticky='e')
        tkinter.Button(self.root, text="Zamknij", command=self.root.destroy).grid()

        return

    def choose_file(self):
        path = filedialog.askopenfilename(
            title="Choose file",
            filetypes=[("Log Files", "*.log")]
        )
        if path:
            print(f"Chose file: {path}")

        self.file_path.text.set(path)
        self.file_data = lib.read_log_from_path(path)
        self.display_log()

        return

    def display_log(self, log = None, max_chars = 30, _filter = lambda line: line):
        if log is None:
            print('Using default log')
            log = self.file_data

            if self.file_data is None:
                print('No valid log to open')
                return

        strings = []
        for num, line in enumerate(log):
            new_line = _filter(line)
            strings.append(';'.join([str(i)[:max_chars] for i in new_line])+'...')

        self.clear_text_field()
        self.update_text_field(strings)
        self.highlight_line(2)

        return

    def clear_text_field(self):
        self.text_field.delete('1.0', tkinter.END)
        return

    def update_text_field(self, lines):
        for line in lines:
            self.text_field.insert(tkinter.END, line + '\n')
        return

    def highlight_line(self, line_number):
        start = f"{line_number}.0"
        end = f"{line_number+1}.0"

        self.text_field.tag_add(f"line{line_number}", start, end)
        self.text_field.tag_configure(f"line{line_number}", background="yellow")

    def run(self):
        self.root.mainloop()

app =App('HTPP log explorer')
app.run()
