import threading
import socket
import json
import os
from requests import get


def printClientData():
    print("\n\nFetching data...")
    clientData = get("https://ipinfo.io").text
    data = json.loads(clientData)
    print("   Public IPv4 address: {}".format(data["ip"]))
    print("   Country: {}".format(data["country"]))
    print("   Region: {}".format(data["region"]))
    print("   City: {}\n\n".format(data["city"]))


def handleSeding():
    while True:
        print("Response: ", end="")
        msg = input()
        clientSocket.send(msg.encode())


def handleReceiving():
    while True:
        recvMsg = clientSocket.recv(1024)
        recvMsg = recvMsg.decode()
        print(recvMsg)


printClientData()

# Creare socket TCP
ADDR = ("25.105.200.208", 7777)
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect(ADDR)

send_thread = threading.Thread(target=handleSeding)
receive_thread = threading.Thread(target=handleReceiving)
send_thread.start()
receive_thread.start()
send_thread.join()
receive_thread.join()
