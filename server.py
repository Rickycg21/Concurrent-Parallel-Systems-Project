import socket

#Creating Server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #We use IPV4 and TCP

#Binding the Server Socket to an IP adress and a Port
server_socket.bind((socket.gethostbyname(socket.gethostname()), 22222))

#Listening for connections
server_socket.listen()

#Accept connections and get the Client's socket and adrdess
while True:
    client_socket, client_address = server_socket.accept()
    print(client_socket)
    print(f"Connected to {client_address}")
