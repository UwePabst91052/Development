import tkinter as tk
from tkinter import filedialog
from ReadWorkpackes import read_workpackages
from StoreWorkpackages import write_workpackage
from StoreWorkpackages import open_tag
from StoreWorkpackages import close_tag
import Workpackage as Wp


class EditWorkpackage(tk.Frame):
    def __init__(self, parent, row, col, title, width, ltype):
        super().__init__(parent)

        self._type = ltype
        
        # Label
        self.label_wp = tk.Label(self, text=title)
        self.label_wp.pack(anchor='w')

        # Entry
        self.wp_text = tk.StringVar()
        self.wp_entry = tk.Entry(self, textvariable=self.wp_text, width=width)
        self.wp_entry.pack()

        # Listbox
        self.list_content = tk.StringVar()
        self.wp_list = tk.Listbox(self, listvariable=self.list_content, width=width)
        self.wp_list.bind("<Button-1>", self.wp_selcted)
        self.wp_list.pack()

        self.grid(row=row, column=col)

    def wp_selcted(self, event):
        x = event.x
        y = event.y
        ix = self.wp_list.index("@" + str(x) + ", " + str(y))
        fill_child_list(self._type, ix)

    def add_items(self, item_list):
        self.wp_list.delete(0, last=tk.END)
        for item in item_list:
            self.wp_list.insert(tk.END, item)
        self.wp_list.selection_set(0)

    def update_list(self, ltype, item_list):
        lines = []
        if ltype == 'wp':
            for wp in item_list:
                lines.append(wp.wp_name)
        elif ltype == 'wd':
            for wd in item_list:
                lines.append((str(wd.date)))
        elif ltype == 'bt':
            for wt in item_list:
                lines.append(str(wt.start_time))
        else:
            for wt in item_list:
                lines.append(str(wt.end_time))
        self.add_items(lines)


def load_wpckgs():
    global workpackages, filename
    if len(workpackages) > 0:
        create_new_file()
    filename = filedialog.askopenfilename(initialdir='./Dateien')
    file = open(filename, 'r', encoding='utf-8')
    wp_name_list = []
    wd_list = []
    begin_list = []
    end_list = []
    workpackages = read_workpackages(file)
    file.close()
    for wp in workpackages:
        wp_name_list.append(wp.wp_name)
    wp = workpackages[0]
    for wd in wp.workdays:
        wd_list.append(str(wd.date))
    wd = wp.workdays[0]
    for wt in wd.worktimes:
        begin_list.append(str(wt.start_time))
        end_list.append(str(wt.end_time))
    list_wp.add_items(wp_name_list)
    list_wd.add_items(wd_list)
    list_begin.add_items(begin_list)
    list_end.add_items(end_list)


def save_wpckgs():
    global workpackages, filename
    if filename:
        file = open(filename, 'w', encoding='utf-8')
        open_tag(file, "Zeiterfassung")
        for wp in workpackages:
            write_workpackage(file, wp)
        close_tag(file, "Zeiterfassung")
        file.close()


def save_wpckgs_as():
    global filename
    filename = filedialog.asksaveasfilename(initialdir='./Dateien', defaultextension='.xml',
                                            filetypes=[('XML', '*.xml')])
    save_wpckgs()


def fill_child_list(ltype, index):
    global wp_ix, wd_ix, bt_ix, et_ix
    if ltype == 'wp':
        wp_ix = index
        wp = workpackages[wp_ix]
        wd_list = []
        begin_list = []
        end_list = []
        list_wp.wp_text.set(wp.wp_name)
        list_wd.wp_text.set("")
        list_begin.wp_text.set("")
        list_end.wp_text.set("")
        for wd in wp.workdays:
            wd_list.append(str(wd.date))
        wd = wp.workdays[0]
        for wt in wd.worktimes:
            begin_list.append(str(wt.start_time))
            end_list.append(str(wt.end_time))
        list_wd.add_items(wd_list)
        list_begin.add_items(begin_list)
        list_end.add_items(end_list)
    elif ltype == 'wd':
        wd_ix = index
        wp = workpackages[wp_ix]
        wd = wp.workdays[wd_ix]
        begin_list = []
        end_list = []
        list_wd.wp_text.set(str(wd.date))
        list_begin.wp_text.set("")
        list_end.wp_text.set("")
        for wt in wd.worktimes:
            begin_list.append(str(wt.start_time))
            end_list.append(str(wt.end_time))
        list_begin.add_items(begin_list)
        list_end.add_items(end_list)
    elif ltype == 'bt':
        bt_ix = index
        wp = workpackages[wp_ix]
        wd = wp.workdays[wd_ix]
        wt = wd.worktimes[bt_ix]
        list_begin.wp_text.set(str(wt.start_time))
    else:
        et_ix = index
        wp = workpackages[wp_ix]
        wd = wp.workdays[wd_ix]
        wt = wd.worktimes[et_ix]
        list_end.wp_text.set(str(wt.end_time))


def create_new_file():
    global workpackages, wp_ix, wd_ix, bt_ix, et_ix, filename
    workpackages = []
    filename = ""
    wp_ix = 0
    wd_ix = 0
    bt_ix = 0
    et_ix = 0


def apply_values():
    # get entry values
    wp_name = list_wp.wp_text.get()
    wd_date = list_wd.wp_text.get()
    begin_time = list_begin.wp_text.get()
    end_time = list_end.wp_text.get()
    # get selected objects
    wp_cur = workpackages[wp_ix]
    wd_cur = wp_cur.workdays[wd_ix]
    wt_cur = wd_cur.worktimes[bt_ix]
    if wp_name != "" and wp_cur.wp_name != wp_name:
        wp_cur.wp_name = wp_name
        list_wp.update_list('wp', workpackages)
    if wd_date != "" and wd_cur.date != wd_date:
        wd_cur.date = Wp.Date(wd_date)
        list_wd.update_list('wd', wp_cur.workdays)
    if begin_time != "" and wt_cur.start_time != begin_time:
        wt_cur.start_time = Wp.Time(begin_time)
        list_begin.update_list('bt', wd_cur.worktimes)
    if end_time != "" and wt_cur.end_time != end_time:
        wt_cur.end_time = Wp.Time(end_time)
        list_end.update_list('et', wd_cur.worktimes)


workpackages = []
filename = ""
wp_ix = 0
wd_ix = 0
bt_ix = 0
et_ix = 0

root = tk.Tk()
root.title("Zeitkorrektur")
root.resizable(False, False)

menu_bar = tk.Menu(root)
root['menu'] = menu_bar
sub_menu = tk.Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label='Datei', menu=sub_menu)
sub_menu.add_command(label='Öffnen', command=load_wpckgs)
sub_menu.add_command(label='Speichern', command=save_wpckgs)
sub_menu.add_command(label='Speichern unter...', command=save_wpckgs_as)

list_wp = EditWorkpackage(root, 0, 0, "Arbeitspakete", 20, 'wp')
list_wd = EditWorkpackage(root, 0, 2, "Arbeitstage", 10, 'wd')
list_begin = EditWorkpackage(root, 0, 3, "Beginn", 8, 'bt')
list_end = EditWorkpackage(root, 0, 4, "Ende", 8, 'et')

button_apply = tk.Button(root, text='Übernehmen', command=apply_values)
button_apply.grid(row=1, column=0, columnspan=2)

button_add = tk.Button(root, text='Hinzufügen')
button_add.grid(row=1, column=2, columnspan=3)

root.mainloop()
