import socket

# Define the layer 2 servers for blood group A
locations = {
    'New York': '25',
    'Chicago': '26',
    'Los Angeles': '27'
}

# Connect to the layer 1 server for blood group A
layer1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
layer1_socket.connect(('localhost', 8003))

# Receive the location from the layer 1 server
location = layer1_socket.recv(1024).decode()
print('Received location from layer 1 server:', location)

# Get the blood bank number based on the location and send it to the layer 1 server
if location in locations:
    blood_bank = locations[location]
else:
    blood_bank = 'N/A'
layer1_socket.sendall(blood_bank.encode())
print('Sent blood bank number to layer 1 server:', blood_bank)

# Close the layer 1 socket
layer1_socket.close()
