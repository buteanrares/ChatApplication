import socket


class Connection:
    def __init__(self, clientSocket1: socket, clientAddress1: tuple,
                 clientSocket2: socket, clientAddress2: tuple):
        super().__init__()
        self.clientSocket1 = clientSocket1
        self.clientAddress1 = clientAddress1
        self.clientSocket2 = clientSocket2
        self.clientAddress2 = clientAddress2

    @DeprecationWarning  #no point using
    def sendMessage(self, message, clientNumber=None):
        if clientNumber == None:
            raise ValueError("clientNumber must be '1' or '2' (int)")
        if clientNumber == 1:
            self.clientSocket1.send(message)
        if clientNumber == 2:
            self.clientSocket2.send(message)

    def getClientSocket1(self):
        return self.clientSocket1

    def getClientSocket2(self):
        return self.clientSocket2

    def getClientAddress1(self):
        return self.clientAddress1

    def getClientAddress2(self):
        return self.clientAddress2
