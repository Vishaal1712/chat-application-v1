import tkinter as tk
import client_gui  # Make sure this file exists

def login():
    username = entry_username.get().strip()
    if not username:
        return
    window.destroy()
    client_gui.start_chat(username)

# GUI setup
window = tk.Tk()
window.title("Login")
window.geometry("300x150")

tk.Label(window, text="Enter Username:").pack(pady=10)
entry_username = tk.Entry(window)
entry_username.pack()

tk.Button(window, text="Start Chat", command=login).pack(pady=10)

window.mainloop()
