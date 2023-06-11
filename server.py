import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "127.0.0.1"
port = 8000
server.bind((ip,port))
server.listen()

clients = []
nicknames = []

def removeClients(c):
    if c in clients:
        clients.remove(c)

def removeNicknames(n):
    if n in nicknames:
        nicknames.remove(n)

def broadcast(m, c):
    for i in clients:
        if i != c:
            try: 
                i.send(m.encode("utf-8"))
            except:
                removeClients(i)

def clientThread(c1, addr):
    c1.send("Welcome to the chatroom!".encode("utf-8"))

    while True:
        try:
            msg = c1.recv(2048).decode("utf-8")

            if msg:
                print(msg)
                broadcast(msg, c1)
            else:
                removeClients(c1)
                removeNicknames(nickname)
        except:
            continue

while True: 
    c1, addr = server.accept()
    c1.send('nickname'.encode("utf-8"))
    nickname = c1.recv(2048).decode("utf-8")
    clients.append(c1)
    nicknames.append(nickname)
    msg = nickname + " joined."
    print(msg)
    broadcast(msg, c1)
    thread1 = Thread(target = clientThread, args = (c1, nickname))
    thread1.start()