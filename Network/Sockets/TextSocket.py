import socket
import threading

class TextSocket:
    def __init__(self,ADDR) -> None:
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect(ADDR)
        
        self.sendText_thread = threading.Thread(target=self.sendText).start()
        self.receiveText_thread = threading.Thread(target=self.receiveText).start()


    def sendText(self):
        while True:
            #print("TEXT SEND WORKING")
            print("Response: ", end="")
            msg = input()
            self.socket.send(msg.encode())
    

    def receiveText(self):
        while True:
            #print("TEXT RECEIVE WORKING")
            recvMsg = self.socket.recv(1024)
            recvMsg = recvMsg.decode()
            print(recvMsg)