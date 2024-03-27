Original Repo: https://github.com/mdela359/csc328
# CSC 328 Client/Server Application (Venus, K'drian, Martin)

## ID Block
- Author(s): K'drian Vega, Venuz Velazquez, Martin De La Cruz Valdez
- Major(s): Computer Science, Computer Science, Information Technology respectively.
- Due Date: December 14, 2023
- Course: CSC 328 Secure Network Programming
- Instructor Name: Dr Schwesinger
- Filename(s): client.py, server.py, lib_team.py
- Purpose: Develop a network chat application using stream sockets. The application functions as a group chat, allowing users to exchange messages amongst themselves. To allow smooth communication, the users will not recieve the message they send themselves.

## Installation
*How to Build and Run the Client and Sever*
### client.py
- import the following modules:
  ```python
  import sys, socket, threading
  from lib_team import *
  ```
### server.py
- import the following modules:
  ```python
  import sys, socket, threading, datetime, struct, signal, time, lib_team
  ```
### How to Build and Run the Client and the Server
To build the executable, ensure that the Make build automation tool is installed and execute the following command in your terminal:.

```bash
make
```
Upon execution, two executable files will be created: client and server.
**Running the Server**

To initiate the server, use the following command format:
For example:
```bash
./server [port_number]
```

Replace [port_number] with a 5-digit number of your choice. For example:

```bash
./server 43221
```

**Running the Client**

```bash
./client [host] [port_number]
```

Replace [host] with the server's IP address (e.g., 127.0.0.1) and [port_number] with the same 5-digit number used for the server. For instance:

```bash
./client 127.0.0.1 43221
```

**Application Usage**

Upon connecting the client to the server, the application's functionality is as follows:

    Username Selection: 
      The client will be prompted to choose a username or nickname. If a similar username is already in use, the server will respond           with a "RETRY" message until a unique username is chosen.

    Server Communication:
        Initial Connection: The server sends an initial "HELLO" message to the client upon connection.
        Username Validation: If needed, the server prompts the client to select a unique username with a "RETRY" message.
        Connection Confirmation: Once a unique username is chosen, the server sends a "READY" message.

    Client Interaction:
        Disconnect: When the client sends a "BYE" message, it indicates readiness to disconnect.
        Messaging: Clients can exchange messages and view messages sent by other connected clients.

Clients will be able to see messages from other clients.


## File/folder manifest identifying the purpose of each file/folder included in the project

### server.py
- Log client information into a file.
- Handle the transmission of messages between clients.
- Handle the client connections.
- Send messages to clients.
- Receive messages.

### client.py
- Select username/nickname.
- Connect to server.
- Receive messages.

### lib_team
- Contain common functions between server and client.
  - Receive messages.
  - Read bytes.
  - User input
  - Pack messages
 
### test_lib_team
- Test functions that can be tested using the unittest module

  
## Responsibility Matrix
*table containing a row for each team member and the aspects of the project to which they contributed*

**Venus:** server.py

**K'drian:** client.py

**Martin:** lib_team.py, test_lib_team.py, Makefile

| Team Member  |  Contributed to                      |
| -----------  | -------------------------------------|
| Venus        | server.py, integration               |
| K'drian      | client.py, integration               |
| Martin (P.M) | lib_team.py, test_lib_team, Makefile |


## A section that corresponds to section 3 of the design document.

Task 1: Application Design

List project members (Team) : 1 min

Setup communication plan (Team) : 5 mins

List all tasks (Team) : 15 mins

Select programming languages (Team) : 2 mins

Specify project requirements (Team) : 25 mins

List application inputs and outputs (K’drian) : 30 mins

List functionalities (Martin) 

Specify application protocol (Venus) : 20 mins

Create sequence diagram (Martin) 

Create test plan (Team) : 10 mins


Task 2: Server Implementation (Venus)

Implement server socket creation and binding : 15 mins

Implement threads : 23 mins

Develop server functionalities for handling connections : 6 hours

Design nickname verification : 24 mins

Create a logging system for client connection details and messages : 2 hours 16 mins

Integrate signal handling for graceful shutdown : 1 hour 30 mins

Document functions : 12 mins


Task 3: Client Implementation (K’drian)
Construct client structure : 15 mins

Establish client socket connections : 15 mins

Implement message sending to server : 3 hours

Enable receipt of messages from server : 2 hours

Handle client-side input and user interactions : 6 hours


Task 4: Library Implementation (Martin)

Implement common functionalities 30 minutes

Sending messages 15 minutes

Receiving messages 15 minutes

Data validation 30 minutes

Create unit tests 30 minutes

Task 5: Testing & Debugging

Run tests 13 minutes

Error handle and debug 


Task 6: Documentation (Team)

Write readme file template (Martin): 13 minutess

ID Block (Martin): 9 minutes

How-to guide (Martin): 36 minutes

File/folder manifest (Martin): 32 minutes

Responsibility matrix (Martin): 7 minutes

Tasks & times (Team) : 20 - 35 minutes

Protocol (Venus) : 28 mins

