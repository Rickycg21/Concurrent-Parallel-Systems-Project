import socket
import threading

host_ip = socket.gethostbyname(socket.gethostname())
port = 2222
bytesize = 1024

#Creating Client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #We use IPV4 and TCP
#Connecting the Client Socket with an IP adress and the Server's Port
client_socket.connect((host_ip, port))

#Send a message to the server
def send_message():
    while True:
        message = input("Client: ")
        client_socket.send(f"\nClient: {message}".encode()) #Encode and send the message

        #Check if client wants to quit
        if message == "quit":
            print("\nDisconnected.")
            client_socket.close()
            break
    
#Recieve a message from the server
def receive_message():
    while True:
        #Recieve the message and decode
        message = client_socket.recv(bytesize).decode() 
        #Check if the server quits
        if message == "quit":
            client_socket.send("quit".encode()) #Send Comfirmation to the Server
            print("\nDisconnected.")
            client_socket.close()
            break
        #Print the message
        else:
            print(f"\n{message}")


t1 = threading.Thread(target=send_message)
t2 = threading.Thread(target=receive_message)

t1.start()
t2.start()
t1.join()
t2.join()

client_socket.close()
