import socket

# Define the layer 2 servers for blood group A
locations = {
    'New York': ('localhost', 9001),
    'Chicago': ('localhost', 9011),
    'Los Angeles': ('localhost', 9021)
}

# Create a server socket and listen for connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8001))
server_socket.listen(1)
print('Server started and listening for connections...')

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print('Accepted connection from {}:{}'.format(*client_address))

    # Receive the blood group from the client
    blood_group = client_socket.recv(1024).decode()
    print('Received blood group from client:', blood_group)

    # Connect to the corresponding layer 2 server based on the location
    location = client_socket.recv(1024).decode()
    print('Received location from client:', location)
    if location in locations:
        server_address = locations[location]
        layer2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        layer2_socket.connect(server_address)
        print('Connected to layer 2 server at {}:{}'.format(*server_address))

        # Send the blood group to the layer 2 server and receive the blood bank number
        layer2_socket.sendall(blood_group.encode())
        blood_bank = layer2_socket.recv(1024).decode()
        print('Received blood bank number from layer 2 server:', blood_bank)

        # Send the blood bank number to the client
        client_socket.sendall(blood_bank.encode())
        print('Sent blood bank number to client:', blood_bank)

        # Close the layer 2 socket
        layer2_socket.close()

    else:
        error_message = 'No blood bank available at {}.'.format(location)
        client_socket.sendall(error_message.encode())
        print(error_message)

    # Close the client socket
    client_socket.close()
