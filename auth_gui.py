# auth_gui.py
import tkinter as tk
from tkinter import messagebox
from db import create_table, register_user, login_user

create_table()

def register():
    username = entry_username.get()
    password = entry_password.get()
    email = entry_email.get()

    if register_user(username, password, email):
        messagebox.showinfo("Success", "Registration successful!")
    else:
        messagebox.showerror("Error", "Username already exists!")

def login():
    username = entry_username.get()
    password = entry_password.get()

    if login_user(username, password):
        messagebox.showinfo("Success", f"Welcome {username}!")
    else:
        messagebox.showerror("Error", "Invalid credentials!")

app = tk.Tk()
app.title("WhatsApp Clone - Login/Register")
app.geometry("300x300")

tk.Label(app, text="Username").pack()
entry_username = tk.Entry(app)
entry_username.pack()

tk.Label(app, text="Password").pack()
entry_password = tk.Entry(app, show="*")
entry_password.pack()

tk.Label(app, text="Email (for Signup)").pack()
entry_email = tk.Entry(app)
entry_email.pack()

tk.Button(app, text="Login", command=login).pack(pady=5)
tk.Button(app, text="Sign Up", command=register).pack(pady=5)

app.mainloop()