Assumptions (K'drian) : 35 mins

Development process : days

Status (Team): 5 minites

## Protocol

### Client:
**Connection handling:**

Upon connection:
  - Client connects to the server.
  - Waits to receive a "HELLO" message from the server upon successful connection.

**Nickname Selection:**

Prompt User:
  - Client prompts the user to select a unique nickname.

Send Nickname:
  - Client sends the chosen nickname to the server using the "NICK" message format, containing the proposed nickname.

Nickname Verification:
  - Waits for a response from the server.
  - If the client receives "READY," it proceeds to send and receive messages.
  - If the client receives "RETRY," it prompts the user to choose a different unique nickname and resends the "NICK" message.
  
**Message Exchange:**

Write Timing:
  - When the user wants to send a message, the client initiates a write operation to the socket, sending the message to the server.

Read Timing:
  - The client continuously listens for incoming messages from the server in a dedicated thread while also allowing the user to input 
     messages for sending to the server.

**Disconnect:**

Voluntary Disconnect:
  - When the user voluntarily disconnects, client sends a "BYE" message to the server to indicate the intention to disconnect.

**Server Shutdown:**

Graceful Shutdown Handling:
  - Reacts to the "Server will shut down in 'x' seconds" message from the server, indicating the server's planned shutdown.
  - Handles disconnection gracefully, closes the client socket, and releases any resources upon receiving the server shutdown signal.

### Server

**Connection Handling:**

Upon client connection:
    - Server sends a "HELLO" message to the connected client upon successful connection.

**Nickname Verification:**

Receive Nickname:
  - Server receives the chosen nickname from the client using the "NICK" message format, containing the proposed nickname.

Nickname Uniqueness Check:
  - Checks the uniqueness of the received nickname.
  - If unique, sends a "READY" message to the client, authorizing them to send and receive messages.
  - If not unique, sends a "RETRY" message to prompt the client for a different unique nickname.

Nickname Verification:
  - Waits for a response from the server.
  - If the client receives "READY," it proceeds to send and receive messages.
  - If the client receives "RETRY," it prompts the user to choose a different unique nickname and resends the "NICK" message.

**Message Exchange:**

Read Timing:
  - Server continuously listens for and receives messages from connected clients, it operates in a loop, waiting for data on sockets and 
    processing it upon arrival.
  - Server has a mechanism to handle multiple clients concurrently, through threading.

Write Timing:
  - Upon receiving a message from a client, the server writes data to the sockets of all connected clients except the sender.

**Logging:**

Logging Incoming Messages:
    - Logs incoming messages to a file, including the client's nickname at the start of the message, timestamp, and message content.
    
**Disconnect Handling:**

Handling Client Disconnect:
  - Listens for "BYE" messages from clients indicating voluntary disconnection.
  - Closes the socket associated with the disconnected client.
  - Releases allocated memory/resources used by the client's connection.

Graceful Server Shutdown:
  - Handles the server shutdown signal reception gracefully.
  - Sends a "Server will shut down in 'x' seconds" message to all connected clients.
  - Waits for the specified time before initiating a graceful shutdown, closing sockets, and releasing all connected clients.

## Assumptions
- Assumed the client would have to send the size in bytes of each message sent, turned out to be unnecessary.
- Assumed users can reliably connect to the server without disruptions for the chat to function seamlessly.
- Assumed that the selected port for socket communication are not blocked by firewalls or restricted by network policies.
- Assumed that the application can gracefully handle network disruptions, server failures, or other unexpected errors without crashing or losing data.
- Assumed the server would need separate functions to handle keywords such as NICK, READY, RETRY, etc., all could be handled within one function.
- Assumed the buffer size and handling of data in the client-side socket, expecting that it can handle incoming data appropriately without overflowing or losing information.
- Assumed the application manages concurrent access to shared resources to avoid data corruption or race conditions.
- Assumed that data sent through to the log files is formatted correctly according to the protocol.
- Assumed the format of data sent by client is expected by the server.
- Assumed that the server has the ability to handle a large load without significant performance degradation.
- Assumed that Python versions used on the server and client sides are compatible with the library and features being used.
- Assumed that the socket library functions and their behaviors align with the official documentation.
- Assumed that the Python socket library functions behave consistently across different operating systems without platform-specific issues or variations.
- Assumed the stability and reliability of the library code, expecting that updates or changes to the library won't significantly affect the functionality of the existing code.
## Discussion on your development process
We encountered issues like socket leaks, improper closing of connections, or mishandling of socket objects which can lead to resource depletion or unexpected behavior. Handling multiple client connections concurrently led to synchronization issues, race conditions, or deadlock situations when dealing with shared resources like sockets or data structures, especially in a multi-threaded environment. We experienced unexpected network interruptions, packet loss, and delays. They can disrupt communication between the server and clients. Testing the network chat application thoroughly to simulate various network conditions and debugging issues related to asynchronous behavior, network failures, or race conditions were time-consuming and complex. The linux server CSITRD also seemed to inconveniently lose the ability to handle socket connections closer to the due date. Inadequate documentation and changes in library functionalities, along with the individual server and client applications, led to confusion or difficulties in understanding and utilizing the features effectively. 
We communicated and tried to help each other out as much as possible to get to our final end product. It was tough and taught us a lot about how important communication is and being open to hearing other people's perspectives on things. It also showed us how difficult it can be to integrate different files that are all written by different people. They didn't always mesh well together so it took a bit of back and forth to figure out what needed to change so that it was harmonious.
## Status
*current status of applications in terms of specifications, and any known issues with the application*
- Normal behavior on local machines. Limits on the acad server.
