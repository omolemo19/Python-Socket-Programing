Overview
The application includes a server and multiple clients:

Server: Facilitates client authentication and provides a list of available peers.
Clients: Authenticate with the server, establish peer-to-peer communication, and exchange messages.

Features

Server
Authentication using a predefined password.
Manages active client connections with multithreading.
Provides a list of active peers on request.

Client
Base Functionality:
Authenticate with the server using a username and password.
Request a list of available peers from the server.
Send messages to other clients via UDP.
Additional Features:
Timestamps on messages.
Ability to send a message to multiple clients simultaneously.
Graceful exit using a "quit" command.

Technologies Used
Python 3: Core programming language.
Sockets: TCP for authentication and signaling, UDP for real-time messaging.
Multithreading: For handling multiple client connections simultaneously.

How It Works
Server:

Listens for incoming connections.
Authenticates clients and maintains a list of active peers.
Handles client requests (e.g., peer listing) in separate threads.
Client:

Connects to the server and authenticates.
After authentication:
Sends requests to list available peers.
Initiates UDP connections for direct messaging with other clients.
Includes added features like timestamps and multi-client messaging.
