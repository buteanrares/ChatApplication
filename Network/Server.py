import socket
import threading


class Server:
    def __init__(self):
        # Constructor

        super().__init__()
        self.ip = '127.0.0.1'
        self.port = 55555
        self.socket=None


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


    def __handleClient(self, connectionSocket, clientAddress):
        """Handles the connection with a client.

        :param connectionSocket: contains the connection with the client
        :type connectionSocket: socket
        :param clientAddress: contains client's information
        :type clientAddress: tuple. [0]:ip  [1]:port
        """

        print("New connection with [" + str(clientAddress[0]) + ":" + str(clientAddress[1])+"]")
        msg = "\nTo disconnect, type !disconnect.\nSend some numbers (separated by space): "
        connectionSocket.send(msg.encode())
        while True:
            clientMessage = connectionSocket.recv(1024)
            clientMessage = clientMessage.decode()
            if clientMessage == "!disconnect":
                connectionSocket.send("Goodbye!".encode())
                connectionSocket.close()
                print("Connection ended with [" + str(clientAddress[0]) + ":" + str(clientAddress[1])+"]")
                break
            else:
                print(clientAddress[0] + ":" + str(clientAddress[1]) + " sent: " + clientMessage)


    def start(self):
        # Functia principala - creaza si porneste thread-ul pt fiecare client nou conectat

        self.__setup()
        
        self.socket.listen(5)
        print("\nWaiting for clients...")
        while True:
            # Acceptare conexiune si creare socket
            connectionSocket, clientAddress = self.socket.accept()
            thread = threading.Thread(target=self.__handleClient, args=(connectionSocket, clientAddress))
            thread.start()
            print("Active connections: " + str(threading.activeCount() - 1))

