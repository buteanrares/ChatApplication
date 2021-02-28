class User:
    def __init__(self, name, textSocket, audioSocket, address):
        super().__init__()
        self.name = name
        self.textSocket = textSocket
        self.audioSocket = audioSocket

    def getName(self):
        return self.name

    def getTextSocket(self):
        return self.textSocket

    def getAudioSocket(self):
        return self.audioSocket

    def setSocket(self, newSocket):
        self.socket = newSocket

    def setName(self, newName):
        self.name = newName

