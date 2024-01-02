from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from Password import Password
import pyperclip


class Create(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.rowconfigure((0, 1, 2, 3), weight=1)
        self.columnconfigure((0, 1, 2, 3), weight=1)
        self.__web_site_name = tk.StringVar(value="")
        self.__user_name = tk.StringVar(value="")
        self.pass_word_strength = tk.StringVar(value="v")
        self.__password_length = tk.IntVar(value=8)
        self.__num = tk.BooleanVar(value=False)
        self.__last_password = tk.StringVar(value=None)
        label1 = ttk.Label(self, text="Web site Name:", font=('Calibri', 15, 'bold'))
        label1.grid(row=0, column=0, ipadx=10, ipady=20, padx=10)
        self.Entry1 = ttk.Entry(self, textvariable=self.__web_site_name)
        self.Entry1.grid(row=0, column=1, padx=(0, 10), ipady=15, ipadx=10, sticky="w")
        label2 = ttk.Label(self, text="User Name:", font=('Calibri', 15))
        label2.grid(row=1, column=0, ipadx=10, ipady=20, padx=10)
        self.Entry2 = ttk.Entry(self, textvariable=self.__user_name)
        self.Entry2.grid(row=1, column=1, padx=(0, 10), ipady=15, ipadx=10, sticky="w")
        label3 = ttk.Label(self, text="Password Length:", font=('Calibri', 15))
        label3.grid(row=2, column=0, padx=10)
        self.length_box = ttk.Spinbox(self, textvariable=self.__password_length, from_=8, to=32, increment=1, wrap=True)
        self.length_box.grid(row=2, column=1, padx=10, pady=20, sticky="w")
        box1 = ttk.Radiobutton(self, variable=self.pass_word_strength, value="s", text="strong password")
        box1.grid(row=3, column=0, ipady=10, ipadx=10, padx=10, pady=5)
        box2 = ttk.Radiobutton(self, variable=self.pass_word_strength, value="v", text="very strong password")
        box2.grid(row=3, column=1, ipady=10, ipadx=10, padx=10, pady=5)
        self.num_check_box = ttk.Checkbutton(self, text="Numbers", variable=self.__num, onvalue=True, offvalue=False)
        self.num_check_box.grid(row=4, column=0, columnspan=2, pady=10)
        self.submit_button = ttk.Button(self, text="Submit", command=self.__create_and_print)
        self.submit_button.grid(row=5, column=0, pady=10)
        self.Entry1.focus()
        self.password_label = ttk.Label(self, text="", anchor="center")
        self.trial = tk.Label(self, height=1, width=32, textvariable=self.__last_password, background="white")
        self.copy_button = ttk.Button(self, text="Copy", command=self.__copy_password)
        self.copy_button.grid(row=5, column=1, padx=10, pady=10)

    def __create_and_print(self):
        if self.__web_site_name.get() == "" or self.__user_name.get() == "":
            messagebox.showerror(title="insufficient details", message="Please Enter WebSite and Username",
                                 icon="error")
        else:
            try:
                self.__last_password.set("")
            except tk.TclError:
                pass
            p = Password(web_site=self.__web_site_name.get(), user_name=self.__user_name.get(), num=self.__num.get(),
                         password_strength=self.pass_word_strength.get())
            self.Entry1.delete(0, "end")
            self.Entry2.delete(0, "end")
            password = p.generate_password(self.__password_length.get())
            self.__last_password.set(password)
            self.trial.grid(row=6, column=0, columnspan=2, pady=10)

    def __copy_password(self):
        if self.__last_password is None:
            messagebox.showerror(title="No Password",
                                 message="Please generate Password or use the view password option",
                                 icon="error")
        else:
            pyperclip.copy(self.__last_password.get())

    def clear_password(self):
        if self.__last_password is not None:
            self.__last_password.set("")
            self.trial.grid_remove()
