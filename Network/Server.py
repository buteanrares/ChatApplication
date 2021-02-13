import socket
import threading
from Domain.User import User
import pyaudio


# Audio constants 
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096

class Server:
    def __init__(self):
        # Constructor
        super().__init__()
        self.ip = ""
        self.port = 7776
        self.socket = None
        self.users = {}
        self.pyaudio = pyaudio.PyAudio()
        self.audioStream=None


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
            textSocket, clientAddress = self.socket.accept()
            audioSocket, clientAddress = self.socket.accept()
            print("[%s:%s] has connected." % clientAddress)
            threading.Thread(target=self.__handleClient,
                             args=(textSocket, audioSocket, clientAddress)).start()


    def __handleClient(self, textSocket, audioSocket, clientAddress):
        user = User(None, textSocket, audioSocket, clientAddress)
        user.getTextSocket().send(bytes("You have joined the server. Type '/quit' to exit.\n", "utf8"))
        user.getTextSocket().send(bytes("Type your name below:", "utf8"))
        name = user.getTextSocket().recv(1024).decode("utf8")
        user.setName(name)
        self.users[name] = user

        message = "%s has joined the chat!" % user.getName()
        self.__broadcast(bytes(message, "utf8"), target="global")
        while True:
            msg = user.getTextSocket().recv(1024)
            if msg != bytes("/quit", "utf8"):
                self.__broadcast(msg, user.getName())
            else:
                user.getTextSocket().send(bytes("Goodbye.", "utf8"))
                user.getTextSocket().close()
                del self.users[user.getName()]
                self.__broadcast(
                    bytes("%s has left the server." % user.getName(), "utf8"))
                break


    def __broadcast(self, msg, sender=None, target=None):
        for user in self.users.values():
            if (user.getName() != sender and target == None):
                user.getTextSocket().send(bytes(sender + ": ", "utf8") + msg)
            elif target == "global":
                user.getTextSocket().send(msg)


    def startRecording(self):
        self.audioStream = self.pyaudio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK, stream_callback=self.sendAudio)


    def sendAudio(self, in_data, frame_count, time_info, status):
        for user in self.users.values():
            user.getAudioSocket().send(in_data)
        return (None,pyaudio.paContinue)


    def start(self):
        # Functia principala - creaza si porneste thread-ul pt fiecare client nou conectat

        self.__setup()
        self.socket.listen(5)
        print("\nWaiting for clients...")

        self.startRecording()

        accept_thread = threading.Thread(
            target=self.__acceptIncomingConnections)
        
        accept_thread.start()
        accept_thread.join()
        self.socket.close()
