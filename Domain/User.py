class User:
    def __init__(self, name, socket, address):
        super().__init__()
        self.name = name
        self.socket = socket

    def getName(self):
        return self.name

    def getSocket(self):
        return self.socket

    def getAddress(self):
        return self.address

    def setSocket(self, newSocket):
        self.socket = newSocket

    def setName(self, newName):
        self.name = newName

    def startConnection(self, ip):
        # TODO
        pass

    def sendMessage(self, message):
        # TODO
        pass

    def __loadChat(self):
        # TODO - loading should pe client-side, recieving from server
        pass

    def __saveChat(self):
        # TODO - saving should be server-side
        pass
