#to use print function
from __future__ import print_function
import paho.mqtt.publish as publish
import Adafruit_DHT
import time
from urllib.request import urlopen
import json
import threading

class Publish:
    def __init__(self):
        self.control = True
        self.publisher_threat = threading.Thread(target=self.push)
        self.publisher_threat.start()

        
        self.sensor = Adafruit_DHT.DHT11
        # Set GPIO sensor is connected to
        self.gpio = 4

        # The ThingSpeak Channel  details
        self.channelID = "1410012"
        self.writeAPIKey = "GPWINVR7PERGOKSU"
        self.broker_address = "mqtt.thingspeak.com"
        self.user = "mwa0000009686187"
        self.mqttAPIKey = "TVIUC0UTDT9YOJ4I"
        self.tTransport = "websockets"
        self.tPort = 80

        self.TOPIC = "channels/" + self.channelID + "/publish/" + self.writeAPIKey
        
    def push(self):
        while self.control:
            try:
                # code to get temperature and humidity values
                humidity, temperature = Adafruit_DHT.read_retry(
                    self.sensor, self.gpio)

                if humidity is not None and temperature is not None:
                    print(
                        'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
                else:
                    print('Failed to get reading. Try again!')
                    continue

                # build the payload string.
                payload = "field1=" + str(temperature)+"&field2="+str(humidity)

                # publish to the topic.
                publish.single(self.TOPIC, payload, hostname=self.broker_address, transport=self.tTransport, port=self.tPort, auth={
                               'username': self.user, 'password': self.mqttAPIKey})

                time.sleep(2)

            except Exception as e:
                print('Exception: push ', str(e))

 

class Subscribe:
    
    def __init__(self):
        self.URL = 'https://api.thingspeak.com/channels/1410012/feeds.json?results=1'

    def fetchdata(self):
        # function to fetch date from Chennel API
        with urlopen(self.URL) as url:
            data = json.loads(url.read().decode())

            return (
                data['feeds'][-1]['created_at'].split('T')[0],
                data['feeds'][-1]['created_at'].split('T')[1][:-1],
            )
   

Publish()
Subscribe()
