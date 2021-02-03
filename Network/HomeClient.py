import threading
import socket


def handleSeding():
    while True:
        msg = input("Response: ")
        clientSocket.send(msg.encode())


def handleReceiving():
    while True:
        recvMsg = clientSocket.recv(1024)
        recvMsg = recvMsg.decode()
        print(recvMsg)


# Creare socket TCP
ADDR = ("127.0.0.1", 55555)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(ADDR)

threading.Thread(target=handleSeding).start()
threading.Thread(target=handleReceiving).start()
