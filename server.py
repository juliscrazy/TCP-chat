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
        sent = False
        while sent == False:
            try:
                i.send(data)
                sent = True
            except OSError:
                clientList.remove(i)

def clientHandler(conn):
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        printdata=data.decode("utf-8")
        print("received data:", printdata, conn.getpeername())
        if printdata == "end":
            data = b'end'
            conn.send(data)  # echo
            conn.close()
            break
        else:
            sendAll(data)

while True:
    conn, addr = s.accept()
    print('New Client | Connection address:', addr)
    thread.start_new_thread(clientHandler, (conn,))
    clientList.append(conn)