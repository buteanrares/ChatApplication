import threading
import json
from requests import get
from Sockets import AudioSocket, TextSocket

# Network constants
TEXTADDR=("192.168.0.104",30310)
AUDIOADDR=("192.168.0.104",30311)

class Client:

    def __init__(self) -> None:
        super().__init__()
        self.printClientData()
        self.TextSocket = TextSocket.TextSocket(TEXTADDR)
        self.AudioSocket = AudioSocket.AudioSocket(AUDIOADDR)

    
    
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


client = Client()
