import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Password import Password


class Home(tk.Tk):
    def __init__(self, title=None):
        super().__init__()
        if title:
            self.title(title)
        else:
            self.title("Password Manager")
        self.validate = False
        self.frames = {ttk.Frame: ttk.Frame(self)}
        self.__password = tk.StringVar()
        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1), weight=1)
        self.label = ttk.Label(self, text="Hello Mr.Sivakesh")
        self.entry = ttk.Entry(self, textvariable=self.__password, show="*")
        self.submit = ttk.Button(self, text="Submit", command=self.__verify_password)
        self.create_button = ttk.Button(self, text="Create Password", state="disabled")
        self.show_passwords = ttk.Button(self, text="Show Passwords", state="disabled")


    def __verify_password(self):
        self.validate = Password.validate_master_password(self.entry.get())
        if self.validate:
            self.entry.grid_remove()
            self.submit.grid_remove()
            self.create_button["state"] = "normal"
            self.show_passwords["state"] = "normal"
        else:
            messagebox.showerror(title="Wrong Password", message="Invalid credential", icon="error")

    def __setup_widgets(self):
        self.label.grid(row=0, column=0, columnspan=2, pady=10, sticky="", ipady=40)
        self.entry.grid(row=1, column=0, pady=10)
        self.submit.grid(row=1, column=1, pady=10)
        self.create_button.grid(row=2, column=0, padx=10, pady=5, ipadx=50, ipady=20)
        self.show_passwords.grid(row=2, column=1, padx=10, pady=5, ipadx=50, ipady=20)


home = Home()
home.mainloop()
