import socket
import _thread as thread

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(10)

clientList = []

def sendAll(data):
    global clientList
    for i in clientList:
        try:
            i.send(data)
        except OSError:
            clientList.remove(i)

def clientHandler(conn):
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        printdata=data.decode("utf-8")
        clientName = conn.getpeername()
        print("received data:", printdata, clientName[1])
        if printdata == "end":
            data = b'end'
            conn.send(data)  # echo
            conn.close()
            break
        else:
            bname = bytes(str(clientName[1]), "utf-8")
            data = bname + b": " + data
            sendAll(data)

while True:
    conn, addr = s.accept()
    print('New Client | Connection address:', addr)
    thread.start_new_thread(clientHandler, (conn,))
    clientList.append(conn)