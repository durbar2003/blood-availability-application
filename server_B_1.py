import socket

# Define the blood bank numbers for the given location
blood_banks = {
    'New York': 'Blood Bank 6',
    'Chicago': 'Blood Bank 7',
    'Los Angeles': 'Blood Bank 8'
}

# Create a server socket and listen for connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 9011))
server_socket.listen(1)
print('Server B_1 started and listening for connections...')

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print('Accepted connection from {}:{}'.format(*client_address))

    # Receive the location from the layer 1 server
    location = client_socket.recv(1024).decode()
    print('Received location from layer 1 server:', location)

    # Send the blood bank number for the given location to the layer 1 server
    if location in blood_banks:
        response = blood_banks[location]
    else:
        response = 'No blood bank available for the given location.'
    client_socket.sendall(response.encode())
    print('Sent response to layer 1 server:', response)

    # Close the socket
    client_socket.close()
