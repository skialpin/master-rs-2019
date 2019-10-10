# Quelle: In Anlehnung an
# http://ozzmaker.com/using-python-with-a-gps-receiver-on-a-raspberry-pi/

import serial
import math
import numpy as np
import time

# serieller Port 
port = "/dev/ttyAMA0"

# Parsen der Latitude und Longitude des NMEA-sentences 
def parseLatLng(data):
    if data[0:6] == "$GPRMC":
        sdata = data.split(",")
        if sdata[2] == 'V':
            print ("no satellite data available")
            return
        print("---Parsing GPRMC---"),
        lat = sdata[3]
        lon = sdata[5]
        print(convertDMMtoDDD(float(lat),float(lon)))
 
# Umwandlung von Degree Minute Minute zu Degree Degree Degree
# 5234.5678 => 52.57613
# 1345.6789 => 13.76132
def convertDMMtoDDD(lat,lon):
    lat1 = math.floor(lat/100)
    lon1 = math.floor(lon/100)
    lat2 = lat - (100*lat1)
    lon2 = lon - (100*lon1)
    lat3 = (lat2/0.6)/100
    lon3 = (lon2/0.6)/100
    lat4 = lat1 + np.round(lat3,5)
    lon4 = lon1 + np.round(lon3,5)
    return str(lat4) + " " + str(lon4)

# Ausgeben der Koordinaten auf der Konsole 1x pro Sekunde
print ("Receiving GPS data")
while True:
    try:
        time.sleep(0.5)
        ser = serial.Serial(port, baudrate = 9600)
        time.sleep(0.5)
        data = ser.readline()
        parseLatLng(data)
    except:
        print('data not available')
        ser.close() 