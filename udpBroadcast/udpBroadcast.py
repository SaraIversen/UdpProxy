# -*- coding: utf-8 -*-
from socket import *
#from sense_hat import SenseHat
#import pyaudio
#import numpy as np
import time
import json
import datetime
import random

BROADCAST_IP = '255.255.255.255'
PORT = 17000

sock_sender = socket(AF_INET, SOCK_DGRAM)
sock_sender.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

#sense = SenseHat()

# Noise measurement setup
#CHUNK = 1024
#FORMAT = pyaudio.paInt16
#CHANNELS = 1
#RATE = 44100

#p = pyaudio.PyAudio()

# Find USB-microphone automatically
device_index = None
# for i in range(p.get_device_count()):
#     info = p.get_device_info_by_index(i)
#     if "USB" in info["name"]:
#         device_index = i
#         print("Bruger USB mikrofon:", info["name"])
#         break

# Check if a mic was found
if device_index is None:
    print("Ingen USB mikrofon fundet.")

# Open the stream for noise measurement
# if device_index is not None:
#     stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, input_device_index=device_index, frames_per_buffer=CHUNK)

print("Starting UDP broadcaster...")

while True:
    # Noise measurement
    # if device_index is not None:
    #     data = stream.read(CHUNK, exception_on_overflow=False)
    #     audio_data = np.frombuffer(data, dtype=np.int16)
    #     db = np.sqrt(np.mean(np.square(audio_data)))
    # else:
    db = random.uniform(30, 60)  # dummy-værdi for test uden headphone mic

    # Humidity measurement
    #humidity = sense.get_humidity()
    humidity = random.uniform(70, 80)  # dummy-værdi for test uden SenseHAT
    
    # Temperature measurement
    #temperature = sense.get_temperature()
    temperature = random.uniform(19, 23)  # dummy-værdi for test uden SenseHAT

    # Light measurement
    light = random.uniform(380, 420)  # dummy-værdi for test uden light sensor

    now = datetime.datetime.now()

    message_dictionary = {
        "raspberryId": 1,
        "date": now.date().isoformat(), # "2025-12-04",
        "time": now.strftime("%H:%M:%S"), # "14:35:20" 
        "decibel": db,
        "humidityPercent": humidity,
        "celcius": temperature,   
        "lumen": light,
    }

    message = json.dumps(message_dictionary)

    print("Sending:", message)

    sock_sender.sendto(message.encode(), (BROADCAST_IP, PORT))
    time.sleep(10) # Sleep for 10 seconds between messages