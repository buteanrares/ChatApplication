import socket
import threading
from Domain.User import User


TEXTADDR=("",7777)
AUDIOADDR=("",7778)

class Server:
    # Server class

    def __init__(self):
        # Constructor
        super().__init__()
        self.audioConnections=[]
        self.users = {}
        self.TextSocket=None     # Socket holding text transfer
        self.AudioSocket=None    # Socket holding audio transfer


    def setup(self):
        # Server setup
        self.TextSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.TextSocket.bind(TEXTADDR)

        self.AudioSocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.AudioSocket.bind(AUDIOADDR)


    #
    # AUDIO HANDLING
    #

    def acceptAudioConnections(self):
        # Starts accepting new audio connections and forwards them to client handlers.

        self.AudioSocket.listen(100)
        while True:
            c, addr = self.AudioSocket.accept()
            self.audioConnections.append(c)
            threading.Thread(target=self.handleClientAudio,args=(c,addr,)).start()


    def broadcastAudio(self, sock, data):
        # Broadcasts audio message to every client in the server, except the sender
        for client in self.audioConnections:
            if client != self.AudioSocket and client != sock:
                try:
                    client.send(data)
                except:
                    pass


    def handleClientAudio(self,c,addr):
        # Receives and forwards audio message to broadcast method
        # TO BE USED WITH A THREAD

        while True:
            data = c.recv(4096)
            self.broadcastAudio(c, data)
    

    #
    # TEXT HANDLING
    #

    def acceptTextConnections(self):
        # Starts accepting new text connections and forwards them to client handlers.

        self.TextSocket.listen(100)
        while True:
            textSocket, clientAddress = self.TextSocket.accept()
            print("[%s:%s] has connected." % clientAddress)
            threading.Thread(target=self.handleClientText, args=(textSocket, clientAddress)).start()


    def handleClientText(self, textSocket, clientAddress):
        # Requests a name from a new client and handles text messaging
        # TO BE USED WITH A THREAD

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
        # Broadcasts a text message to all connected clients
        # :param: target (string): None or "global" ; global - to everyone / None - to everyone except sender
        for user in self.users.values():
            if (user.getName() != sender and target == None):
                user.getTextSocket().send(bytes(sender + ": ", "utf8") + msg)
            elif target == "global":
                user.getTextSocket().send(msg)

    #
    #


    def start(self):
        # Server startup

        self.setup()
        print("\nWaiting for clients...")
        threading.Thread(target=self.acceptTextConnections).start()
        threading.Thread(target=self.acceptAudioConnections).start()



server = Server()
server.start()
