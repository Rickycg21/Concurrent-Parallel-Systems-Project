import socket
import threading

#Declarations
bytesize = 1024
server_ip = socket.gethostbyname(socket.gethostname())
stop_threads = threading.Event()  #Used to stop threads on /quit
target_user = None  #Store selected private messaging target

#Create client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #We use IPV4 and TCP

#Connect to server
client_socket.connect((server_ip, 2222))

#Login authentication
username_prompt = client_socket.recv(bytesize).decode()
username = input(username_prompt)  #Enter username
client_socket.send(username.encode())
password_prompt = client_socket.recv(bytesize).decode()
password = input(password_prompt)  #Enter password
client_socket.send(password.encode())
#Show login result
login_response = client_socket.recv(bytesize).decode()
print(login_response)  
if "Login failed" in login_response or "already logged in" in login_response:
    client_socket.close()
    exit()

#Show command list on login
print("\nAvailable commands:")
print("/commands   - Show this command list")
print("/available  - Show currently online users")
print("/username   - Select a user to message privately")
print("/all        - Return to public chat")
print("/quit       - Exit the chat")
print("Type your message below:\n")

#Recieve incoming message
def receive_message():
    while not stop_threads.is_set():
        try:
            message = client_socket.recv(bytesize).decode()
            if not message:
                break  #Server closed connection

            cleaned = message.strip()
            if cleaned:
                print("\n" + cleaned)  # Print incoming message

        except:
            break  #Exit if socket error occurs

#Send message to server
def send_message():
    global target_user

    while not stop_threads.is_set():
        message = input()
        if stop_threads.is_set():
            break  #Exit if flagged for shutdown
        #Detect commands
        if message.strip().lower() == "/commands":
            print("\nAvailable commands:")
            print("/commands   - Show this command list")
            print("/available  - Show currently online users")
            print("/username   - Select a user to message privately")
            print("/all        - Return to public chat")
            print("/quit       - Exit the chat\n")
            continue
        #Request active users
        if message.strip().lower() == "/available":
            client_socket.send("/available".encode())  
            continue
        #Send quit signal
        if message.strip().lower() == "/quit":
            client_socket.send("/quit".encode())  
            stop_threads.set()
            break
        #Set private target
        if message.startswith("/") and message.lower() not in ["/quit", "/commands", "/available", "/all"]:
            selected = message[1:].strip()
            if selected:
                target_user = selected  
                print(f"[Client]: Now sending messages only to {target_user}.")
            continue
        #Switch back to public chat
        if message.strip().lower() == "/all":
            target_user = None  #
            print("[Client]: Switched back to public chat.")
            continue

        #Send message based on target
        if target_user:
            formatted = f"TO:{target_user}::{message}"
            client_socket.send(formatted.encode())
        else:
            client_socket.send(message.encode())

    #Disconect
    client_socket.close()
    print("Disconnected from server.")

#Start threads
t1 = threading.Thread(target=send_message)
t2 = threading.Thread(target=receive_message)
t1.start()
t2.start()
t1.join()
t2.join()
