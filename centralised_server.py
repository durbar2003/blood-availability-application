import socket

# Create a mapping of blood groups to layer 1 servers
blood_group_servers = {
    'A': ['localhost', 8001],
    'B': ['localhost', 8002],
    'O': ['localhost', 8003],
    'AB': ['localhost', 8004]
}

# Create a mapping of locations to layer 2 servers
location_servers = {
    'New York': ['localhost', 9001, 9011, 9021],
    'Chicago': ['localhost', 9002, 9012, 9022],
    'Los Angeles': ['localhost', 9021, 9022, 9023, 9024]
}

# Create a server socket and listen for connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 7000))
server_socket.listen(1)
print('Central server started and listening for connections...')

while True:
    # Accept a client connection
    client_socket, client_address = server_socket.accept()
    print('Accepted connection from {}:{}'.format(*client_address))

    # Receive the blood group and location from the client
    blood_group = client_socket.recv(1024).decode()
    location = client_socket.recv(1024).decode()
    print('Received blood group and location from client:', blood_group, location)

    # Check if the location is valid
    if location not in location_servers:
        client_socket.sendall('We do not have any blood bank available at that location.'.encode())
        print('Sent response to client: We do not have any blood bank available at that location.')
        client_socket.close()
        continue

    # Connect to the layer 1 server for the given blood group
    layer1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    layer1_server = blood_group_servers[blood_group]
    layer1_socket.connect((layer1_server[0], layer1_server[1]))

    # Send the location to the layer 1 server and receive the blood bank number from the layer 2 servers
    blood_banks = []
    for server_port in location_servers[location]:
        layer2_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        layer2_socket.connect((layer1_server[0], server_port))
        layer2_socket.sendall(location.encode())
        blood_bank = layer2_socket.recv(1024).decode()
        blood_banks.append(blood_bank)
        layer2_socket.close()

    # Send the blood bank numbers to the client
    response = 'Blood banks for blood group {} at location {}:\n{}\n{}\n{}'.format(
        blood_group, location, *blood_banks)
    client_socket.sendall(response.encode())
    print('Sent response to client:', response)

    # Close the sockets
    layer1_socket.close()
    client_socket.close()
