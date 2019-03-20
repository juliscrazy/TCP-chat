import socket
import tkinter as tk
from tkinter import scrolledtext
import threading as thread

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

class App:

    def __init__(self):
        self.stop = 0
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((TCP_IP, TCP_PORT))
        self.msgListener = thread.Thread(target=self.listenForMessages)
        self.msgListener.start()
        self.main()

    def closeApp(self):
        #shuts down server and 
        self.s.send(b'end')
        self.root.destroy()
        self.stop = 1

    def sendTextMessage(self, message):
        message = bytes(message, "utf-8")
        self.s.send(message)
        self.chatEntry.delete(0, "end")

    def listenForMessages(self):
        while self.stop == 0:
            data = self.s.recv(BUFFER_SIZE)
            data=data.decode("utf-8")
            if data == "":
                pass
            elif data == "end":
                break
            else:
                oldData = self.chatWindow.cget("text")
                newData = oldData + "\n" + data
                self.chatWindow.configure(text=newData)
                print(data)

    def main(self):
        self.root = tk.Tk()
        self.root.configure(bg="#444444")
        self.root.geometry("350x300")
        self.root.iconbitmap('icon.ico')
        self.root.title("Chat Client")
        self.root.resizable(0,0)
        self.chatEntry = tk.Entry(self.root, relief="flat", bg="#222222",fg="#DDDDDD", width=350)
        self.chatEntry.pack(side=tk.BOTTOM)
        self.chatWindow = tk.Label(self.root, relief="flat", bg="#333333",fg="#DDDDDD", width=350, height=80, anchor=tk.NW, justify=tk.LEFT)
        self.chatWindow.pack(side=tk.TOP, fill=tk.BOTH)
        self.root.protocol("WM_DELETE_WINDOW", self.closeApp)
        self.root.bind('<KeyPress-Return>', (lambda event: self.sendTextMessage(self.chatEntry.get())))
        self.root.mainloop()


if __name__ == "__main__":
    app = App()