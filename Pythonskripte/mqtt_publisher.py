# Quellen: In Anlehnung an
# Weigend, M. (2019). Raspberry Pi programmieren mit Python. Rheinbreitbach.
# http://ozzmaker.com/using-python-with-a-gps-receiver-on-a-raspberry-pi/
# https://tutorials-raspberrypi.de/datenaustausch-raspberry-pi-mqtt-broker-client/

import paho.mqtt.publish as publish
import os, time
import serial
import math
import numpy as np

#------------------------------------------

os.system('modprobe w1-gpio')
os.system("modprobe w1-therm")

PATH = "/sys/bus/w1/devices/{}/w1_slave"
MQTT_SERVER = "surfbrett.ddns.net"
#MQTT_SERVER = "192.168.178.53"
MQTT_PATH = "TempGPS"

# serieller Port
port = "/dev/ttyAMA0"

for d in os.listdir("/sys/bus/w1/devices/"):
    if d.startswith("10") or d.startswith("28"):
        path = PATH.format(d)
        
#------------------------------------------

def readTemp():
    ok = False                                 
    while not ok:
        f = open(path, 'r')                    
        first, second = f.readlines()       
        f.close()                           
        if 'YES' in first:                   
            ok = True
    a, b = second.split('=')
    temp = str(float(b)/1000)
    return temp

def parseGPS(data):
        sdata = data.split(",")
        lat = sdata[3]
        latDir = sdata[4]
        lon = sdata[5]
        lonDir = sdata[6]
        return convertDMMtoDDD(float(lat),latDir,float(lon),lonDir)

# Umwandlung funktionert auch auf der suedlichen oder westlichen Erdhalbkugel 
def convertDMMtoDDD(lat,latDir,lon,lonDir):
    lat1 = math.floor(lat/100)
    lon1 = math.floor(lon/100)
    lat2 = lat - (100*lat1)
    lon2 = lon - (100*lon1)
    lat3 = (lat2/0.6)/100
    lon3 = (lon2/0.6)/100
    lat4 = lat1 + np.round(lat3,5)
    lon4 = lon1 + np.round(lon3,5)
    if latDir == "S":
        lat4*=-1
    if lonDir == "W":
        lon4*=-1
    return str(lat4) + " " + str(lon4)

#------------------------------------------

# Serieller Port wird ausgelesen, das Ergebnis sind NMEA-Strings.
# Der NMEA-String, der mit "$GPRMC" anfaengt, beinhaltet u.A. Koordinaten.
# Die Publish.single() Funktion uebermittelt die Daten via MQTT.
# Die Exception schliesst die serielle Schnittstelle und startet von vorne,
# falls fehlerhaft geparst wurde.
while True:
    try:
        time.sleep(0.5)
        ser = serial.Serial(port, baudrate = 9600)
        time.sleep(0.5)
        data = ser.readline()
        if data[0:6] == "$GPRMC":
            publish.single(MQTT_PATH, readTemp() + " " + parseGPS(data), hostname=MQTT_SERVER)
    except:
        ser.close()