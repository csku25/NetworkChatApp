#!/usr/bin/env python3
#   Author:		Venus Velazquez
#	Major:		CS
#	Due Date:	Dec. 14, 2023
#	Course:		CSC328 020
#	Assignment:	Network Program
#	Filename:	server.py
#	Purpose: 	Multi-client chat server

import sys, socket, threading, datetime, signal, time, lib_team

# dictionary to map client sockets to their nicknames
clients = {}
# dictionary to map nicknames to their respective messages
client_messages = {}

# Description: Handles ctrl+c abort
# Parameters:  int signum - signal number, frame obj frame - current execution frame
# Returns:     N/A
def sigint_handler(signum, frame):
    # send shut down message to all clients
    broadcast_all("The server will shut down in 5 seconds. Goodbye!")
    # wait for specified seconds
    time.sleep(5)
    # cleanup
    sys.exit(0)

# assign the SIGINT signal handler
signal.signal(signal.SIGINT, sigint_handler)

# Description: Processes each client individually 
# Parameters:  socket client_sock - the connected client socket
# Returns:     N/A
def handle_client(client_sock):
    # sending HELLO upon client connection
    client_sock.sendall(lib_team.pack_message("HELLO"))
    while True:
        try:
            message = client_sock.recv(1024).decode()
            if message.startswith("NICK"):
                # extract nickname from the message
                nickname = message[4:].strip()
                if nickname not in clients.values():
                    # nickname is unique
                    client_sock.sendall(lib_team.pack_message("READY"))
                    clients[client_sock] = nickname
                    # log client info
                    log_client_info(client_sock, nickname)
                else:
                    # nickname is not unique
                    client_sock.sendall(lib_team.pack_message("RETRY"))
            elif message.startswith("BYE"):
                # remove disconnected client
                remove_client(client_sock, clients[client_sock])
                break
            elif message:
                # handle chat messages
                nickname = clients[client_sock]
                client_messages[nickname] = message
                # log chat message
                log_chat_message(client_sock, message)
                # broadcast to other clients
                broadcast(nickname)
        except ConnectionResetError:
            # remove disconnected client from set
            remove_client(client_sock, clients[client_sock])
            break
        except KeyboardInterrupt:
            sigint_handler(signal.SIGINT, None)
    client_sock.close()

# Description: Removes disconnected client from dicts and closes socket
# Parameters:  socket client_sock - current connected client socket
# Returns:     N/A
def remove_client(client_sock, nickname):
    print(f"{clients[client_sock]} disconnected")
    try:
        # free up resources
        del clients[client_sock]
        if nickname in client_messages: 
            del client_messages[nickname]
        client_sock.close()
    except KeyError as e:
        print("KeyError:", e)

# Description: Inputs nickname, time, and IP of connected clients into a log file
# Parameters:  socket client_sock - current client socket, str nickname - client's chosen nickname
# Returns:     N/A
def log_client_info(client_sock, nickname):
    try:
        # log timestamp, IP address, and nickname
        timestamp = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        ip = client_sock.getpeername()[0]
        with open("log.txt", "a") as log_file:
            log_file.write(f"{nickname} connected on {timestamp} IP Address: {ip}\n")
    except Exception as e:
        print("Error logging messages:", e)
        
# Description: Inputs nickname, time, and message on connected clients to a log file
# Parameters:  socket client_sock - current connected client, str message - text sent by client
# Returns:     N/A
def log_chat_message(client_sock, message):
    try: 
        # log chat message
        timestamp = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        nickname = clients[client_sock]
        # format message
        log_message = (f"{nickname}: \"{message}\" {timestamp}\n")
        # write message to log file
        with open("log.txt", "a") as log_file:
            log_file.write(log_message)
    except Exception as e:
        print("Error logging messages:", e)

# Description: Broadcasts message from sender to all clients
# Parameters:  str sender_nick - the sender's nickname
# Returns:     N/A
def broadcast(sender_nick):
    sender_mess = client_messages.get(sender_nick)
    if sender_mess:
        for client_sock, nickname in clients.items():
            if nickname != sender_nick:
                try:
                    client_sock.sendall(lib_team.pack_message(f"{sender_nick}: {sender_mess}"))
                except Exception as e:
                    print("Error broadcasting message to other clients:", e)
    else:
        print(f"No message found for {sender_nick}.")

# Description: Broadcasts message to all clients
# Parameters:  str message - message to be sent
# Returns:     N/A
def broadcast_all(message):
    for client_sock in clients:
        try:
            client_sock.sendall(message.encode())
        except socket.error as e:
            print(f"Error broadcasting message: {e}")

def main():
    if len(sys.argv) != 2:
        exit('Usage: ./server host <port>')
    host = ""
    port = int(sys.argv[1])
    try:
        s_socket = socket.socket()
        s_socket.bind((host, port))
        s_socket.listen(5)
        print(f"Listening on port {port}")
        while True:
            (client_sock, _) = s_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_sock,))
            client_handler.start()
    except OSError as err:
        print("Error: ", err)
        s_socket.close()
        sys.exit(-1)
    except KeyboardInterrupt:
        sigint_handler(signal.SIGINT, None)
        s_socket.close()

if __name__ == "__main__":
    main()
