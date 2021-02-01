class User:
    
    def __init__(self,username,socket):
        super().__init__()
        self.username = username
        self.socket = socket
    
    def getUsername(self):
        return self.username

    def getSocket(self):
        return self.socket

    def setSocket(self, newSocket):
        this.socket = newSocket

    def sendMessage(self, message):
        # TODO
        pass

    def __loadChat(self):
        # TODO - loading should pe client-side, recieving from server
        pass

    def __saveChat(self):
        # TODO - saving should be server-side
        pass
