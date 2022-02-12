import socket
from unicodedata import name

HEADER = 64
PORT = 41001
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
SERVER = "10.120.70.145"
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
        msg = input("Enter your Name: ")
        send(msg)
        count +=1

    msg = input("Enter a Message: ")
    send(msg)

    if msg == "DISCONNECT":
        break

