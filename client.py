import socket
import sys
from unicodedata import name

HEADER = 64
PORT = 5050 #int(sys.argv[2])
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
SERVER = "192.168.56.1" #str(sys.argv[1])
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))


flag = 0

while(flag== 0):
    msg = input("Enter a Message: ")
    send(msg)

    clientMsg = msg.split(" ")
    if clientMsg[0] == "DISCONNECT":
        flag += 1
        break
    
    if clientMsg[0] == "GAME":
        print(client.recv(2048).decode(FORMAT))
        for i in returnmsg
        {
            peerSocket.connect(ADDR)
            msg = "Inviting you to a game from"  
            message = msg.encode(FORMAT)
            msg_length = len(message)
            send_length = str(msg_length).encode(FORMAT)
            send_length += b' ' * (HEADER - len(send_length))
            client.send(send_length)
            client.send(message)   
        }
        

    if clientMsg[0] == "QUERYP":
        print(client.recv(2048).decode(FORMAT))
    
    if clientMsg[0] == "QUERYG":
        print(client.recv(2048).decode(FORMAT))

