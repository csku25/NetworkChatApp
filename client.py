#!/usr/bin/env python3

# Filename:  client.py
# Author:    K'drian Vega
# Course:    CSC328
# Due:       12/14/23 @ 10am

import sys, socket, threading
from lib_team import *

# Function Name:  nick_selection
# Description:    loops through prompt for user to choose a unique nickname
# Parameters:     fd: a socket file descriptor -> socket type
# Return Value:   a string of decoded bytes received from the server
#                 that validates the nickname
# Type:           socket type -> str
def nick_selection(fd):
    nick = input("Enter a nickname: ")
    NICK = "NICK".encode() + nick.encode()
    fd.sendall(NICK)
    response_size = int.from_bytes(read_bytes(fd, 2), 'big')
    if response_size == 0: raise OSError
    return read_bytes(fd, response_size).decode()

def main():
    if len(sys.argv) != 3:
        exit(f"Usage: {sys.argv[0]} <host> <port>")

    try:
        with socket.socket() as sock:
            sock.connect((sys.argv[1], int(sys.argv[2])))
            acpt_len = int.from_bytes(read_bytes(sock, 2), 'big')

            if read_bytes(sock, acpt_len).decode() == "HELLO":
                response = nick_selection(sock)
                while response != "READY":
                    if response != "RETRY": raise OSError
                    print("Nickname already taken!\n")
                    response = nick_selection(sock)

                usr_thread = threading.Thread(target=usr_input, args=(sock,))
                rec_thread = threading.Thread(target=receive_messages, args=(sock,))
                rec_thread.start()
                usr_thread.start()
                usr_thread.join()

            else: raise OSError

    except ConnectionRefusedError:
        print("Connection to the server has been refused.")
        sys.exit()
    except OSError as e:
        print(f"\r{e}")
        sys.exit()
    except KeyboardInterrupt:
        print("Exiting program...  ")
        sys.exit()

if __name__ == "__main__":
    main()
