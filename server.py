import socket
import _thread as thread
import json

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(20)

clientList = []

def sendAll(data):
    global clientList
    for i in clientList:
        try:
            i.send(data)
        except OSError:
            clientList.remove(i)

def clientHandler(conn, clientData):
    global clientList
    #message handler
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        printdata=data.decode("utf-8")
        print("received data:", clientData["clientNick"], printdata)
        if "sys" in printdata:
            printdata = printdata[4:]
            if printdata == "end":
                data = b'end'
                conn.send(data)  # echo
                conn.close()
                clientList.remove(conn)
                print("dropped:", clientData["clientNick"])
                break
            elif "changed name to" in printdata: 
                bname = bytes(str(clientData["clientNick"]), "utf-8")
                bdata = bytes(printdata, "utf-8")
                data = bname + b" " + bdata
                sendAll(data)
                clientData["clientNick"] = conn.recv(BUFFER_SIZE).decode("utf-8")
        else:   
            bname = bytes(str(clientData["clientNick"]), "utf-8")
            data = bname + b": " + data
            sendAll(data)

while True:
    conn, addr = s.accept()
    print('New Client | Connection address:', addr)
    #user setup
    clientData = conn.recv(2000)
    clientData = clientData.decode("utf-8")
    clientData = json.loads(clientData.replace("'", "\""))
    clientList.append(conn)
    sendAll(bytes("{0} connected. Say Hi!".format(clientData["clientNick"]), "utf-8"))
    thread.start_new_thread(clientHandler, (conn, clientData))