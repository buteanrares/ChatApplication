import socket
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 4096

class AudioSocket:

    def __init__(self,ADDR) -> None:
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect(ADDR)

        self.audio = pyaudio.PyAudio()
        self.audioStream = None

    def startAudioStream(self):
        self.audioStream =self.audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
    
    
    def receiveAudio(self):
        while True:
            data = self.socket.recv(CHUNK)
            self.audioStream.write(data)

