from tkinter import *
from tkinter import ttk, Toplevel
from showpassword import Show
from createpassword import Create
from Password import Password

try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


def switch_command():
    if frame_switch.get():
        frame1.tkraise()
        frame_switch.set(False)

    else:
        frame2.tkraise()
        frame_switch.set(True)


def launch():
    global password_change_window
    password_change_window = Toplevel(w)
    password_change_window.title("Change Master Password")
    change_master_password = Label(password_change_window, text="Passphrase:")
    change_master_password.grid(row=0, column=0, padx=10, pady=10)
    master_password = Entry(password_change_window)
    master_password.grid(row=0, column=1, padx=10, pady=10)
    ok_button = ttk.Button(password_change_window, text="Change",
                           command=lambda: Password.change_pass_key(master_password.get()))
    ok_button.grid(row=1, column=0, pady=10, padx=10)
    cancel_button = ttk.Button(password_change_window, text="cancel", command=pressed_cancel)
    cancel_button.grid(row=1, column=1, pady=10, padx=10)


def pressed_ok(passphrase: str):
    Password.change_pass_key(passphrase)
    print("New Master Password: ", passphrase)
    password_change_window.destroy()


def pressed_cancel():
    password_change_window.destroy()


w = Tk()
w.rowconfigure(0, weight=1)
w.columnconfigure(0, weight=1)
frame2 = Create(w)
frame2.grid(row=0, column=0, sticky="nswe")
frame1 = Show(w)
frame1.grid(row=0, column=0, sticky="nswe")
switch_button = ttk.Button(w, text="Switch_Window", command=switch_command, width=20)
frame2.tkraise()
frame_switch = BooleanVar(value=True)
switch_button.grid(row=1, column=0, padx=20, pady=10)
change_password_button = ttk.Button(w, text="Change Password", command=launch)
change_password_button.grid(pady=10)
w.mainloop()
