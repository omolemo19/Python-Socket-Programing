# Created by
# Omolemo Modise
# Baye-Saliou Fall
# Mziwokholo Tshem

import socket
import threading

host = "127.0.0.1"
port = 12345
client_addresses = {}  # Dictionary to store client addresses and their labels
user_count = 1  # Counter for labeling users

# Function to authenticate user via password
def authenticate(default_password):
    # Check if the default password matches the expected password
    if default_password == "CSC3@A1":
        return True
    else:
        return False

# Create a TCP socket and bind it to the specified host and port
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.bind((host, port))
tcp_socket.listen()

print(f"Server listening on {host}:{port}")

# Function to handle client connections
def handle_client(client_socket, client_address):
    global client_addresses, user_count
    # Label for the client
    client_label = f"USER {user_count}"
    user_count += 1

    authenticated = False  # Flag to track client authentication status
    while not authenticated:
        # Receive the default password sent by the client for authentication
        default_password = client_socket.recv(1024).decode()
        # Authenticate the client based on the received password
        if authenticate(default_password):
            authenticated = True
            # Store client's label and address in the dictionary
            client_addresses[client_label] = client_address
            # Send "OK" message to the client indicating successful authentication
            client_socket.send(b"OK")
            # Send client's IP and port to the client for UDP communication
            client_socket.send(f"{client_address[0]}:{client_address[1]}".encode())
            print(f"Authentication successful for {client_address}")
        else:
            authenticated = False
            # Send "FAIL" message to the client indicating authentication failure
            client_socket.send(b"FAIL")
            print(f"Authentication failed for {client_address}")

    # Main loop for handling client messages
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(f"Received: {data.decode('utf-8')}")

        # Send the list of available clients to the client upon request
        if data.decode('utf-8') == 'LIST':
            client_socket.send(str(client_addresses).encode())
        else:
            # Send acknowledgment message back to the client
            client_socket.send(b"Message received!")

    # Close the client socket connection
    client_socket.close()

# Main loop to accept incoming client connections
while True:
    # Accept a new client connection
    client_socket, client_address = tcp_socket.accept()
    print(f"Accepted connection from {client_address}")

    # Create a new thread to handle the client connection
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()





