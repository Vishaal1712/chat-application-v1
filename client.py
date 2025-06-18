import socket
import threading

# Server connection details
HOST = '127.0.0.1'  # Same as in server.py
PORT = 12345

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            print("An error occurred. Connection closed.")
            client_socket.close()
            break

def send_messages(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode())

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Wait for server to ask for username
    username_prompt = client.recv(1024).decode()
    if username_prompt == "USERNAME":
        username = input("Enter your username: ")
        client.send(username.encode())

    # Start threads for receiving and sending
    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    send_thread = threading.Thread(target=send_messages, args=(client,))
    send_thread.start()

if __name__ == "__main__":
    start_client()
