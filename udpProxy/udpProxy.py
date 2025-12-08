from socket import *
from urllib import response
import requests # install this library: $ python -m pip install requests
import json

PORT = 17000
endpoints = {
    "decibel": "https://localhost:7080/api/NoiseDB",
    "humidityPercent": "https://localhost:7080/api/HumidityDB",
    "celcius": "https://localhost:7080/api/TemperatureDB",
    "lumen": "https://localhost:7080/api/LightDB"
}

sock_receiver = socket(AF_INET, SOCK_DGRAM)
sock_receiver.bind(('', PORT))

print("Proxy UDP Receiver started")
print(f'Listening for incoming UDP messages on port {PORT}')

while True:
    msg, clientAdr = sock_receiver.recvfrom(3000)
    message_str = msg.decode()
    print(f'Message from UDP broadcaster {clientAdr}: {message_str}')

    message_dictionary = json.loads(message_str)
    print(f'Converted to dictionary: {message_dictionary}')

    for key, url in endpoints.items():
        value = message_dictionary.get(key)
        payload = {
            "raspberryId": message_dictionary["raspberryId"],
            key: value if value is not None else "-1",
            "date": message_dictionary["date"],
            "time": message_dictionary["time"],
        }
        print(f'url: {url} message: {payload}') # For testing purposes when the using the dummy measuments...
        #response = requests.post(url, json=payload, verify=False)
        # json=... automatically serializes the dictionary to JSON
        # json=... automatically sets the Content-Type header to application/json
        #print(f'Response from REST API: {response.status_code} - {response.text}')