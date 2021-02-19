import socket
import pyaudio
import threading

chunk_size = 4096 # 4kb
audio_format = pyaudio.paInt16
channels = 1
rate = 20000

class AudioSocket:
    # Audio socket class

    def __init__(self,ADDR) -> None:
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect(ADDR)

        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
        
        # start threads
        receive_thread = threading.Thread(target=self.receive_server_data).start()
        self.send_data_to_server()


    def receive_server_data(self):
        # Receives audio data from server
        
        while True:
            try:
                data = self.socket.recv(4096)
                self.playing_stream.write(data)
            except:
                pass


    def send_data_to_server(self):
        #Sends audio data to server

        while True:
            try:
                data = self.recording_stream.read(4096)
                self.socket.sendall(data)
            except:
                pass
