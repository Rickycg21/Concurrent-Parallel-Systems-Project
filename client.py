import socket
import threading

#Declarations
server_ip = socket.gethostbyname(socket.gethostname())
port = 2222
bytesize = 1024

#Connecting to the Server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, port))

#Login Process
#Receiving Username
username_prompt = client_socket.recv(bytesize).decode()
username = input(username_prompt)
client_socket.send(username.encode())

#Receive Password
password_prompt = client_socket.recv(bytesize).decode()
password = input(password_prompt)
client_socket.send(password.encode())

#Receive and print login result
login_response = client_socket.recv(bytesize).decode()
print(login_response)

#Receiving messages
def receive_messages():
    while True:
        try:
            message = client_socket.recv(bytesize).decode()
            if not message:
                break  #close connection
            print(message)
        except:
            break  #Error

#Message Sending Function
def send_messages():
    while True:
        message = input()
        client_socket.send(message.encode())

#Start Chat Threads
threading.Thread(target=receive_messages, daemon=True).start()
send_messages()  #Thread that handles input
