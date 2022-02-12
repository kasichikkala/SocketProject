from concurrent.futures import thread
import socket 
import threading

HEADER = 64
PORT = 41001
SERVER = "10.120.70.145" #running manager on general4.asu.edu
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
QUERYP_MESSAGE = "QUERYP"
QUERYG_MESSAGE = "QUERYG"


connectedIP = []
names = []
uCount = 0
games = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDR)

def handle_client(conn, addr):
    count = 0
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if(count == 0):
                
                addr = addr + (msg,)
                connectedIP.append(addr)
                print(addr)
                count+=1
                

            
            if msg == DISCONNECT_MESSAGE:
                #connectedIP.pop(int(addr[3]))
                connected = False
                print(f"{addr[2]} has left the game!")
                connectedIP.remove(addr)  


            if msg == QUERYP_MESSAGE:
                queryPlayers()
            
            if msg == QUERYG_MESSAGE:
                queryGames()

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
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        


def queryPlayers():
    count = 0
    for i in connectedIP:
        count+= 1

        print(str(i[2]) + ": " + "IP " + str(count) + ": " + str(i[0]) + " Port: " + str(i[1]))

def queryGames():
    print("List of Games and Users playing in games: " + str(len(games)))

print("[STARTING] server is starting...")
start()
