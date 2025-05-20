import tkinter
from tkinter import filedialog
from tkinter import ttk
from l3 import lib,dicts
import datetime

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

        ## MAIN
        self.main_frame = tkinter.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=10)

        self.main_frame.grid_columnconfigure(0, weight=0)  # DETAIL - nie rośnie
        self.main_frame.grid_columnconfigure(1, weight=1)  # LOG - główny
        self.main_frame.grid_columnconfigure(2, weight=0)  # NAV - wąski

        ## DETAIL
        self.detail_frame = tkinter.Frame(self.main_frame)
        self.detail_frame.grid(row=0, column=0, sticky='n') 
        ##

        ## LOG
        self.log_frame = tkinter.Frame(self.main_frame)
        self.log_frame.grid(row=0, column=1, sticky='nsew')
        self.text_field = tkinter.Text(self.log_frame, wrap='none',width=50)
        # self.text_field.grid(row=0, column=0)
        self.text_field.bind("<Key>", lambda _: 'break')
        self.text_field.pack()
        ##

        ## NAVIGATION
        self.nav_frame = tkinter.Frame(self.main_frame)
        self.nav_frame.grid(row=0, column=2, sticky='ns')
        ##

        self.date_from=None
        self.date_to = None


        return

    def choose_file(self):
        path = filedialog.askopenfilename(
            title="Choose file",
            filetypes=[("Log Files", "*.log")]
        )
        if path:
            print(f"Chose file: {path}")

            for i in self.detail_frame.winfo_children():
                i.destroy()

            self.current_linenr = 0
            self.file_path.text.set(path)
            self.file_data = lib.read_log_from_path(path)
            self.display_log()
            self.prepare_details()
            self.display_details(self.current_linenr)
            self.highlight_line(self.current_linenr+1)

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
            if new_line is None: continue
            strings.append(';'.join([str(i) for i in new_line])[:max_chars]+'...')

        self.clear_text_field()
        self.update_text_field(strings)

        return

    def clear_text_field(self):
        self.text_field.delete('1.0', tkinter.END)
        return

    def update_text_field(self, lines):
        for line in lines:
            self.text_field.insert(tkinter.END, line + '\n')
        return

    def highlight_line(self, line_number, reset=False):
        start = f"{line_number}.0"
        end = f"{line_number+1}.0"

        if reset:
            self.text_field.tag_remove("highlight", "1.0", "end")

        self.text_field.tag_add("highlight", start, end)
        self.text_field.tag_configure("highlight", background="yellow")

    def prepare_details(self, log = None):
        if log is None:
            print('Using default log in prep')
            log = self.file_data

            if not self.file_data:
                print('No valid log to open')
                return

        self.detail_vars = [self.InnerElement(i, '', self.detail_frame) for i in dicts.get_keys()]
        for i, _ in enumerate(self.detail_vars):
            self.detail_vars[i].title_label.grid(row=i, column=0,sticky='w')
            self.detail_vars[i].label.grid(row=i, column=1, sticky='w')

        tkinter.Button(self.nav_frame, text='<-', command=lambda: self.next_log(dir=-1)).grid(row=len(self.detail_vars)-1, column = 5)
        tkinter.Button(self.nav_frame, text='->', command=lambda: self.next_log(dir=1)).grid(row=len(self.detail_vars)-1, column = 6)

        self.date_from = tkinter.Entry(self.nav_frame)
        self.date_to = tkinter.Entry(self.nav_frame)

        self.date_from.bind("<Return>", lambda event: self.parse_date(event, start=-1))
        self.date_to.bind("<Return>", lambda event: self.parse_date(event, start=1))

        self.date_from.grid(row = len(self.detail_vars), column=5)
        self.date_to.grid(row = len(self.detail_vars)+1, column=5)

        return

    def display_details(self, linenr = None):
        if linenr is None:
            if self.current_linenr is None:
                return
            linenr = self.current_linenr
        if not self.file_data: return

        dct = dicts.entry_to_dict(self.file_data[linenr])
        for _, ((_, value), var) in enumerate(zip(dct.items(), self.detail_vars)):
            var.text.set(value)
        return
        
    def next_log(self, dir=0):
        if not dir: return
        if self.current_linenr is None:
            self.current_linenr = 0

        dir = min(1, max(-1, dir))

        self.current_linenr += dir
        self.display_details(self.current_linenr)
        self.highlight_line(self.current_linenr+1, reset=True)
        return

    def parse_date(self, event= None, start=0):
        to = self.date_to.get()
        fr = self.date_from.get()

        if not to or not fr:
            self.display_log()

        # to = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=float(to))
        # fr = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=float(fr))

        to = datetime.datetime.strptime(to, "%Y-%m-%d")
        fr = datetime.datetime.strptime(fr, "%Y-%m-%d")

        def f(line):
            temp = dicts.entry_to_dict(line)
            curr_ts = temp['ts']
            # print(fr, curr_ts, to)
            if fr <= curr_ts <= to: 
                print('ret')
                return line

            else: return None

        self.display_log(_filter=f)

        return

    def run(self):
        self.root.mainloop()

app =App('HTPP log explorer')
app.run()
