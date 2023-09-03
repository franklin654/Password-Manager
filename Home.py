import tkinter as tk
from tkinter import ttk


class Home(tk.Tk):
    def __init__(self, title=None):
        super().__init__()
        if title:
            self.title(title)
        else:
            self.title("Password Manager")
        self.frames = {ttk.Frame: ttk.Frame(self)}
        self.rowconfigure((0, 1), weight=1)
        # self.grid_rowconfigure(1, weight=1)
        self.columnconfigure((0, 1), weight=1)
        # self.columnconfigure(1, weight=1)
        label = ttk.Label(self, text="Hello Mr.Sivakesh")
        label.grid(row=0, column=0, columnspan=2, pady=10, sticky="", ipady=40)
        create_button = ttk.Button(self, text="Create Password")
        create_button.grid(row=1, column=0, padx=10, pady=5, ipadx=50, ipady=20)
        show_passwords = ttk.Button(self, text="Show Passwords")
        show_passwords.grid(row=1, column=1, padx=10, pady=5, ipadx=50, ipady=20)