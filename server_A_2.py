import socket

# Define the blood banks for blood group A at each location
blood_banks = {
    'New York': '4',
    'Chicago': '5',
    'Los Angeles': '6'
}

# Create a server socket and listen for connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 9002))
server_socket.listen(1)
print('Server started and listening for connections...')

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print('Accepted connection from {}:{}'.format(*client_address))

    # Receive the location from the layer 1 server
    location = client_socket.recv(1024).decode()
    print('Received location from layer 1 server:', location)

    # Get the blood bank number based on the location and send it to the layer 1 server
    if location in blood_banks:
        blood_bank = blood_banks[location]
    else:
        blood_bank = 'N/A'
    client_socket.sendall(blood_bank.encode())
    print('Sent blood bank number to layer 1 server:', blood_bank)

    # Close the client socket
    client_socket.close()
