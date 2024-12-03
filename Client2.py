# Created by
# Omolemo Modise
# Client 2



import socket
import threading
import datetime

# TCP Configuration
tcp_host = "127.0.0.1"
tcp_port = 12345

# Establish TCP connection
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.connect((tcp_host, tcp_port))

# Authenticate user
authenticated = False
while not authenticated:
    username = input("Enter your username: ")
    password = input("Enter your password: ")


    # Send credentials to the server for authentication
    tcp_socket.send(password.encode())

    # Receive response from the server
    response = tcp_socket.recv(1024).decode()
    if response == "OK":
        authenticated = True
        print("Authentication successful!")
    else:
        print("Incorrect username or password. Please try again.")

# Receive client's IP address and port number from the server
client_ip_port = tcp_socket.recv(1024).decode()
client_ip, client_port = client_ip_port.split(':')

# Create a UDP socket with the received IP address and port number
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_socket.bind((client_ip, int(client_port)))

# Function to receive UDP messages
def receive_messages(sock):
    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes


        # Lookup username by IP address
        sender_username = None
        for username, address in available_clients.items():
            if address == addr:
                sender_username = username
                break

        # Get the current timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        if sender_username:
            print(f"\n[{timestamp}]Received message from {sender_username}: {data.decode()}")
        else:
            print(f"\n[{timestamp}]Received message from {addr}: {data.decode()}")

# Start a thread for receiving UDP messages
receive_thread = threading.Thread(target=receive_messages, args=(udp_socket,))
receive_thread.daemon = True
receive_thread.start()


# Main loop for sending messages
while True:
    LIST = input("LIST AVAILABLE CLIENTS: Y/N \n")
    if LIST == "Y":
        tcp_socket.send(b"LIST")
        available_clients_str = tcp_socket.recv(1024).decode()
        available_clients = eval(available_clients_str)
        print(f"Available clients are: {available_clients}")

    recipient_user = input("Enter recipient's username: ")
    message = input("Enter message to send: ")


    # Determine recipient's IP address and port from available_clients
    recipient_info = available_clients.get(recipient_user)
    if recipient_info:
        recipient_ip, recipient_port = recipient_info
        recipient_address = (recipient_ip.strip(), int(recipient_port))
        udp_socket.sendto(message.encode(), recipient_address)
    else:
        print("Recipient not found.")



