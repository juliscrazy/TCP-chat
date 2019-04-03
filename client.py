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
        self.optnWindow = self.userOptionsWindow(self.clientData, self)
        self.s.send(bytes(str(self.clientData), "utf-8"))
        self.msgListener = thread.Thread(target=self.listenForMessages)
        self._guisetup()
        self.root.after(100, lambda: self.chatEntry.focus_force())
        self.msgListener.start()
        self.root.mainloop()

    def closeApp(self):
        #shuts down server and 
        self.s.send(b'sys end')
        self.root.destroy()
        self.stop = 1

    def reloadData(self):
            with open('clientData.json') as f:
                self.clientData = json.load(f)
            f.close()

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
                #oldData = self.chatWindow.cget("text")
                #newData = oldData + "\n" + data
                self.chatWindow.configure(state=tk.NORMAL)
                self.chatWindow.insert(tk.INSERT, "{0}\n".format(data))
                self.chatWindow.see(tk.END)
                self.chatWindow.configure(state=tk.DISABLED)
                #self.chatWindow.configure(text=newData)
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
        self.chatWindow = tk.scrolledtext.ScrolledText(self.root, relief="flat", bg="#333333", fg="#DDDDDD", width=350, height=80, wrap=tk.WORD) #anchor=tk.SW, justify=tk.LEFT
        self.chatWindow.pack(side=tk.TOP, fill=tk.BOTH)
        self.chatWindow.vbar.pack_forget() #epic invisible scrollbar cus styles are a pain
        #binds
        self.root.protocol("WM_DELETE_WINDOW", self.closeApp)
        self.root.bind('<KeyPress-Return>', (lambda event: self.sendTextMessage(self.chatEntry.get())))

    class userOptionsWindow:

        def __init__(self, clientData, parent):
            self.clientData = clientData
            self.parent = parent

        def storeSettings(self, NickName, Font, FontSize):
            with open('clientData.json') as f:
                clientData = json.load(f)
                f.close()
            clientData["clientNick"] = NickName
            clientData["clientFont"] = "{0} {1}".format(Font, FontSize)
            with open('clientData.json', "w") as f:
                json.dump(clientData, f)
                f.close()
        
        def safe(self):
            self.storeSettings(self.NickEntry.get(), self.FontEntry.get(), self.FontSizeEntry.get())
            self.optns.destroy()
            self.parent.reloadData()
            self.clientData = self.parent.clientData
            self.parent.root.option_add("*Font", self.clientData["clientFont"])
            self.parent.root.title("Chat Client - {0}".format(self.clientData["clientNick"]))
            self.parent.sendTextMessage("sys changed name to {0}".format(self.clientData["clientNick"]))
            self.parent.sendTextMessage(self.clientData["clientNick"])

        def _guisetup(self):
            #window setup
            self.optns = tk.Tk()
            self.optns.configure(bg="#444444")
            self.optns.geometry("350x150")
            self.optns.iconbitmap('icon.ico')
            self.optns.resizable(0,0)
            self.optns.configure(padx=5, pady=5)
            self.optns.title("Settings - {0}".format(self.clientData["clientNick"]))
            #client Options
            self.NickFrame = tk.Frame(self.optns, bg="#222222") #nickname
            self.NickFrame.pack(side=tk.TOP)
            self.NickEntryLabel = tk.Label(self.NickFrame, text="Name:",bg="#222222",fg="#DDDDDD")
            self.NickEntryLabel.pack(side=tk.LEFT)
            self.NickEntry = tk.Entry(self.NickFrame, relief="flat", bg="#222222", fg="#DDDDDD", insertbackground="#DDDDDD", width=40)
            self.NickEntry.pack(side=tk.LEFT)
            self.spacer1 = tk.Text(self.optns, bg="#444444", height="1",width="1",relief="flat", font=("Helvetica", 1))
            self.spacer1.pack()
            self.FontFrame = tk.Frame(self.optns, bg="#222222") #font
            self.FontFrame.pack(side=tk.TOP)
            self.FontEntryLabel = tk.Label(self.FontFrame, text="Font: ",bg="#222222",fg="#DDDDDD")
            self.FontEntryLabel.pack(side=tk.LEFT)
            self.FontEntry = tk.Entry(self.FontFrame, relief="flat", bg="#222222", fg="#DDDDDD", insertbackground="#DDDDDD", width=41)
            self.FontEntry.pack(side=tk.LEFT)
            self.spacer2 = tk.Text(self.optns, bg="#444444", height="1",width="1",relief="flat", font=("Helvetica", 1))
            self.spacer2.pack()
            self.FontSizeFrame = tk.Frame(self.optns, bg="#222222") #font size
            self.FontSizeFrame.pack(side=tk.TOP)
            self.FontSizeLabel = tk.Label(self.FontSizeFrame, text="Font Size:",bg="#222222",fg="#DDDDDD")
            self.FontSizeLabel.pack(side=tk.LEFT)
            self.FontSizeEntry = tk.Entry(self.FontSizeFrame, relief="flat", bg="#222222", fg="#DDDDDD", insertbackground="#DDDDDD", width=38)
            self.FontSizeEntry.pack(side=tk.LEFT)
            self.spacer1 = tk.Text(self.optns, bg="#444444", height="1",width="1",relief="flat", font=("Helvetica", 1))
            self.spacer1.pack()
            #Fill in previous
            self.NickEntry.insert(0, self.clientData["clientNick"])
            clientFontPrev = self.clientData["clientFont"].split(" ")
            clientFontSizePrev = clientFontPrev[1]
            clientFontPrev = clientFontPrev[0]
            self.FontEntry.insert(0, clientFontPrev)
            self.FontSizeEntry.insert(0, clientFontSizePrev)
            #Save Button
            self.SaveButton = tk.Button(self.optns, command=lambda: self.safe(),relief="flat", bg="#282828", fg="#DDDDDD", bd="0", text="Save",
                                        padx=8, pady=2, activebackground="#444444", activeforeground="#FFFFFF")
            self.SaveButton.pack()

        def runwindow(self):
            self._guisetup()
            self.optns.after(20, lambda: self.NickEntry.focus_force()) #put focus on nickname
            self.optns.after(20, lambda: self.optns.geometry("")) #this line gives me the creeps
            self.optns.mainloop()

if __name__ == "__main__":
    app = App()
