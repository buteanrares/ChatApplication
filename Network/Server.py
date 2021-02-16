import socket
import threading
from Domain.User import User


TEXTADDR=("",7777)
AUDIOADDR=("",7778)

class Server:
    def __init__(self):
        # Constructor
        super().__init__()
        self.audioConnections=[]
        self.users = {}
        self.TextSocket=None
        self.AudioSocket=None


    def setup(self):
        self.TextSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.TextSocket.bind(TEXTADDR)

        self.AudioSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.AudioSocket.bind(AUDIOADDR)


    #
    # AUDIO HANDLING
    #

    def acceptAudioConnections(self):
        self.AudioSocket.listen(100)
        while True:
            c, addr = self.AudioSocket.accept()
            print("New AUDIO socket connection")
            self.audioConnections.append(c)
            threading.Thread(target=self.handleClientAudio,args=(c,addr,)).start()


    def broadcastAudio(self, sock, data):
        for client in self.audioConnections:
            if client != self.AudioSocket and client != sock:
                try:
                    client.send(data)
                except:
                    pass


    def handleClientAudio(self,c,addr):
        while True:
            data = c.recv(4096)
            self.broadcastAudio(c, data)
    
    #
    #


    #
    # TEXT HANDLING
    #

    def acceptTextConnections(self):
        self.TextSocket.listen(100)
        while True:
            textSocket, clientAddress = self.TextSocket.accept()
            print("New TEXT socket connection")
            print("[%s:%s] has connected." % clientAddress)
            threading.Thread(target=self.handleClientText, args=(textSocket, clientAddress)).start()


    def handleClientText(self, textSocket, clientAddress):
        user = User(None, textSocket, None, clientAddress)
        user.getTextSocket().send(bytes("You have joined the server. Type '/quit' to exit.\n", "utf8"))
        user.getTextSocket().send(bytes("Type your name below:", "utf8"))
        name = user.getTextSocket().recv(1024).decode("utf8")
        user.setName(name)
        self.users[name] = user

        message = "%s has joined the chat!" % user.getName()
        self.broadcastText(bytes(message, "utf8"), target="global")
        while True:
            msg = user.getTextSocket().recv(1024)
            if msg != bytes("/quit", "utf8"):
                self.broadcastText(msg, user.getName())
            else:
                user.getTextSocket().send(bytes("Goodbye.", "utf8"))
                user.getTextSocket().close()
                del self.users[user.getName()]
                self.broadcastText(
                    bytes("%s has left the server." % user.getName(), "utf8"))
                break


    def broadcastText(self, msg, sender=None, target=None):
        for user in self.users.values():
            if (user.getName() != sender and target == None):
                user.getTextSocket().send(bytes(sender + ": ", "utf8") + msg)
            elif target == "global":
                user.getTextSocket().send(msg)

    #
    #


    def start(self):
        self.setup()
        print("\nWaiting for clients...")
        threading.Thread(target=self.acceptTextConnections).start()
        threading.Thread(target=self.acceptAudioConnections).start()
        