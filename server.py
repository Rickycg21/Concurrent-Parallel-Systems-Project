#Declarations
import socket
import threading
import time
from datetime import datetime

#Declarations
host_ip = socket.gethostbyname(socket.gethostname()) 
port = 2333                                           
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

# Max 3 clients at a time
client_semaphore = threading.Semaphore(3)
waiting_clients = []  #Queue of (client_socket, address)

#Creating Server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #We use IPV4 and TCP
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  #Allow reusing port
server_socket.bind((host_ip, port))
server_socket.listen()

print(f"[+] Server running at {host_ip}:{port}")

#Forward a recieved message back to it's real destination
def forward(message, sender=None):
    timestamp = datetime.now().strftime("[%H:%M:%S] ") #Add timestamp to messages
    with user_lock:
        for user, sock in active_users.items(): #Send message to all users except sender
            if user != sender:
                try:
                    sock.send(f"{timestamp}{message}\n".encode())
                except:
                    pass #Ignore failures

#Handle actual client after reaching front of queue
def handle_client(client_socket, addr):
    username = None
    try:
        #Prompt for login
        client_socket.send("Username: ".encode()) 
        username = client_socket.recv(bytesize).decode().strip()  
        #Prompt for password
        client_socket.send("Password: ".encode())  
        password = client_socket.recv(bytesize).decode().strip() 
        #Login fail message
        if registered_users.get(username) != password:
            client_socket.send("Login failed. Disconnecting.".encode())
            client_socket.close()
            return
        with user_lock:
            if username in active_users:
                client_socket.send("User already logged in.".encode())
                client_socket.close()
                return
            active_users[username] = client_socket #Add to active user list
        #Login successful
        client_socket.send(f"Login successful. Welcome {username}!".encode())
        print(f"[+] {username} successfully logged in from {addr}")
        forward(f"[Server]: {username} has joined the chat.", sender=username)

        #Main chat loop
        while True:
            message = client_socket.recv(bytesize).decode() #Wait for message
            if not message:
                break

            if message.strip().lower() == "/quit":
                break #User requested to leave

            if message.strip().lower() == "/available":
                with user_lock:
                    online_users = [u for u in active_users if u != username] #Get other users

                response = "[Server]: Online users: "
                response += ', '.join(online_users) if online_users else "No other users online."

                client_socket.send(response.encode()) #Send list to requesting user
                continue

            timestamp = datetime.now().strftime("[%H:%M:%S]") #Server log with time
            print(f"{timestamp} [{username}]: {message}")
            forward(f"{username}: {message}", sender=username) #Relay to others

    except Exception as e:
        print(f"[ERROR] {e}") # Print error

    finally:
        with user_lock:
            if username in active_users:
                del active_users[username] #Remove from active users
                print(f"[-] {username} disconnected")
                forward(f"[Server]: {username} has left the chat.", sender=username)
        client_socket.close()
        client_semaphore.release()  #Release the slot

# Monitor queue and promote clients when space opens
def queue_manager():
    while True:
        time.sleep(1) #Check queue once per second
        if waiting_clients and client_semaphore._value > 0:
            with user_lock:
                next_client, addr = waiting_clients.pop(0) #Take next client from queue
            threading.Thread(target=enter_chat, args=(next_client, addr)).start() #Allow to try joining

# Handles queue wait and transition
def enter_chat(client_socket, addr):
    try:
        while True:
            with user_lock:
                position = waiting_clients.index((client_socket, addr)) + 1 if (client_socket, addr) in waiting_clients else 0

            if client_semaphore.acquire(blocking=False):
                # Accepted into active clients
                handle_client(client_socket, addr)
                break
            else:
                if position > 0:
                    try:
                        client_socket.send(f"[Server]: All slots full. You are #{position} in the queue.\n".encode())
                    except:
                        pass #Ignore send failure
                time.sleep(3) # Retry after short delay
    except:
        pass  #Client disconnected while waiting

#Accept incoming connections
def accept_connections():
    while True:
        client_socket, client_address = server_socket.accept() #Accept new client
        print(f"[!] Incoming connection from {client_address}")

        with user_lock:
            if client_semaphore._value > 0:
                client_semaphore.acquire() #Take a slot immediately
                threading.Thread(target=handle_client, args=(client_socket, client_address)).start()
            else:
                waiting_clients.append((client_socket, client_address)) #Add to waiting list
                threading.Thread(target=enter_chat, args=(client_socket, client_address)).start()

#Start threads
threading.Thread(target=queue_manager, daemon=True).start() #Run queue manager in background
accept_connections() #Start accepting clients





