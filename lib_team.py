#Author: Martin De La Cruz Valdez
#Major: Information Technology
#Due Date: December 14, 2023
#Course: CSC328
#Professor Name: Dr. Schwesinger
#Assignment: final project
#Filename: lib_team.py

import struct

# This is was modeled after really_read in client.py by Dr. Schwesinger
# /export/home/public/schwesin/csc328/examples/project5/Python

def read_bytes(sock, num_bytes):
    """
    Reads a specified number of bytes from a socket.

    Args:
    - sock (socket): The socket object to read from.
    - num_bytes (int): The number of bytes to read.

    Returns:
    - bytes: The read bytes from the socket.
    """
    sock = sock
    my_bytes = b''
    while len(my_bytes) != num_bytes:
        bytes_read = sock.recv(num_bytes - len(my_bytes))
        my_bytes += bytes_read
        if len(bytes_read) == 0: break
    return my_bytes

def user_input(fd):
    """
    Accepts user input and sends it through a socket.

    Args:
    - fd: The file descriptor/socket to send the input.

    Returns:
    - None
    """
    while True:
        try:
            user_message = input("Me: ")
            if user_message.strip():
                fd.sendall(user_message.encode())
        except KeyboardInterrupt:
            raise KeyboardInterrupt

def generate_wordspackets(words):
    """
    Generates packets of words encoded as bytes.

    Args:
    - words (list): List of words to be packed into bytes.

    Returns:
    - bytes or str: Encoded bytes containing word packets or a UnicodeError message.
    """
    b= b''
    try:
        for word in words:
            wordpacket = struct.pack('!H', len(word)) + word.encode('ascii')
            b += wordpacket
        return b
    except UnicodeError:
        return 'Unicode Error occured while encoding'
    
def pack_message(message):
    """
    Packs a message into bytes, considering its length.

    Args:
    - message (str): The message to be packed into bytes.

    Returns:
    - bytes or str: Encoded bytes containing the message or a UnicodeError message.
    """

    b= b''
    try:
        wordpacket = struct.pack('!H', len(message)) + message.encode('ascii')
        b += wordpacket
        return b
    except UnicodeError:
        return 'Unicode Error occured while encoding'
    

def receive_messages(fd):
    """
    Receives messages from a socket, decodes, and prints them.

    Args:
    - fd: The file descriptor/socket to receive messages from.

    Returns:
    - None
    """
    while True:
        try:
            msg_len = int.from_bytes(read_bytes(fd, 2), 'big')
            if msg_len != 0:
                msg = read_bytes(fd, msg_len)
                print('\r' + msg.decode())
        except (ConnectionResetError, ConnectionAbortedError):
            fd.sendall("BYE".encode())
            print("\rConnection to the server has been closed.")
            break
        except OSError:
            print("\rConnection to the server has been closed.")
            break
