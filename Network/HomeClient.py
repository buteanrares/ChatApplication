import threading
import socket
import json
from requests import get
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import pyaudio


ADDR = ("25.105.200.208", 7777)

class HomeClient(DatagramProtocol):

    def __init__(self) -> None:
        super().__init__()
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect(ADDR)

    def startProtocol(self):
            py_audio = pyaudio.PyAudio()
            self.buffer = 1024  # 127.0.0.1
            self.another_client = "25.105.200.208", 7777

            self.output_stream = py_audio.open(format=pyaudio.paInt16,
                                            output=True, rate=44100, channels=2,
                                            frames_per_buffer=self.buffer)
            self.input_stream = py_audio.open(format=pyaudio.paInt16,
                                            input=True, rate=44100, channels=2,
                                            frames_per_buffer=self.buffer)
            reactor.callInThread(self.record)


    def record(self):
        while True:
            data = self.input_stream.read(self.buffer)
            self.transport.write(data, self.another_client)


    def datagramReceived(self, datagram, addr):
        self.output_stream.write(datagram)


    def printClientData(self):
        print("\nFetching data...")
        clientData = get("https://ipinfo.io").text
        data = json.loads(clientData)
        print("   Public IPv4 address: {}".format(data["ip"]))
        print("   Country: {}".format(data["country"]))
        print("   Region: {}".format(data["region"]))
        print("   City: {}\n\n".format(data["city"]))


    def handleSeding(self):
        while True:
            print("Response: ", end="")
            msg = input()
            self.clientSocket.send(msg.encode())


    def handleReceiving(self):
        while True:
            recvMsg = self.clientSocket.recv(1024)
            recvMsg = recvMsg.decode()
            print(recvMsg)

    def run(self):
        self.printClientData()

        send_thread = threading.Thread(target=self.handleSeding)
        receive_thread = threading.Thread(target=self.handleReceiving)
        
        send_thread.start()
        receive_thread.start()
        
        reactor.listenUDP(7777, self)
        reactor.run()
        
        send_thread.join()
        receive_thread.join()


homeclient = HomeClient()
homeclient.run()
