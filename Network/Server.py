import socket
import threading
from Network.Connection import Connection


class Server:
    def __init__(self):
        # Constructor
        super().__init__()
        self.ip = "127.0.0.1"
        self.port = 55555
        self.socket = None
        self.connections = list()

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

    # def __startThreads(self, connection):
    #     threading.Thread(target=self.__handleMessagingForward,
    #                      args=(connection)).start()
    #     threading.Thread(target=self.__handleMessagingBackward,
    #                      args=(connection)).start()

    def __handleMessaging(self, connection):
        data, address = self.socket.recvfrom(1024)

        print("[" + address[0] + ":" + address[1] + "]: ", repr(data))

        if address[0] == connection.getClientAddress1[1] and address[
                1] == connection.getClientAddress1[1]:
            self.socket.sendto(data, (connection.getClientAddress2[0],
                                      connection.getClientAddress2[1]))

        if address[0] == connection.getClientAddress2[1] and address[
                1] == connection.getClientAddress2[1]:
            self.socket.sendto(data, (connection.getClientAddress1[0],
                                      connection.getClientAddress1[1]))

    # def __handleForwardMessage(self, message, receiver):
    #     # TODO: might need to add sender parameter
    #     self.socket.sendto(message.encode(), receiver)

    def start(self):
        # Functia principala - creaza si porneste thread-ul pt fiecare client nou conectat

        self.__setup()
        self.socket.listen(5)
        print("\nWaiting for clients...")
        while True:
            # Acceptare conexiune si creare socket
            connectionSocket1, clientAddress1 = self.socket.accept()
            print("New connection with [" + str(clientAddress1[0]) + ":" +
                  str(clientAddress1[1]) + "]")

            connectionSocket2, clientAddress2 = self.socket.accept()
            print("New connection with [" + str(clientAddress2[0]) + ":" +
                  str(clientAddress2[1]) + "]")

            connection = Connection(connectionSocket1, clientAddress1,
                                    connectionSocket2, clientAddress2)

            self.__handleMessaging(connection)

            print("Active connections: " + str(threading.activeCount() - 1))
