import paho.mqtt.publish as publish
import os, time
import serial
import string
import pynmea2
import random
import numpy as np

# Initialisierung des 1-Wire-Bus
os.system('modprobe w1-gpio')
os.system("modprobe w1-therm")

#Pfad fuer Datei mit Temperaturwerten, Platzhalter {}
PATH = "/sys/bus/w1/devices/{}/w1_slave"
MQTT_SERVER = "surfbrett.ddns.net" 
#MQTT_SERVER = "192.168.178.53"
MQTT_PATH = "TempGPS"

# os.listdir liefert Liste aller Verzeichniseintraege des ausgegeben Ordners
# Datei des verwendeteten Sensors DS18S20 beginnt mit 10
# Platzhalter {} im Pfad wird durch den Ordner 10... ersetzt.
for d in os.listdir("/sys/bus/w1/devices/"):
    if d.startswith("10") or d.startswith("28"):
        path = PATH.format(d)

# first = 1. Zeile, second = 2.Zeile der Datei
# In 1. Zeile sollte YES stehen, am Ende der 2. Zeile die Temperatur in 1/1000 Celsius
# 2. Zeile wird aufgespalten in a und b und Gleichheitszeichen als Trennsymbol verwendet
# Somit ist 2. Element der 2. Zeile ist die Temperatur (Variable b)
def readTemp():
    ok = False                                 
    while not ok:
        f = open(path, 'r')                    
        first, second = f.readlines()       
        f.close()                           
        if 'YES' in first:                   
            ok = True
    a, b = second.split('=')        
    return str(float(b)/1000)

# Zufallswerte fuer Temperatur, Latitude und Longitude, um ohne Sensoren testen zu koennen
def generateTemp():
    temp = np.round(27 + random.random(),2)
    return str(temp)
            
def generateLat():
    lat = np.round(52 + random.random(),2)
    return str(lat)

def generateLng():
    lng = np.round(13 + random.random(),2)
    return str(lng)
 
# publish.single(Topic, MqttDaten, Broker)
# Daten werden im 1-Sekunden-Takt an den Broker gesendet
while True:
    publish.single(MQTT_PATH, generateTemp() + " " + generateLat() + " " + generateLng(), hostname=MQTT_SERVER)
    time.sleep(1)