""" Python Implemetation for Sending Data to CloudChip for Visualisation
    Developed by Team Evolvers, Acharya Nagarjuna University """

# Packages Required
import os
import time
import sys
import paho.mqtt.client as mqtt
import json

def sendApi(latitude,longitude,person):
    
    TOKEN = 'KX39TCoUhW3nWbevoZ9w'  # Token to Access
    topic = 'v1/devices/me/telemetry' # Telementary
    qos=1

    client = mqtt.Client()
    client.username_pw_set(TOKEN)
    client.connect("www.cloudchip.io", 1883, 60)
    client.loop_start()

    # Data or Parameters to Send to Api
    data = {'latitude': latitude,'longitude': longitude,'person': person}

    client.publish(topic, json.dumps(data), qos)
    client.loop_stop()
    client.disconnect()
