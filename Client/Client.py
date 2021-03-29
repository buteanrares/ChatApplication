import json
from requests import get
from Sockets import AudioSocket, TextSocket


class Client:
    # Client class
    def __init__(self) -> None:
        super().__init__()
        self.TextSocket = None      # Socket for text
        self.AudioSocket = None     # Socket for audio

    def connect(self):
        ip = input("Type server's IP address: ")
        port = int(input("Type server's port: "))

        self.TextSocket = TextSocket.TextSocket((ip, port))
        self.AudioSocket = AudioSocket.AudioSocket((ip, port+1))

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
        # Client startup

        self.printClientData()
        self.connect()


client = Client()
client.run()
