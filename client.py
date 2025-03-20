import socket

#Creating Client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #We use IPV4 and TCP

#Connecting the Client Socket with an IP adress and the Server's Port
client_socket.connect((socket.gethostbyname(socket.gethostname()), 22222))