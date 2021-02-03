import socket
import threading


class Server:
    def __init__(self):
        # Constructor
        super().__init__()
        self.ip = "127.0.0.1"
        self.port = 55555
        self.socket = None
        self.clients = {}
        self.addresses = {}

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
            client, clientAddress = self.socket.accept()
            print("[%s:%s] has connected." % clientAddress)
            client.send(
                bytes("Hello. This is the server.\nType your name!", "utf8"))
            self.addresses[client] = clientAddress
            threading.Thread(target=self.__handleClient,
                             args=(client, )).start()

    def __handleClient(self, client):
        name = client.recv(1024).decode("utf8")
        client.send(
            bytes("You have joined the server. Type '/quit' to exit.", "utf8"))
        message = "%s has joined the chat!" % name
        self.__broadcast(bytes(message, "utf8"))
        self.clients[client] = name
        while True:
            msg = client.recv(1024)
            if msg != bytes("/quit", "utf8"):
                self.__broadcast(msg, name + ": ")
            else:
                client.send(bytes("Goodbye.", "utf8"))
                client.close()
                del self.clients[client]
                self.__broadcast(
                    bytes("%s has left the server." % name, "utf8"))
                break

    def __broadcast(self, msg, prefix=""):
        for sock in self.clients:
            sock.send(bytes(prefix, "utf8") + msg)

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
