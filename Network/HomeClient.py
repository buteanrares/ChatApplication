# Clientul trimite o lista de numere, serverul intoarce cel mai mare numar

import socket

def connect(clientSocket, ADDR):
    # Functia cu care clientul se conecteaza la server
    # Se ocupa de input - output cu serverul
    # @param clSocket (socket) : socketul creat pt conexiunea cu serverul
    # @param ADDR (tuple , constant) : tuplu cu adresa IP si portul pe care ruleaza
    # serverul

    clientSocket.connect(ADDR)
    recvMsg = clientSocket.recv(1024)
    recvMsg = recvMsg.decode()
    while True:
        msg = input("Response: ")
        clientSocket.send(msg.encode())
    print("Connection has been broken.")

# Creare socket TCP
ADDR = ("127.0.0.1", 7777)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connect(clientSocket, ADDR)
