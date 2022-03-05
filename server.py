from concurrent.futures import thread
from distutils import command
import socket
import sys 
import threading

HEADER = 64
PORT =  5050 #int(sys.argv[1])
SERVER = socket.gethostbyname(socket.gethostname()) #running manager on general4.asu.edu
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
START_GAME = "GAME"
DISCONNECT_MESSAGE = "DISCONNECT"
QUERYP_MESSAGE = "QUERYP"
QUERYG_MESSAGE = "QUERYG"


connectedIP = []
userNames = []
portNum = []
flagGame = True

game_identifier = 0

players = []
names = []
uCount = 0
games = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDR)

# class Player:
#     def __init__(self, name, port):
#         self.name = name
#         self.port = port

#     def __str__(self):
#         return "Name: %s  Port: %s" % (self.name, self.port)

#     def getName(self):
#         return "%s" % (self.name)

def handle_client(conn, addr):
    count = 0
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            commandmsg = msg.split(" ")
           
            if(commandmsg[0] == "register"):
                namemsg = commandmsg[1]
                addr = addr + (namemsg,flagGame,) 
                connectedIP.append(addr)
                print(addr)
                conn.send("SUCCESS".encode(FORMAT))

            # if commandmsg[0] == "register":
            #     temp = Player(commandmsg[1], commandmsg[3])
            #     print(temp)
            #     players.append(temp)
            #     #make it so that it starts another process called player.py that runs another socket. 
            
            if commandmsg[0] == DISCONNECT_MESSAGE:
                connected = False
                print(f"{addr[2]} has left the game!")
                connectedIP.remove(addr)  #removing the user from connectedIP list. 


            if commandmsg[0] == START_GAME: #start_game username numUsers
                if(len(connectedIP) <= int(commandmsg[2])):
                    conn.send("FAILURE Required number of users not present".encode(FORMAT))
                elif(commandmsg[2] >= 4 or commandmsg[2] <= 1):
                    conn.send("FAILURE Number of users not possible".encode(FORMAT))
                elif(commandmsg[1] in connectedIP):
                    conn.send(startGame().encode(FORMAT))
                else:
                    conn.send("FAILURE".encode(FORMAT))


            if commandmsg[0] == QUERYP_MESSAGE:
                conn.send(queryPlayers().encode(FORMAT))
            
            if commandmsg[0] == QUERYG_MESSAGE:
                conn.send(queryGames().encode(FORMAT))

            print(f"[{addr[2]}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    conn.close()
        
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER} {PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_Count() - 1}")
        
def startGame():
    msg = ""
    msg += "Game identifier" + game_identifier 
    games += 1
    for i in connectedIP:
        msg += str(i) + "\n"
    return msg


def queryPlayers():
    count = 0
    msg = ""
    for i in connectedIP:
        count+= 1
        msg += str(i) + "\n"

    return msg

def send(msg, socket):
    encodedMessage = bytes(msg, 'utf-8')
    socket.sendall(encodedMessage)

def queryGames():
    return "List of Games and Users playing in games: " + str(len(games)) # will return 0 since start games has not been implemented yet. 



print("[STARTING] Server is starting...")
start()