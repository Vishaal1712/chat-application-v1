import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = {}  # {client_socket: username}


def broadcast(message, sender_socket=None):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                remove_client(client)


def send_private_message(target_username, message, sender_socket):
    found = False
    for client, username in clients.items():
        if username == target_username:
            try:
                client.send(f"[DM from {clients[sender_socket]}] {message}".encode())
                sender_socket.send(f"[DM to {target_username}] {message}".encode())
                found = True
            except:
                remove_client(client)
            break
    if not found:
        sender_socket.send(f"[Server] User '{target_username}' not found.".encode())


def handle_client(client_socket):
    try:
        # Step 1: Get the username first
        username = client_socket.recv(1024).decode().strip()
        clients[client_socket] = username
        print(f"Username of client is {username}")
        broadcast(f"{username} joined the chat!", sender_socket=client_socket)

        # Step 2: Start receiving messages
        while True:
            msg = client_socket.recv(1024).decode()
            if msg.startswith('@'):
                try:
                    target_username, private_msg = msg[1:].split(' ', 1)
                    send_private_message(target_username, private_msg, client_socket)
                except ValueError:
                    client_socket.send("[Server] Invalid DM format. Use @username message".encode())
            else:
                broadcast(f"{username}: {msg}", sender_socket=client_socket)

    except:
        remove_client(client_socket)


def remove_client(client_socket):
    if client_socket in clients:
        username = clients[client_socket]
        print(f"{username} disconnected")
        broadcast(f"{username} has left the chat.")
        del clients[client_socket]
        client_socket.close()


def start_server():
    print(f"Server started on {HOST}:{PORT}")
    while True:
        client_socket, _ = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()


start_server()
