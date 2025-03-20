import socket

#Creating Client socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #We use IPV4 and TCP

#Binding the Server Socket to an IP adress and a Port
server_socket.bind(socket.gethostbyname(socket.gethostname(), 2222))

#Listening for connections
server_socket.listen()
