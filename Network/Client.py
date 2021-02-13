import socket
import json
from requests import get
from Sockets import AudioSocket, TextSocket

# Network constants
ADDR = ("127.0.0.1", 7776)

class Client:

    def __init__(self) -> None:
        super().__init__()
        self.TextSocket = TextSocket.TextSocket(ADDR)
        self.AudioSocket = AudioSocket.AudioSocket(ADDR)
    
    
    @staticmethod
    def printClientData():
        print("\nFetching data...")
        clientData = get("https://ipinfo.io").text
        data = json.loads(clientData)
        print("   Public IPv4 address: {}".format(data["ip"]))
        print("   Country: {}".format(data["country"]))
        print("   Region: {}".format(data["region"]))
        print("   City: {}\n\n".format(data["city"]))


    def run(self):
        self.printClientData()
        
        self.TextSocket.startTextThreads()
        self.AudioSocket.startAudioStream()

        self.TextSocket.stopTextThreads()


client = Client()
client.run()
