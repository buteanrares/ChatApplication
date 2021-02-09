import socket
import threading
from Domain import User


class Server:
    def __init__(self):
        # Constructor
        super().__init__()
        self.ip = ""
        self.port = 7777
        self.socket = None
        self.users = {}

    def __setup(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.port))

    def getSocket(self):
        return self.socket

    def getIP(self):
        """Getter for the IP attribute

        :return: IP
        :rtype: string
        """
        return self.ip

    def getPort(self):
        """Getter for the port attribute

        :return: port
        :rtype: int
        """
        return self.port

    def __acceptIncomingConnections(self):
        while True:
            clientSocket, clientAddress = self.socket.accept()
            print("[%s:%s] has connected." % clientAddress)
            threading.Thread(target=self.__handleClient,
                             args=(clientSocket, clientAddress)).start()

    def __handleClient(self, clientSocket, clientAddress):
        user = User(None, clientSocket, clientAddress)
        user.getSocket().send(
            bytes("You have joined the server. Type '/quit' to exit.\n",
                  "utf8"))
        user.getSocket().send(bytes("Type your name below:", "utf8"))
        name = user.getSocket().recv(1024).decode("utf8")
        user.setName(name)
        self.users[name] = user

        message = "%s has joined the chat!" % user.getName()
        self.__broadcast(bytes(message, "utf8"), target="global")
        while True:
            msg = user.getSocket().recv(1024)
            if msg != bytes("/quit", "utf8"):
                self.__broadcast(msg, user.getName())
            else:
                user.getSocket().send(bytes("Goodbye.", "utf8"))
                user.getSocket().close()
                del self.users[user.getName()]
                self.__broadcast(
                    bytes("%s has left the server." % user.getName(), "utf8"))
                break

    def __broadcast(self, msg, sender=None, target=None):
        for user in self.users.values():
            if (user.getName() != sender and target == None):
                user.getSocket().send(bytes(sender + ": ", "utf8") + msg)
            elif target == "global":
                user.getSocket().send(msg)

    def start(self):
        # Functia principala - creaza si porneste thread-ul pt fiecare client nou conectat

        self.__setup()
        self.socket.listen(5)
        print("\nWaiting for clients...")
        accept_thread = threading.Thread(
            target=self.__acceptIncomingConnections)
        accept_thread.start()
        accept_thread.join()
        self.socket.close()
