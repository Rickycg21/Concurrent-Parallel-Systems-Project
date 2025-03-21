import socket
import threading

#Declarations
host_ip = socket.gethostbyname(socket.gethostname())
port = 2222
bytesize = 1024

client_socket_list = []
client_name_list = []

#Creating Server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #We use IPV4 and TCP
#Binding the Server Socket to an IP adress and a Port
server_socket.bind((host_ip, port))
#Listening for connections
server_socket.listen()

#Accept connections and get the Client's socket and adrdess
client_socket, client_address = server_socket.accept()
client_socket_list.append(client_socket)
#Send notification to the client that he has been connected
client_socket.send("Connected to Server.".encode()) #Make sure the String is encode
print("Client Connected")

#Forward a recieved message back to everyone else
def forward_message(message):
    pass

def send_message():
    while True:
        message = input("Server: ")
        client_socket.send(f"\nServer: {message}".encode()) #Encode and send the message

        #Check if server wants to quit
        if message == "quit":
            print("\nDisconnected.")
            client_socket.close()
            break

#Recieve incoming message
def receive_message(client_socket):
    while True:
        #Recieve Messages and decode
        message = client_socket.recv(bytesize).decode() 
        #Check if client quits
        if message == "quit":
            print("\nDisconnected.")
            break
        #Print message
        else:
            print(f"\n{message}")
#Connect incoming client
def connect_client():
    pass


t1 = threading.Thread(target=send_message)
t2 = threading.Thread(target=receive_message, args=(client_socket,))



t1.start()
t2.start()
t1.join()
t2.join()


#Close
server_socket.close()



