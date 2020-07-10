import tkinter as tk
from tkinter.simpledialog import *


class LoginDialog(Dialog):
    def __init__(self, parent, title=None):
        self.label_chatname = None
        self.chatname = None
        self.entry_chatname = None
        self.chat_name = None
        super().__init__(parent, title)

    def body(self, parent):
        self.label_chatname = tk.Label(parent, text="Chat Name")
        self.label_chatname.pack(anchor='nw')

        self.chatname = tk.StringVar()
        self.entry_chatname = tk.Entry(parent, width=20, textvariable=self.chatname)
        self.entry_chatname.pack()

        return self.entry_chatname

    def apply(self):
        self.chat_name = self.chatname.get()
        self.result = 1


def input_chatname():
    global root

    input_dialog = LoginDialog(root, title="Chat Name eingeben")

    if input_dialog.result is not None:
        chat_name = input_dialog.chat_name
        return chat_name
    else:
        return "Agent007"

def show_dialog():
    global root
    chatname = input_chatname()
    print(chatname)

if '__main__' == __name__:
    root = tk.Tk()
    button = tk.Button(root, text="Show Dialog", command=show_dialog)
    button.pack()
    root.mainloop()
