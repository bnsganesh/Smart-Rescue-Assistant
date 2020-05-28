""" Python Implemetation for retreving Longitude and Latitude from GPS MOdule
    Developed by Team Evolvers, Acharya Nagarjuna University """

# Packages required 
import serial

# Packages required for sending data to Mobile and API
from sms import *
from api import *

def decode(coord):
    x = coord.split(".")        #Converts DDDMM.MMMMM > DD deg MM.MMMMM min
    head = x[0]
    tail = x[1]
    deg = head[0:-2]
    min = head[-2:]
    return deg + " deg " + min + "." + tail + " min"

def parseGPS(data,person):
    sdata = data.split(",")
    latitude = decode(sdata[3]) # latitude
    longitude = decode(sdata[5]) # longitute
    sendMessage(latitude,longitude,person) # Sending SMS
    sendApi(latitude,longitude,person) # Sending Data to Api
 
def trigger(person):
    port = "/dev/serial0"
    ser = serial.Serial(port, baudrate = 9600, timeout = 0.5)
    parseGPS(data,person) # Access GPS lat, long  then sends to mobile and Api

