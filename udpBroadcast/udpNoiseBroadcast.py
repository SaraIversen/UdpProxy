# -*- coding: utf-8 -*-
import pyaudio
import numpy as np
import time
from socket import *
import time
import random
import json

BROADCAST_IP = '255.255.255.255' #special IP address for broadcast
PORT = 17000

sock_sender = socket(AF_INET, SOCK_DGRAM)
sock_sender.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

CHUNK = 1024        # mindre chunk for hurtigere opdatering
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

# Find USB-mikrofonen automatisk
device_index = None
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if "USB" in info["name"]:
        device_index = i
        print("Bruger USB mikrofon:", info["name"])
        break

if device_index is None:
    raise RuntimeError("Ingen USB mikrofon fundet.")

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=CHUNK)

print("Maaler lydniveau...")

while True:
    data = stream.read(CHUNK, exception_on_overflow=False)
    audio_data = np.frombuffer(data, dtype=np.int16)
    db = np.sqrt(np.mean(np.square(audio_data)))

    measuments_dictionary = {
        "sound": db }
    message: str = json.dumps(measuments_dictionary)
    print(f'Broadcaster sending: {message}')
    sock_sender.sendto(message.encode(), (BROADCAST_IP, PORT))
    time.sleep(10) # sleep for 2 seconds between messages