# Created by
# Baye-Saliou Fall

import socket
import threading

# TCP Configuration
tcp_host = "10.130.36.16"
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

        if sender_username:
            print(f"\nReceived message from {sender_username}: {data.decode()}")
        else:
            print(f"\nReceived message from {addr}: {data.decode()}")

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
        availClients = available_clients_str.split(",")
        available_clients = eval(available_clients_str)
        print(f"Available clients are: {available_clients}")

        # feature for communicating with two clients below
        # ask number of recepients
        recNum = int(input("Enter number of recepients: "))

        if recNum == 1: # sends to one user
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

        else: # sends a message to two users
            rec_one = input("Enter recipient one's username: ")
            rec_two = input("Enter recipient two's username: ")
            message = input("Enter message to send: ")

            recipient_one_info = available_clients.get(rec_one)
            recipient_two_info = available_clients.get(rec_two)

            if recipient_one_info and recipient_two_info:
                rec_one_IP, rec_one_Port = recipient_one_info
                rec_two_IP, rec_two_Port = recipient_two_info

                rec_one_address = (rec_one_IP.strip(), int(rec_one_Port))
                rec_two_address = (rec_two_IP.strip(), int(rec_two_Port))

                udp_socket.sendto(message.encode(), rec_one_address)
                udp_socket.sendto(message.encode(), rec_two_address)
            else:
                print("Recipients not found.")
