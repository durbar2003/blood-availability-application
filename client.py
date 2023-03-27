import socket

# Prompt the user for the blood group and location
blood_group = input('Enter the blood group (A, B, O, or AB): ')
location = input('Enter the location (New York, Chicago, Los Angeles): ')

# Connect to the appropriate layer 1 server based on the blood group
if blood_group == 'A':
    server_address = ('localhost', 8001)
elif blood_group == 'B':
    server_address = ('localhost', 8002)
elif blood_group == 'O':
    server_address = ('localhost', 8003)
elif blood_group == 'AB':
    server_address = ('localhost', 8004)
else:
    print('Invalid blood group')
    exit()

# Connect to the layer 1 server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

# Send the location to the layer 1 server
client_socket.sendall(location.encode())

# Receive the blood bank number from the layer 2 servers and print the result
blood_bank1 = client_socket.recv(1024).decode()
blood_bank2 = client_socket.recv(1024).decode()
blood_bank3 = client_socket.recv(1024).decode()
print('Blood bank numbers for {} in {}: {}, {}, {}'.format(blood_group, location, blood_bank1, blood_bank2, blood_bank3))

# Close the client socket
client_socket.close()
