import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, simpledialog, messagebox

HOST = '127.0.0.1'
PORT = 12345

class ChatClient:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Python Chat")
        self.window.geometry("360x640")

        self.chat_display = scrolledtext.ScrolledText(self.window, state='disabled', wrap=tk.WORD)
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.entry_message = tk.Entry(self.window, font=("Arial", 10))
        self.entry_message.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)
        self.entry_message.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.window, text="Send", bg="#27ae60", fg="white", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT, padx=(0, 10), pady=10)

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.username = simpledialog.askstring("Username", "Enter your username:")
        if not self.username:
            messagebox.showerror("Username required", "You must enter a username.")
            self.window.destroy()
            return

        try:
            self.client_socket.connect((HOST, PORT))
            self.client_socket.send(self.username.encode())
            threading.Thread(target=self.receive_messages, daemon=True).start()
        except Exception as e:
            messagebox.showerror("Connection error", str(e))
            self.window.destroy()

        self.window.mainloop()

    def send_message(self, event=None):
        message = self.entry_message.get()
        if message:
            try:
                self.client_socket.send(message.encode())
                self.entry_message.delete(0, tk.END)
            except:
                messagebox.showerror("Error", "Unable to send message.")
                self.window.destroy()

    def receive_messages(self):
        while True:
            try:
                message = self.client_socket.recv(1024).decode()
                self.chat_display.config(state='normal')
                self.chat_display.insert(tk.END, message + "\n")
                self.chat_display.config(state='disabled')
                self.chat_display.yview(tk.END)
            except:
                break

if __name__ == "__main__":
    ChatClient()
