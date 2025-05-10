import tkinter
from tkinter import filedialog
from tkinter import ttk
from l3 import lib,dicts

class App:

    class InnerElement:
        def __init__(self, title, user_text, root):
            self.text= tkinter.StringVar()
            self.text.set(user_text)

            self.title_label=tkinter.Label(root, text=title)
            self.label = tkinter.Label(root, textvariable=self.text)
            return

    def __init__(self, title):
        self.root = tkinter.Tk()
        self.root.title(title)

        self.file_data = None
        self.current_linenr = None
        self.detail_vars = []

        self.root.grid_columnconfigure(0, weight = 1)
        self.root.grid_columnconfigure(1, weight = 1)
        self.root.grid_columnconfigure(2, weight = 1)

        ## HEADER
        self.header_frame = tkinter.Frame(self.root)
        self.header_frame.grid_columnconfigure(1, weight = 1)
        self.header_frame.pack(side='top', fill='x')

        self.file_path = self.InnerElement('Log File', "No file chosen", self.header_frame)
        self.file_path.label.grid(row=0, column=1,sticky='ew')

        self.file_path.title_label.grid(row=0, column=0,sticky='w')
        tkinter.Button(self.header_frame, text="Choose file", command=self.choose_file).grid(row=0, column=2, sticky='e')
        tkinter.Button(self.header_frame, text="Zamknij", command=self.root.destroy).grid()
        ##

        ## DETAIL
        self.detail_frame = tkinter.Frame(self.root)
        self.detail_frame.pack(side='top', fill='x')

        self.text_field = tkinter.Text(self.detail_frame, wrap='none')
        self.text_field.grid(row=0, column=0)
        self.text_field.bind("<Key>", lambda _: 'break')

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
            self.prepare_details()
            self.display_details(0)

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
            strings.append(';'.join([str(i) for i in new_line])[:max_chars]+'...')

        self.clear_text_field()
        self.update_text_field(strings)
        # self.highlight_line(2)

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

    def prepare_details(self, log = None):
        if log is None:
            print('Using default log in prep')
            log = self.file_data

            if not self.file_data:
                print('No valid log to open')
                return

        self.detail_vars = [self.InnerElement(i, '', self.detail_frame) for i in dicts.get_keys()]
        for i, _ in enumerate(self.detail_vars):
            self.detail_vars[i].title_label.grid(row=i, column=1)
            self.detail_vars[i].label.grid(row=i, column=2)
        return

    def display_details(self, linenr = None):
        if linenr is None:
            if self.current_linenr is None:
                return
            linenr = self.current_linenr
            

        dct = dicts.entry_to_dict(self.file_data[linenr])
        for _, ((_, value), var) in enumerate(zip(dct.items(), self.detail_vars)):
            var.text.set(value)
        return
        

    def run(self):
        self.root.mainloop()

app =App('HTPP log explorer')
app.run()
