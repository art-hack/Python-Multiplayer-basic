import socket
from _thread import *
import sys

server = "172.22.45.173"
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


def read_pos(stra):
    stra = stra.split(",")
    # print(stra)
    return int(stra[0]), int(stra[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


pos = [(0, 0), (100, 100)]


def thread_client(conn, player):
    conn.send(str.encode(make_pos(pos[player])))
    print("started")
    reply = ""
    while True:
        try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data

            # if not data:
            #     print("Disconnected")
            #     break
            # else:
            # print("hua")
            if player == 1:
                reply = pos[0]
            else:
                reply = pos[1]
            # print("ye bhi")
            print("Received: " + str(data))
            print("Sending: " + str(reply))

            conn.sendall(str.encode(make_pos(reply)))

        except:
            break
    print("Lost Connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("connected to: ", str(addr))

    start_new_thread(thread_client, (conn, currentPlayer))
    currentPlayer += 1
