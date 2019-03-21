import json
import socket
import threading as thread
import time
import tkinter as tk
from tkinter import scrolledtext

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
BUFFER_SIZE = 1024

class App:

    def __init__(self):
        self.stop = 0
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((TCP_IP, TCP_PORT))
        with open('clientData.json') as f:
            self.clientData = json.load(f)
        f.close()
        self.optnWindow = self.userOptionsWindow(self.clientData)
        self.s.send(bytes(str(self.clientData), "utf-8"))
        self.msgListener = thread.Thread(target=self.listenForMessages)
        self._guisetup()
        self.msgListener.start()
        self.root.mainloop()

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
        time.sleep(0.1)
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

    def _guisetup(self):
        #root config
        self.root = tk.Tk()
        self.root.configure(bg="#444444")
        self.root.geometry("350x300")
        self.root.iconbitmap('icon.ico')
        self.root.title("Chat Client - {0}".format(self.clientData["clientNick"]))
        ###self.root.resizable(0,0)
        self.root.option_add("*Font", self.clientData["clientFont"])
        #topbar
        self.navOptnBar = tk.Frame(self.root, bg="#444444", height=20, padx=2, pady=2)
        self.navOptnBar.pack(side=tk.TOP, fill=tk.X)
        self.userOptions = tk.Button(self.navOptnBar, command=(lambda: self.optnWindow.runwindow()),relief="flat", bg="#282828", fg="#DDDDDD", bd="0", text="Settings", padx=8, pady=2, activebackground="#444444", activeforeground="#FFFFFF")
        self.userOptions.pack(side=tk.LEFT)
        #entryline
        self.chatEntry = tk.Entry(self.root, relief="flat", bg="#222222", fg="#DDDDDD", insertbackground="#DDDDDD", width=350)
        self.chatEntry.pack(side=tk.BOTTOM, fill=tk.X)
        #chat history
        self.chatWindow = tk.Label(self.root, relief="flat", bg="#333333", fg="#DDDDDD", width=350, height=80, anchor=tk.SW, justify=tk.LEFT)
        self.chatWindow.pack(side=tk.TOP, fill=tk.BOTH)
        #binds
        self.root.protocol("WM_DELETE_WINDOW", self.closeApp)
        self.root.bind('<KeyPress-Return>', (lambda event: self.sendTextMessage(self.chatEntry.get())))

    class userOptionsWindow:

        def __init__(self, clientData):
            self.clientData = clientData

        def _guisetup(self):
            self.optns = tk.Tk()
            self.optns.configure(bg="#444444")
            self.optns.geometry("350x300")
            self.optns.iconbitmap('icon.ico')
            self.optns.resizable(0,0)
            self.optns.title("Settings - {0}".format(self.clientData["clientNick"]))
            self.optns.mainloop()

        def runwindow(self):
            self._guisetup()

if __name__ == "__main__":
    app = App()
