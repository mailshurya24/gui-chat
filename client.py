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
        self.enter = Button(self.login, text = "Log In", fg = "black", bg = "#87a9d6", command = self.signin(self.nameEntry.get()))
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

    def receive(self):
        while True:
            try:
                msg = client.recv(2048).decode("utf-8")
                if msg == 'nickname':
                    client.send(self.name.encode('utf-8'))
                else:
                    print(msg)
            except:
                print("Error")
                client.close()
                break

    



#def write():
 #   while True:
  #      msg = nickname + ": " + input("")
   #     client.send(msg.encode("utf-8"))

g = gui()

#thread1 = Thread(target = receive)
#thread1.start()
#thread2 = Thread(target = write)
#thread2.start()