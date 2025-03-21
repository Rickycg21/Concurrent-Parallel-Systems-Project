import socket

#Creating Server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #We use IPV4 and TCP

#Binding the Server Socket to an IP adress and a Port
server_socket.bind((socket.gethostbyname(socket.gethostname()), 22222))

#Listening for connections
server_socket.listen()


while True:
    #Accept connections and get the Client's socket and adrdess
    client_socket, client_address = server_socket.accept()

    #Send notification to the client that he has been connected
    client_socket.send("Connected".encode()) #Make sure the String is encoded

    #Close
    server_socket.close()
    break