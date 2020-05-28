""" Python Implemetation for Sending SMS to Mobile
    Developed by Team Evolvers, Acharya Nagarjuna University """

# Packages Required
import serial
import RPi.GPIO as GPIO      
import os, time

def sendMessage(latitude,longitude,person):
    
    GPIO.setmode(GPIO.BOARD)    
    
    # Enable Serial Communication
    port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=1)
     
    # Transmitting AT Commands to the Modem ('\r\n' indicates the Enter key)
     
    port.write('AT'+'\r\n')     
    port.write('ATE0'+'\r\n')      # Disable the Echo
    port.write('AT+CMGF=1'+'\r\n')  # Select Message format as Text mode 
    port.write('AT+CNMI=2,1,0,0,0'+'\r\n')   # New SMS Message Indication
    port.write('AT+CMGS="9052191523"'+'\r\n')   # Sending a message to a particular Number
    port.write(person'-Persons, Detected at Lat: '+latitude+', Long:'+longitude+'\r\n')  # Message: person, latitude and longitude
    port.write("\x1A") # Enable to send SMS
