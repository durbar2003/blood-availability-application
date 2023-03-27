import socket

# Define the layer 2 servers for blood group A
locations = {
    'New York': '1',
    'Chicago': '2',
    'Los Angeles': '3'
}

# Connect to the layer 1 server for blood group A
layer1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
layer1_socket.bind(('localhost', 9001))
layer1_socket.listen(1)
print('Server started and listening for connections...')

while True:
    # Accept a client connection
    client_socket, client_address = layer1_socket.accept()
    print('Accepted connection from {}:{}'.format(*client_address))

    # Receive the location from the layer 1 server
    location = client_socket.recv(1024).decode()
    print('Received location from layer 1 server:', location)

    # Get the blood bank number based on the location and send it to the layer 1 server
    if location in locations:
        blood_bank = locations[location]
    else:
        blood_bank = 'N/A'
    client_socket.sendall(blood_bank.encode())
    print('Sent blood bank number to layer 1 server:', blood_bank)

    # Close the client socket
    client_socket.close()
