import socket
from _thread import *
import sys
from player import Player
import pickle

server = "192.168.254.11"
port = 5555
players = 2
package_size = 2048
data_decode_format = "utf-8"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

#argument limits connections
s.listen(players)
print("Waiting for a connection, Server Started")

players = [Player(0,0,50,50,(255,0,0)), Player(100,100,50,50, (0,0,255))]

def threaded_client(conn, player):

    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(package_size))
            players[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(pickle.dumps(reply))
        #Find out which error might occur and how to handle it
        except:
            break
    print("Lost connection")
    conn.close()


current_player = 0;
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1