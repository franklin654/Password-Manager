import os
import re
import tkinter
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from Password import Password
import pyperclip


class Show(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.__last_password = None
        self.columnconfigure((0, 1), weight=1)
        self.search_item = tk.StringVar(value="")
        self.search = ttk.Entry(self, textvariable=self.search_item, width=40)
        self.search.grid(row=0, column=0, sticky="ew", padx=10, pady=10, columnspan=2)
        self.search_item.trace_add("write", self.set_choices)
        self.__choices = [re.sub(r".json", "", i) for i in os.listdir("passwords")]
        self.choices_var = tk.StringVar(value=self.__choices)
        self.Lbox = tk.Listbox(self, listvariable=self.choices_var, width=20, height=len(self.__choices))
        self.Lbox.grid(row=1, column=0, padx=10, pady=20, sticky="we")
        self.view_button = ttk.Button(self, text="View", command=self.__get_password)
        self.view_button.grid(row=1, column=1, padx=10, sticky="e")
        self.trial = tk.Text(self, height=1)
        self.set_choices()
        self.copy_button = ttk.Button(self, text="Copy", command=self.__copy_password)
        self.copy_button.grid(row=2, column=1, padx=10, sticky="e")

    def set_choices(self):
        files = [re.sub(r".json", "", i) for i in os.listdir("passwords")]
        pattern = self.search_item.get()
        self.__choices = [x for x in files if re.match(pattern, x)]
        self.choices_var.set(self.__choices)
        self.Lbox["height"] = len(self.__choices)

    def __get_password(self):
        try:
            self.trial.delete(index1="1.0", index2=tk.END)
        except tkinter.TclError:
            pass
        idx = self.Lbox.curselection()
        if len(idx) == 0:
            messagebox.showerror(title="web site", message="No website selected please select a message from the list "
                                                           "below or use the search", icon="error")
        else:
            web_site_name = self.__choices[int(idx[0])]
            p = Password(web_site=web_site_name)
            user_name, password = p.read_password()
            self.__last_password = password
            self.trial.insert(tk.END, "username: " + user_name + " password: " + password)
            self.trial.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

    def __copy_password(self):
        idx = self.Lbox.curselection()
        if len(idx) == 0:
            if self.__last_password is None:
                messagebox.showerror(title="web site", message="No website selected please select a message from "
                                                               "the list below or use the search", icon="error")
            else:
                pyperclip.copy(self.__last_password)
                messagebox.showinfo(title="password_copied", message=f"you copied \"{self.__last_password}\"",
                                    icon='info')
        else:
            web_site_name = self.__choices[int(idx[0])]
            p = Password(web_site=web_site_name)
            _, password = p.read_password()
            pyperclip.copy(password)
            messagebox.showinfo(title="password_copied", message=f"you copied \"{password}\"",
                                icon='info')
