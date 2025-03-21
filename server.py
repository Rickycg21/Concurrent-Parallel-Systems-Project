import socket
import threading

#Declarations
host_ip = socket.gethostbyname(socket.gethostname()) 
port = 2222                                           
bytesize = 1024                             

#Dictionary of valid users and their passwords
registered_users = {
    "Omar": "1234",
    "Diego": "1234",
    "Ricardo": "1234",
    "Mario": "1234"
}

active_users = {}  #Username to client_socket for currently logged-in users
user_lock = threading.Lock()  #Lock to protect shared access to active_users

#Creating Server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #We use IPV4 and TCP
#Binding the Server Socket to an IP adress and a Port
server_socket.bind((host_ip, port))
#Listening for connections
server_socket.listen()

print(f"[+] Server running at {host_ip}:{port}")

#Forward a recieved message back to it's real destination
def forward(message, sender=None):
    with user_lock:
        for user, sock in active_users.items():
            if user != sender:  #Don't send message back to sender
                try:
                    sock.send(f"{message}\n".encode())  #Send the message
                except:
                    pass  #Ignore failed sends

#Connect incoming client
def handle_client(client_socket, addr):
    username = None  #Default in case we fail early

    try:
        #Prompt for login
        client_socket.send("Username: ".encode()) 
        username = client_socket.recv(bytesize).decode().strip()  

        client_socket.send("Password: ".encode())  
        password = client_socket.recv(bytesize).decode().strip() 

        #Validate credentials
        if registered_users.get(username) != password:
            client_socket.send("Login failed. Disconnecting.".encode())  #Reject client
            client_socket.close()
            return

        #Check for duplicate login
        with user_lock:
            if username in active_users:
                client_socket.send("User already logged in.".encode())  #Prevent double login
                client_socket.close()
                return
            active_users[username] = client_socket  #Add to active users

        #Confirm login
        client_socket.send(f"Login successful. Welcome {username}!".encode())  #Acknowledge
        print(f"[+] {username} successfully logged in from {addr}")
        forward(f"[Server]: {username} has joined the chat.", sender=username)

        #Listen for messages
        while True:
            message = client_socket.recv(bytesize).decode()  #Wait for message from client
            if not message:
                break  #Client disconnected

            if message.strip().lower() == "/quit":
                break  #User requested to quit

            if message.strip().lower() == "/available":
                with user_lock:
                    online_users = [u for u in active_users if u != username]  #Exclude self

                response = "[Server]: Online users: "
                response += ', '.join(online_users) if online_users else "No other users online."

                client_socket.send(response.encode())  #Send user list to requester
                continue

            print(f"[{username}]: {message}")  #Log to server console
            forward(f"{username}: {message}", sender=username)  #Forward to others

    except Exception as e:
        print(f"[ERROR] {e}")

    finally:
        with user_lock:
            if username in active_users:
                del active_users[username]  #Remove from active list
                print(f"[-] {username} disconnected")
                forward(f"[Server]: {username} has left the chat.", sender=username)
        client_socket.close()  #Clean up socket

#Start the server loop
while True:
    client_socket, client_address = server_socket.accept()  #Accept new client
    threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
