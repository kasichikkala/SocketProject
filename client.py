from ctypes.wintypes import PPOINT
import socket
import sys
from unicodedata import name
import threading

HEADER = 64
PORT =int(sys.argv[2])
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
SERVER = str(sys.argv[1])
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
global peer
peer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
flag = 0

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))



# def start():
#     global peer
#     peer.listen()
#     IPAddr = peer.getpeername()[0]
#     PPort = peer.getpeername()[1]
#     print(f"[LISTENING] Client is listening on " + IPAddr + " " + PPort)
#     while True:
#         conn, addr = peer.accept()
#         thread = threading.Thread(target=handle_peer, args=(conn, addr))
#         thread.start()

# def handle_peer(conn, addr):
#     print(f"[NEW CONNECTION] {addr} connected.")
#     connected = True 
#     while connected:
#         msg_length = conn.recv(HEADER).decode(FORMAT)
#         if msg_length:
#             msg_length = int(msg_length)
#             msg = conn.recv(msg_length).decode(FORMAT)
#             print(msg)
    


while(flag== 0):
    msg = input("Enter a Message: ")
    send(msg)

    clientMsg = msg.split(" ")
    if clientMsg[0] == "DISCONNECT":
        flag += 1
        break
    
    if clientMsg[0] == "GAME":
        #print("hello")
        gameInfo = client.recv(2048).decode(FORMAT)
        #print(msgR)

        #print("hello2")
        #gameInfo = client.recv(2048).decode(FORMAT)
        print(gameInfo)
       # print(gameInfo + " test")
        # peerIMSG = gameInfo.split(" -")
        # sIP = peerIMSG[1]
        # port = peerIMSG[2]
        # print(peerIMSG)
        # PADDR = (str(sIP),str(port))
        # msgP = "Game invitation from peer to peer"
        # peer.sendto(msgP.encode(FORMAT),((sIP),int(port)))
        # peer.close()


    if clientMsg[0] == "QUERYP":
        print(client.recv(2048).decode(FORMAT))
    
    if clientMsg[0] == "QUERYG":
        print(client.recv(2048).decode(FORMAT))


# start()
