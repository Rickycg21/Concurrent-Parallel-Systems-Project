import socket
import threading

#Declarations
host_ip = socket.gethostbyname(socket.gethostname())
port = 2222                                            
bytesize = 1024                                        

#Dictionary of all registered users Hardcoded
registered_users = {
    "Omar": "1234",
    "Diego": "1234",
    "Ricardo": "1234",
    "Mario": "1234"
}

#Dictionary to store all active users
active_users = {}
user_lock = threading.Lock()  #Thread safety for shared data


#Creating Server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Binding the Server Socket to an IP adress and a Port
server_socket.bind((host_ip, port))
#Listening for connections
server_socket.listen()

print(f"Server running")

#Forward message to all clients except sender
def forward(message, sender=None):
    with user_lock:
        for user, sock in active_users.items():
            if user != sender:
                try:
                    sock.send(f"{message}\n".encode())
                except:
                    pass  #Skip if there's an issue sending

#Handle an individual client
def handle_client(client_socket, addr):
    username = None  # tore username once authenticated
    try:
        #Prompt for Username
        client_socket.send("Username: ".encode())
        username = client_socket.recv(bytesize).decode().strip()

        #Prompt for Password
        client_socket.send("Password: ".encode())
        password = client_socket.recv(bytesize).decode().strip()

        #Verify Username and Password
        if registered_users.get(username) != password:
            client_socket.send("Login failed. Disconnecting.".encode())
            client_socket.close()
            return

        #Prevent multiple logins
        with user_lock:
            if username in active_users:
                client_socket.send("User already logged in.".encode())
                client_socket.close()
                return
            active_users[username] = client_socket  #Add to active user

        #Confirm Login
        client_socket.send(f"Login successful. Welcome {username}".encode())
        forward(f"[Server]: {username} has joined the chat.", sender=username)

        #Receive and broadcast messages
        while True:
            message = client_socket.recv(bytesize).decode()
            if not message:
                break  #Client disconnected

            if message.strip() == "/quit":
                break  #User wants to quit

            print(f"[{username}]: {message}")
            forward(f"{username}: {message}", sender=username)


    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        #Cleanup on disconnect
        with user_lock:
            if username in active_users:
                del active_users[username]
        client_socket.close()
        print(f"{username} disconnected")
        forward(f"[Server]: {username} has left the chat.", sender=username)


#Accept and handle clients
while True:
    client_socket, client_address = server_socket.accept()
    threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
