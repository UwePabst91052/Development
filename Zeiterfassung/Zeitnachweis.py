import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import Workpackage as Wp
import datetime as dt
import os as os
from ReadWorkpackes import read_workpackages
from StoreWorkpackages import write_workpackage
from StoreWorkpackages import open_tag
from StoreWorkpackages import close_tag
from BerichtAnzeigen import display_report
from BerichtAnzeigen import input_timespan
from BerichtAusdrucken import report_work_summary
from BerichtAusdrucken import report_work_summary_timespan
from BerichtAusdrucken import report_workday_summary
from BerichtAusdrucken import report_workpackage_summary
from Zeitkorrektur import CorrectionDialog


class DispWorkpackages(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(borderwidth=3, relief='groove')
        label1 = tk.Label(self, text="Wählen Sie das Arbeitspaket")
        label1.grid(row=0, column=0, padx=10, sticky='W')
        label2 = tk.Label(self, text="Datum")
        label2.grid(row=0, column=2, padx=5, sticky='W')

        self.wp_name = tk.StringVar()
        self.select_wp = ttk.Combobox(self)
        self.select_wp["textvariable"] = self.wp_name
        self.select_wp["values"] = ()
        self.select_wp.bind('<<ComboboxSelected>>', self.workpackage_selected)
        self.select_wp.grid(row=1, column=0, columnspan=2, padx=10, sticky='W')
        self.wd_date = tk.StringVar()
        self.date_entry = tk.Entry(self, textvariable=self.wd_date, width=10)
        self.date_entry.grid(row=1, column=2, padx=5)

        self.add_wp_button = tk.Button(self, text="Hinzufügen")
        self.add_wp_button['command'] = self.add_workpackage
        self.add_wp_button.grid(row=1, column=1, sticky='W')

        self.begin_time = tk.StringVar()
        self.begin_entry = tk.Entry(self, textvariable=self.begin_time, width=8)
        self.begin_entry.grid(row=2, column=0, padx=10, sticky='E')
        self.begin_button = tk.Button(self, text="Beginne", command=self.begin_work)
        self.begin_button.grid(row=2, column=1, sticky='W')

        self.end_time = tk.StringVar()
        self.end_entry = tk.Entry(self, textvariable=self.end_time, width=8)
        self.end_entry.grid(row=2, column=2, padx=5, sticky='W')
        self.end_button = tk.Button(self, text="Beende", command=self.end_work)
        self.end_button.grid(row=2, column=3, sticky='W')

        self.pack(anchor='nw')

    def add_wp_names(self, wp_list):
        global workpackages
        self.select_wp['values'] = wp_list
        self.select_wp.current(0)
        wp_cur = workpackages[0]
        overview.fill_dates(wp_cur)

    def add_workpackage(self):
        global workpackages
        wp_name = self.select_wp.get()
        if wp_name not in self.select_wp['values']:
            self.select_wp['values'] += (wp_name,)
            wp = Wp.Workpackage(wp_name)
            workpackages.append ( wp )
        else:
            wp = workpackages[self.select_wp.current()]
        date = self.wd_date.get()
        if date == "":
            date = dt.date.today().strftime("%d.%m.")
            date = str(Wp.Date(date))
            wp.add_workday(date)
            self.wd_date.set(date)
        else:
            wp.add_workday(date)
        overview.fill_dates(wp)

    def begin_work(self):
        time = self.begin_time.get()
        date = self.wd_date.get()
        ix = self.select_wp.current()
        if ix >= 0:
            wp_cur = workpackages[ix]
            if date == "":
                wp_cur.add_workday(dt.date.today().strftime("%d.%m.%Y"))
            else:
                wp_cur.add_workday(date)
            if time == "":
                time = input_time()
                wp_cur.begin_working(time)
                self.begin_time.set(time)
            else:
                wp_cur.begin_working(time)

    def end_work(self):
        time = self.end_time.get()
        ix = self.select_wp.current()
        if ix >= 0:
            wp_cur = workpackages[ix]
            if time == "":
                time = input_time()
                wp_cur.finish_working(time)
                self.begin_time.set("")
            else:
                wp_cur.finish_working(time)
            overview.fill_times(wp_cur.cur_workday)

    @staticmethod
    def workpackage_selected(event):
        global overview
        ix = event.widget.current()
        if ix >= 0:
            wp_cur = workpackages[ix]
            overview.fill_dates(wp_cur)


class DisplayWorkdays(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label_wd = tk.Label(self, text="Arbeitstage")
        self.label_wd.grid(row=0, column=0)
        datelist = tk.StringVar()
        self.listbox_wd = tk.Listbox(self, listvariable=datelist, width=11)
        self.listbox_wd.bind('<Button-1>', self.date_selected)
        self.listbox_wd.grid(row=1, column=0, padx=10)

        self.label_times = tk.Label(self, text="Arbeitszeiten")
        self.label_times.grid(row=0, column=1)
        self.list_times = tk.Label(self, width=30, height=10, bg='white', anchor=tk.NW, relief='sunken')
        self.list_times.grid(row=1, column=1, sticky=tk.NW)

        self.pack()

    def fill_dates(self, workpackage):
        self.listbox_wd.delete(0, last=tk.END)
        self.list_times['text'] = ""
        for wd in workpackage.workdays:
            self.listbox_wd.insert(tk.END, str(wd.date))

    def fill_times(self, workday):
        self.list_times['text'] = ""
        for wt in workday.worktimes:
            times = str(wt).split(' ')
            self.list_times['text'] += times[0] + " | " + times[1] + " || " + times[2] + '\n'
        self.list_times['text'] += "         Summe:            {0}".format(workday.get_duration_str())

    def date_selected(self, event):
        x = event.x
        y = event.y
        ix = self.listbox_wd.index("@" + str(x) + ", " + str(y))
        ix_wp = dialog.select_wp.current()
        wp_cur = workpackages[ix_wp]
        wd_cur = wp_cur.workdays[ix]
        wp_cur.cur_workday = wd_cur
        self.fill_times(wd_cur)
        dialog.wd_date.set(str(wd_cur.date))


class MainMenu(tk.Menu):
    def __init__(self, parent, dlg):
        super().__init__(parent)
        self.dialog = dlg
        self.sub_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label='Datei', menu=self.sub_menu)
        self.sub_menu.add_command(label='Neu', command=new_file)
        self.sub_menu.add_command(label='Öffnen', command=load_wpckgs)
        self.sub_menu.add_command(label='Speichern', command=save_wpckgs)
        self.sub_menu.add_command(label='Speichern unter...', command=save_wpckgs_as)

        self.sub_menu_edit = tk.Menu(self, tearoff=False)
        self.add_cascade(label='Ändern', menu=self.sub_menu_edit)
        self.sub_menu_edit.add_command(label='Korrigieren', command=self.correction)

        self.sub_menu_rep = tk.Menu(self, tearoff=False)
        self.add_cascade(label='Bericht', menu=self.sub_menu_rep)
        self.sub_menu_rep.add_command(label='Zeitnachweis', command=self.show_report)
        self.sub_menu_rep.add_command(label='Arbeitspaket', command=self.show_workpackage)
        self.sub_menu_rep.add_command(label='Arbeitstag', command=self.show_workday)
        self.sub_menu_rep.add_command(label="Gleitzeitsaldo", command=self.show_balance)

    @staticmethod
    def show_report():
        report = report_work_summary("Otto Normalverbraucher", workpackages)
        display_report(report)

    def show_workpackage(self):
        wp_name = self.dialog.wp_name.get()
        report = report_workpackage_summary(wp_name, workpackages)
        display_report(report)

    def show_workday(self):
        date = self.dialog.wd_date.get()
        report = report_workday_summary(date, workpackages)
        display_report(report)

    def show_balance(self):
        timespan = input_timespan()
        report = report_work_summary_timespan("Uwe Pabst", workpackages, timespan[0], timespan[1])
        display_report(report)

    @staticmethod
    def correction():
        CorrectionDialog(root, workpackages)


def new_file():
    global workpackages
    dialog.select_wp.delete(0, tk.END)
    dialog.wd_date.set("")
    dialog.begin_time.set("")
    dialog.end_time.set("")
    overview.listbox_wd.delete(0, tk.END)
    overview.list_times['text'] = ""
    workpackages = []
    root.title("Zeitnachweis")


def load_wpckgs():
    global workpackages, filename
    filename = filedialog.askopenfilename(initialdir='./Dateien', filetypes=[("XML", "*.xml")])
    file = open(filename, 'r', encoding='utf-8')
    wp_name_list = []
    workpackages = read_workpackages(file)
    file.close()
    root.title("Zeitnachweis - " + os.path.basename(filename))
    for wp in workpackages:
        wp_name_list.append(wp.wp_name)
    dialog.add_wp_names(wp_name_list)


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
    root.title("Zeitnachweis - " + os.path.basename(filename))


def input_time():
    time_str = dt.datetime.now().strftime("%H:%M:%S")
    return time_str


workpackages = []
filename = ""

root = tk.Tk()
root.title("Zeitnachweis")


dialog = DispWorkpackages(root)
overview = DisplayWorkdays(root)

menu_bar = MainMenu(root, dialog)
root['menu'] = menu_bar

root.mainloop()
