import socket

# Define the layer 2 servers for blood group B
locations = {
    'New York': '4',
    'Chicago': '5',
    'Los Angeles': '6'
}

# Create a server socket and listen for connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 8002))
server_socket.listen(1)
print('Server started and listening for connections...')

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print('Accepted connection from {}:{}'.format(*client_address))

    # Receive the location from the client
    location = client_socket.recv(1024).decode()
    print('Received location from client:', location)

    # Get the blood bank number based on the location and send it to the client
    if location in locations:
        blood_bank = locations[location]
    else:
        blood_bank="N/A"
    client_socket.sendall(blood_bank.encode())
    print('Sent blood bank number to client:', blood_bank)
    client_socket.close()
