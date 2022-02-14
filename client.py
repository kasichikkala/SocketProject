import socket
import sys
from unicodedata import name

HEADER = 64
PORT = int(sys.argv[2])
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
SERVER = str(sys.argv[1])
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


count = 0

while True:
    if(count == 0):
        msg = input("Register player: [USERNAME , IP, PORT]")
        #msg.split(" ")
        #msg = msg[0]
        send(msg)
        count +=1

    msg = input("Enter a Message: ")
    send(msg)

    if msg == "DISCONNECT":
        break

    if msg == "QUERYP":
        print(client.recv(2048).decode(FORMAT))
    
    if msg == "QUERYG":
        print(client.recv(2048).decode(FORMAT))
