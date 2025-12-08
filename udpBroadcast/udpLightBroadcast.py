from socket import *
#from sense_hat import SenseHat
import time
import json
import datetime
import random

BROADCAST_IP = '255.255.255.255'
PORT = 17003

sock_sender = socket(AF_INET, SOCK_DGRAM)
sock_sender.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

#sense = SenseHat()

print("Starting SenseHAT UDP broadcaster...")

while True:
    #humidity = sense.get_humidity()
    light = random.uniform(380, 420)  # dummy-værdi for test uden SenseHAT
    now = datetime.datetime.now()

    message_dictionary = {
        "raspberryId": 1,
        "lumen": light,
        "date": now.date().isoformat(), # "2025-12-04",
        "time": now.strftime("%H:%M:%S") # "14:35:20"        
    }

    message = json.dumps(message_dictionary)

    print("Sending:", message)

    sock_sender.sendto(message.encode(), (BROADCAST_IP, PORT))
    time.sleep(10)