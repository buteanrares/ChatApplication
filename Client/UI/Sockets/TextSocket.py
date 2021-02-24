import socket
import threading

class TextSocket:
    # Text socket class

    def __init__(self,ADDR) -> None:
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect(ADDR)
        
        self.sendText_thread = threading.Thread(target=self.sendText).start()
        self.receiveText_thread = threading.Thread(target=self.receiveText).start()


    def sendText(self):
        # Sends text data to server

        while True:
            print("Response: ", end="")
            msg = input()
            self.socket.send(msg.encode())
    

    def receiveText(self):
        # Receives text data from server

        while True:
            recvMsg = self.socket.recv(1024)
            recvMsg = recvMsg.decode()
            print(recvMsg)