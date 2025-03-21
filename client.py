import socket
import threading

#Declarations
server_ip = socket.gethostbyname(socket.gethostname())
port = 2222
bytesize = 1024
stop_threads = threading.Event()

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
print("\nAvailable commands:")
print("/commands   - Show this command list")
print("/available  - Show currently online users")
print("/\"username\" - Select a user to message")
print("/quit       - Exit the chat")
print("Type below:\n")


#Receiving messages
def receive_messages():
    while not stop_threads.is_set():
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                break
            print(message)
        except:
            break

#Message Sending Function
def send_messages():
    while not stop_threads.is_set():
        message = input()
        client_socket.send(message.encode())

        if message.strip().lower() == "/quit":
            stop_threads.set()  #Signal to stop receiving thread
            break

    client_socket.close()
    print("Disconnected from server.")




#Start Chat Threads
threading.Thread(target=receive_messages, daemon=True).start()
send_messages()  #Thread that handles input
