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

    if msg == "DISCONNECT":
        flag += 1
        break

    if msg == "QUERYP":
        print(client.recv(2048).decode(FORMAT))
    
    if msg == "QUERYG":
        print(client.recv(2048).decode(FORMAT))

