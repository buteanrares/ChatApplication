import socket
import threading

class TextSocket:
    def __init__(self,ADDR) -> None:
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect(ADDR)
        self.sendText_thread = None
        self.receiveText_thread = None


    def sendText(self):
        while True:
            print("Response: ", end="")
            msg = input()
            self.clientSocket.send(msg.encode())
    
    def receiveText(self):
        while True:
            recvMsg = self.clientSocket.recv(1024)
            recvMsg = recvMsg.decode()
            print(recvMsg)

    def startTextThreads(self):
        self.sendText_thread = threading.Thread(target=self.handleSend)
        self.receiveText_thread = threading.Thread(target=self.handleReceiveText)

        self.sendText_thread.start()
        self.receiveText_thread.start()

    def stopTextThreads(self):
        self.sendText_thread.join()
        self.receiveText_thread.join()