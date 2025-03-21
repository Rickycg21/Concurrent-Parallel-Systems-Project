import socket
import threading

host_ip = socket.gethostbyname(socket.gethostname())
port = 2222
bytesize = 1024

#Creating Client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #We use IPV4 and TCP
#Connecting the Client Socket with an IP adress and the Server's Port
client_socket.connect((host_ip, port))

#Send and Recieve Messages
while True:
    message = client_socket.recv(bytesize).decode() #Recieve the message and decode

    #Check if server quits
    if message == "quit":
        client_socket.send("quit".encode()) #Send Comfirmation to the Server
        print("\nDisconnected.")
        break
    #If not send message
    else:
        print(f"\n{message}")
        message = input("\nClient: ")
        client_socket.send(message.encode()) #Encode and send the message

#Close
client_socket.close()






