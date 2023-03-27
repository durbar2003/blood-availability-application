import socket

# Define the central server address and port
HOST = '127.0.0.1'
PORT = 5021

# Prompt the user for the blood group and location
blood_group = input('Enter blood group: ')
location = input('Enter location: ')

# Create a TCP/IP socket for the client
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # Connect to the central server
    client_socket.connect((HOST, PORT))
    
    # Send the blood group and location to the central server
    request = f'{blood_group},{location}'
    client_socket.sendall(request.encode())
    
    # Receive the response from the central server
    response = client_socket.recv(1024).decode()
    print(f'Response: {response}')
