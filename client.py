import socket
from threading import Thread
from tkinter import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "127.0.0.1"
port = 8000
client.connect((ip, port))

class gui:
    def __init__(self):
        self.window = Tk()
        self.window.withdraw()
        self.login = Toplevel()
        self.login.geometry('400x300')
        self.login.title('Login')
        self.login.resizable(width = False, height = False)
        self.heading = Label(self.login, text = "Please login to continue", font = ("Arial", 15))
        self.heading.place(x = 90, y = 10)
        self.nickname = Label(self.login, text = 'Your Nickname:', font = ("Arial", 10))
        self.nickname.place(x = 50, y = 90)
        self.nameEntry = Entry(self.login, text = "", width = 27, bd = 3)
        self.nameEntry.place(x = 150, y = 90)
        self.enter = Button(self.login, text = "Log In", fg = "black", bg = "#87a9d6", command = lambda:self.signin(self.nameEntry.get()))
        self.enter.place(x = 170, y = 130)
        self.window.mainloop()

    def signin(self, name):
        self.login.destroy()
        
        self.layout(name)

        chatThread = Thread(target = self.receive)
        chatThread.start()

    def layout(self, name):
        self.name = name
        self.window.deiconify()
        self.window.title("chat")
        self.window.config(width = 470, height = 570, bg = "#17202A")
        self.window.resizable(width = False, height = False)

        self.header = Label(self.window, text = self.name, bg = "#17202A", fg = "#EAECEE", font = ("Arial", 15), pady = 5)
        self.header.place(relwidth = 1)
        self.line = Label(self.window, width = 450, bg = "#ABB2B9")
        self.line.place(relwidth = 1, relheight = 0.012, rely = 0.07)
        self.chats = Text(self.window, width = 20, height = 2, bg = "#17202A", fg = "#EAECEE", font = ("Arial, 20"), padx = 5, pady = 5)
        self.chats.place(relheight = 0.745, relwidth = 1, rely = 0.08)
        self.chats.config(cursor = "arrow")
        scrollbar = Scrollbar(self.chats)
        scrollbar.place(relheight = 1, relx = 0.974)
        scrollbar.config(command = self.chats.yview)
        self.chats.config(state = DISABLED)
        self.frame = Label(self.window, bg = "#ABB2B9", height = 80)
        self.frame.place(relwidth = 1, rely = 0.825)
        self.input = Entry(self.frame, text = "", bg = "#2C3E50", fg = "#EAECEE", font = ("Times New Roman", 10))
        self.input.place(relwidth = 0.74, relheight = 0.06, relx = 0.011, rely = 0.008)
        self.input.focus()
        self.send = Button(self.frame, text = "Send", width = 20, bg = "#ABB2B9", command = lambda:self.sendButton(self.input.get()))
        self.send.place(relwidth = 0.22, relheight = 0.06, relx = 0.77, rely = 0.008)

    def sendButton(self,text):
        self.chats.config(state = DISABLED)
        self.msg = text
        self.input.delete(0, END)
        thread1 = Thread(target = self.write)
        thread1.start()

    def write(self):
        self.chats.config(state = DISABLED)
        while True:
            msg = (f"{self.name}: {self.msg}")
            client.send(msg.encode("utf-8"))
            self.showMessage(msg)
            break

    def showMessage(self, msg):
        self.chats.config(state = NORMAL)
        self.chats.insert(END, msg + "\n")
        self.chats.config(state = DISABLED)
        self.chats.see(END)

    def receive(self):
        while True:
            try:
                msg = client.recv(2048).decode("utf-8")
                if msg == 'nickname':
                    client.send(self.name.encode('utf-8'))
                else:
                    self.showMessage(msg)
            except:
                print("Error")
                client.close()
                break

g = gui()

#thread1 = Thread(target = receive)
#thread1.start()
#thread2 = Thread(target = write)
#thread2.start()