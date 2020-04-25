import socket
from _thread import *
import sys


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

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


pos = [(0,0), (100,100)]
def threaded_client(conn, player):

    conn.send(str.encode(make_pos(pos[player])))
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(package_size).decode())
            pos[player] = data

            if not data:
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                print("Received: ", data)
                print("Sending : ", reply)

            conn.sendall(str.encode(make_pos(reply)))
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