import socket
import _thread as thread
import json

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(20)

clientList = []
roomList = ["Room0"] #0 = general
Room0 = []

class backendCommands:
    def __init__(self):
        pass

    def message(self, messageData, conn, clientData, room):
        bname = bytes(str(clientData["clientNick"]), "utf-8")
        data = bname + b": " + bytes(" ".join(messageData), "utf-8")
        sendAll(data)
        return True

    def end(self, messageData, conn, clientData, room):
        global clientList
        data = b'end'
        conn.send(data)  # echo
        conn.close()
        clientList.remove(conn)
        bname = bytes(str(clientData["clientNick"]), "utf-8")
        sendAll(bname + b" disconnected")
        return False

    def changeName(self, messageData, conn, clientData, room):
        bname = bytes(str(clientData["clientNick"]), "utf-8")
        bdata = bytes(" ".join(messageData[0:]), "utf-8")
        data = bname + b" changed name to " + bdata
        sendAll(data)
        clientData["clientNick"] = conn.recv(BUFFER_SIZE).decode("utf-8")
        return True

    def newRoom(self, messageData, conn, clientData, room):
        i = len(roomList)
        i = "Room" + str(i+1)
        globals()[i] = []
        roomList.append(i)

    def joinRoom(self, messageData, conn, clientData, room):
        room.remove(conn)
        globals()[messageData[0]].append(conn)



BackendCommands = backendCommands()

def sendAll(data):
    global clientList
    for i in clientList:
        try:
            i.send(data)
        except OSError:
            clientList.remove(i)

def sendGroup(data):
    global roomList

def clientHandler(conn, clientData, room):
    #message handler
    room.append(conn)
    run = True
    while run:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        messageData=data.decode("utf-8")
        print("received data:", clientData["clientNick"], messageData)
        if "sys" in messageData:
            messageData = messageData[4:]
            messageData = messageData.split()
            run = getattr(BackendCommands, messageData[0])(messageData[1:], conn, clientData, room)
        else:
            pass
    print("dropped:", clientData["clientNick"])
            

while True:
    conn, addr = s.accept()
    print('New Client | Connection address:', addr)
    #user setup
    clientData = conn.recv(2000)
    clientData = clientData.decode("utf-8")
    clientData = json.loads(clientData.replace("'", "\""))
    clientList.append(conn)
    sendAll(bytes("{0} connected. Say Hi!".format(clientData["clientNick"]), "utf-8"))
    thread.start_new_thread(clientHandler, (conn, clientData, Room0))