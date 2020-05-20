from tkinter import *
from tkinter import filedialog
from BerichtAnzeigen import input_timespan


class MyFrame(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(borderwidth=3, relief='raise')
        self.button = Button(self, text="aabb", command=self.on_click)
        self.button.grid()

    @staticmethod
    def on_click():
        print("Button clicked")
        print("Das ist ein Beispiel für Branching")
        print("Hier wurde ein Fehler eingebaut")


def load_wpckgs():
    filename = filedialog.askopenfilename(initialdir='./Zeiterfassung/Dateien')
    print(filename)


def print_timespan():
    timespan = input_timespan()
    print("Date from {0} until {1}".format(timespan[0], timespan[1]))
    print("Erster Teil des neuen Features")
    print("Rest des Features")


root = Tk()
root.title("Playground")
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

menu_bar = Menu(root)
root['menu'] = menu_bar
sub_menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label='Datei', menu=sub_menu)
sub_menu.add_command(label='Öffnen', command=load_wpckgs)
sub_menu.add_command(label="Zeitraum", command=print_timespan)

frame1 = MyFrame(root)
frame1.grid(row=0, column=0, padx=5, ipady=0)

frame2 = MyFrame(root)
frame2.grid(row=1, column=1, padx=6, ipady=0)

frame3 = MyFrame(root)
frame3.grid(row=0, column=2, padx=7, ipady=0)

frame4 = MyFrame(root)
frame4.grid(row=1, column=0, padx=8, ipady=0)

frame5 = MyFrame(root)
frame5.grid(row=0, column=1, padx=9, ipady=0)

frame6 = MyFrame(root)
frame6.grid(row=1, column=2, padx=10, ipady=0)

root.mainloop()
