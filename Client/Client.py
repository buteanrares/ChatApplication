import json
from requests import get
from Sockets import AudioSocket, TextSocket

# Network constants
TEXTADDR=("79.113.41.18",7777)
AUDIOADDR=("79.113.41.18",7778)


class Client:
    # Client class
    def __init__(self) -> None:
        super().__init__()
        self.TextSocket = None      # Socket for text
        self.AudioSocket = None  # Socket for audio

    
    @staticmethod
    def printClientData():
        # Prints client data in console when client executable starts

        print("\nFetching data...")
        clientData = get("https://ipinfo.io").text
        data = json.loads(clientData)
        print("   Public IPv4 address: {}".format(data["ip"]))
        print("   Country: {}".format(data["country"]))
        print("   Region: {}".format(data["region"]))
        print("   City: {}\n\n".format(data["city"]))


    def run(self):
        #Client startup 
        
        self.printClientData()
        self.TextSocket = TextSocket.TextSocket(TEXTADDR)      # Socket for text
        self.AudioSocket = AudioSocket.AudioSocket(AUDIOADDR)  # Socket for audio

client = Client()
client.run()