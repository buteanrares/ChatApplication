import threading
import socket
import json
from requests import get
import pyaudio

# Network constants
ADDR = ("192.168.0.103", 7777)

# Audio constants
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096

class Client:

    def __init__(self) -> None:
        super().__init__()

        #Network fields
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect(ADDR)

        #Audio fields
        py_audio = pyaudio.PyAudio()
        self.output_stream = py_audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
        self.input_stream = py_audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
    
    
    @staticmethod
    def printClientData():
        print("\nFetching data...")
        clientData = get("https://ipinfo.io").text
        data = json.loads(clientData)
        print("   Public IPv4 address: {}".format(data["ip"]))
        print("   Country: {}".format(data["country"]))
        print("   Region: {}".format(data["region"]))
        print("   City: {}\n\n".format(data["city"]))

    
    def handleReceiveAudio(self):
        while True:
            data = self.clientSocket.recv(CHUNK)
            self.input_stream.write(data)


    def handleSend(self):
        while True:
            print("Response: ", end="")
            msg = input()
            self.clientSocket.send(msg.encode())


    def handleReceiveText(self):
        while True:
            recvMsg = self.clientSocket.recv(1024)
            recvMsg = recvMsg.decode()
            print(recvMsg)


    def run(self):
        self.printClientData()

        send_thread = threading.Thread(target=self.handleSend)
        receiveText_thread = threading.Thread(target=self.handleReceiveText)
        receiveAudio_thread = threading.Thread(target=self.handleReceiveAudio)
        
        send_thread.start()
        receiveText_thread.start()
        receiveAudio_thread.start()
        
        send_thread.join()
        receiveText_thread.join()
        receiveAudio_thread.join()


client = Client()
client.run()
