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

def threaded_client(conn):

    conn.send(str.encode("Connected"))
    reply = ""
    while True:
        try:
            data = conn.recv(package_size)
            reply = data.decode(data_decode_format)

            if not data:
                print("Disconnected")
                break
            else:
                print("Received: ", reply)
                print("Sending : ", reply)

            conn.sendall(str.encode(reply))
        #Find out which error might occur and how to handle it
        except:
            break
    print("Lost connection")
    conn.close()



while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,))