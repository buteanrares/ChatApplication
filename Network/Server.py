import socket
import threading


def handleClient(connectionSocket, clientAddress):
    # Functia care se ruleaza cu fiecare client conectat
    # @param connectionSocket (socket) - socketul creat pentru conexiunea cu clientul
    # @param clientAddress (tuple) - tuplu cu adresa IP si portul clientului

    print("New connection with [" + str(clientAddress[0]) + ":" + str(clientAddress[1])+"]")
    msg = "\nTo disconnect, type !disconnect.\nSend some numbers (separated by space): "
    connectionSocket.send(msg.encode())
    while True:
        clMsg = connectionSocket.recv(1024)
        clMsg = clMsg.decode()
        if clMsg == "!disconnect":
            connectionSocket.send("Goodbye!".encode())
            connectionSocket.close()
            print("Connection ended with [" + str(clientAddress[0]) + ":" + str(clientAddress[1])+"]")
            break
        else:
            print(clientAddress[0] + ":" + str(clientAddress[1]) + " sent: " + clMsg)


def startServer():
    # Functia principala - creaza si porneste thread-ul pt fiecare client nou conectat

    svSocket.listen(5)
    print("\nWaiting for clients...")
    while True:
        # Acceptare conexiune si creare socket
        conSocket, clientAddr = svSocket.accept()
        thread = threading.Thread(target=handleClient, args=(conSocket, clientAddr))
        thread.start()
        print("Active connections: " + str(threading.activeCount() - 1))



# Creare socket TCP

ADDR = ("127.0.0.1", 7777)
svSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
svSocket.bind(ADDR)

startServer()
