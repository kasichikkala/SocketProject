from concurrent.futures import thread
from distutils import command
import socket
import sys 
import threading
import random

HEADER = 64
PORT = int(sys.argv[1])
SERVER = "10.120.70.145"#running manager on general4.asu.edu
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
START_GAME = "GAME"
DISCONNECT_MESSAGE = "DISCONNECT"
QUERYP_MESSAGE = "QUERYP"
QUERYG_MESSAGE = "QUERYG"


connectedIP = []

userNames = []
portNum = []
IPlist = []
flagGame = True

gameID = 0

players = []
names = []
uCount = 0
games = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDR)

# class Card(object):
#     def __init__(self, suit, val):
#         self.suit = suit
#         self.value = val

#     # Implementing build in methods so that you can print a card object
#     def __unicode__(self):
#         return self.show()
#     def __str__(self):
#         return self.show()
#     def __repr__(self):
#         return self.show()
        
#     def show(self):
#         if self.value == 1:
#             val = "Ace"
#         elif self.value == 11:
#             val = "Jack"
#         elif self.value == 12:
#             val = "Queen"
#         elif self.value == 13:
#             val = "King"
#         else:
#             val = self.value

#         return "{} of {}".format(val, self.suit)

# class Deck(object):
#     def __init__(self):
#         self.cards = []
#         self.build()

#     # Display all cards in the deck
#     def show(self):
#         for card in self.cards:
#             return card.show()

#     # Generate 52 cards
#     def build(self):
#         self.cards = []
#         for suit in ['Hearts', 'Clubs', 'Diamonds', 'Spades']:
#             for val in range(1,14):
#                 self.cards.append(Card(suit, val))

#     # Shuffle the deck
#     def shuffle(self, num=1):
#         length = len(self.cards)
#         for _ in range(num):
#             # This is the fisher yates shuffle algorithm
#             for i in range(length-1, 0, -1):
#                 randi = random.randint(0, i)
#                 if i == randi:
#                     continue
#                 self.cards[i], self.cards[randi] = self.cards[randi], self.cards[i]
#             # You can also use the build in shuffle method
#             # random.shuffle(self.cards)

#     # Return the top card
#     def deal(self):
#         return self.cards.pop()
# # class Player:
# #     def __init__(self, name, port):
# #         self.name = name
# #         self.port = port

# #     def __str__(self):
# #         return "Name: %s  Port: %s" % (self.name, self.port)

# #     def getName(self):
# #         return "%s" % (self.name)

def handle_client(conn, addr):
    count = 0
    print(f"[NEW CONNECTION] {addr} connected.")
    global gameID

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            commandmsg = msg.split(" ")
           
            if(commandmsg[0] == "register"): #register username IP port
                namemsg = commandmsg[1]
                userNames.append(namemsg)

                IPlist.append(addr[0])
                portNum.append(addr[1])
                
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
                userNames.remove(addr[2])
                connectedIP.remove(addr)  #removing the user from connectedIP list. 


            if commandmsg[0] == START_GAME: #start_game username numUsers
                if(len(connectedIP) <= int(commandmsg[2])):
                    conn.send("FAILURE Required number of users not present".encode(FORMAT))
                elif(int(commandmsg[2]) >= 4 or int(commandmsg[2]) <= 1):
                    conn.send("FAILURE Number of users not possible".encode(FORMAT))
                elif(commandmsg[1] in userNames):
                    #gameID += 1
                    #print(addr)
                    peerInfo = "Peer info: " +" -" + IPlist[0] + " -" + str(portNum[0])
                    # conn.send(addr[0].encode(FORMAT))
                    # conn.send(str(addr[1]).encode(FORMAT))
                    #conn.send(str(peerInfo).encode(FORMAT))
                    conn.send(str(peerInfo).encode(FORMAT) + " -".encode(FORMAT) + "\n".encode(FORMAT) + startGame().encode(FORMAT))
                else:
                    conn.send("FAILURE".encode(FORMAT))


            if commandmsg[0] == QUERYP_MESSAGE:
                conn.send(queryPlayers().encode(FORMAT))
            
            if commandmsg[0] == QUERYG_MESSAGE:
                conn.send(queryGames().encode(FORMAT))

            # if commandmsg[0] == "SEND":


            print(f"[{addr[2]}] {msg}")
            conn.send("Msg received by server".encode(FORMAT))

    conn.close()
        
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER} {PORT}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        
def startGame():
    global gameID
    msg = ""
    #msg += "Game identifier: " + str(gameID) + "\n"

    gameID += 1
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
    global gameID
    return "List of Games and Users playing in games: " + str(gameID) # will return 0 since start games has not been implemented yet. 

print("[STARTING] Server is starting...")
start()