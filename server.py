import socket

# Define the central server address and port
HOST = '127.0.0.1'
PORT = 5021

# Create a TCP/IP socket for the central server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Bind the socket to the central server address and port
    server_socket.bind((HOST, PORT))
    
    # Listen for incoming connections
    server_socket.listen()
    
    print(f'Central server running on {HOST}:{PORT}')
    
    while True:
        # Wait for a client connection
        client_socket, client_address = server_socket.accept()
        print(f'New client connection from {client_address}')
        
        # Receive the client request
        request = client_socket.recv(1024).decode()
        print(f'Received request: {request}')
        
        # Extract the blood group and location from the client request
        blood_group, location = request.split(',')
        
        # Forward the request to the layer 1 servers for this blood group
        layer1_servers = [('127.0.0.1', 5001), ('127.0.0.1', 5002), ('127.0.0.1', 5003)]
        responses = []
        for layer1_server in layer1_servers:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as layer1_socket:
                layer1_socket.connect(layer1_server)
                layer1_socket.sendall(request.encode())
                response = layer1_socket.recv(1024).decode()
                responses.append(response)
        
        # Concatenate the responses from the layer 1 servers
        layer1_response = '\n'.join(responses)
        
        # Forward the layer 1 response to the layer 2 servers for this location
        layer2_servers = [('127.0.0.1', 5011), ('127.0.0.1', 5012), ('127.0.0.1', 5013)]
        responses = []
        for layer2_server in layer2_servers:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as layer2_socket:
                layer2_socket.connect(layer2_server)
                layer2_socket.sendall(layer1_response.encode())
                response = layer2_socket.recv(1024).decode()
                responses.append(response)
        
        # Concatenate the responses from the layer 2 servers
        layer2_response = '\n'.join(responses)
        
        # Send the final response back to the client
        client_socket.sendall(layer2_response.encode())
        
        # Close the client socket
        client_socket.close()
