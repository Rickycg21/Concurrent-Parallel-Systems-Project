import socket

#Declarations
host_ip = socket.gethostbyname(socket.gethostname())
port = 2222
bytesize = 1024

#Creating Server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #We use IPV4 and TCP
#Binding the Server Socket to an IP adress and a Port
server_socket.bind((host_ip, port))
#Listening for connections
server_socket.listen()
#Accept connections and get the Client's socket and adrdess
client_socket, client_address = server_socket.accept()
#Send notification to the client that he has been connected
client_socket.send("Connected to Server.".encode()) #Make sure the String is encode
print("Client Connected")

#Send and Receive messages
while True:
    message = client_socket.recv(bytesize).decode() #Recieve Messages and decode

    #Check if client quits
    if message == "quit":
        client_socket.send("quit".encode()) #Send Comfirmation to the Server
        print("\nDisconnected.")
        break
    #If not send message
    else:
        print(f"\n{message}")
        message = input("\nServer: ")
        client_socket.send(message.encode())#Encode and send the message

#Close
server_socket.close()
