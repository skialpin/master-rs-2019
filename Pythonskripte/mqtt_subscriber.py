# Quellen: In Anlehnung an
# https://tutorials-raspberrypi.de/datenaustausch-raspberry-pi-mqtt-broker-client/
# https://praxistipps.chip.de/python-mit-mysql-verbinden-und-daten-abfragen-so-gehts_95559

import paho.mqtt.client as mqtt
import logging
import time
import datetime
import MySQLdb

#MQTT-Server und MQTT-Topic
MQTT_SERVER = "surfbrett.ddns.net"
#MQTT_SERVER = "192.168.178.53"
MQTT_PATH = "TempGPS"

# Verbindung zur Datenbank herstellen
db = MySQLdb.connect(host="localhost",  # Host 
                     user="raven",      # Benutzername
                     passwd="jkdf",     # Passwort
                     db="sensordata")   # Name der Datenbank

# cursor ermoeglicht das Hinzufuegen / Manipulieren von Datensaetzen
cur = db.cursor()

# t = Zeit in Sekunden, wie lange der Broker Daten vom Publisher empfaengt
# tableName = Tabellenname
t = 400
tableName = "s12"

# Erstelle Tabelle mit Attributen und mit Angabe des Datentyps.
# Wenn es die Tabelle schon gibt, kommt ein Error, der in dem Fall ignoriert werden muss.
# Die Werte werden in diesem Fall an die schon bestehende Tabelle angehangen.
try:
    cur.execute("CREATE TABLE "+tableName+
                " (date varchar(255), topic varchar(255), temp float, lat float, lng float);")
except:
    pass

# Datum mit Uhrzeit auf die Sekunde als String, der sich alphabetisch ordnen laesst,
# z.B. wird der September als "09" und nicht als "9" dargestellt.
def getDatetime():
    dt = str(datetime.datetime.now())
    
    year = dt[0:4]
    month = dt[5:7]
    day = dt[8:10]
    hour = dt[11:13]
    minute = dt[14:16]
    second = dt[17:19]
    
    dateString = (year+"-"+month+"-"+day+"-"+hour+"-"+minute+"-"+second)
    return dateString

# Daten werden zusaetzlich in txt-File und csv-File gespeichert.
# Oeffnet beide Dateien zum Schreiben, Name = Datum mit Uhrzeit.
txt = open("/home/pi/Dokumente/MQTT/txt/" + getDatetime() + "_Messwerte.txt","w")
csv = open("/home/pi/Dokumente/MQTT/csv/" + getDatetime() + "_Messwerte.csv","w")

# Kopfzeile fuer das txt-File
def writeHeaderTXT():
    txt.write("topic")
    txt.write("\t")
    txt.write("temp")
    txt.write("\t")
    txt.write("lat")
    txt.write("\t")
    txt.write("lng")
    txt.write("\n")

# Kopfzeile fuer das csv-File
def writeHeaderCSV():
    csv.write("topic")
    csv.write("\t")
    csv.write("temp")
    csv.write("\t")
    csv.write("lat")
    csv.write("\t")
    csv.write("lng")
    csv.write("\n")

# Wenn der Client eine CONNACK-Antwort vom Server erhaelt, kommt:
# "Connected with result code 0".
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # "subscribe" in on_connect () bedeutet, dass bei einem Verbindungsverlust
    # und einer Wiederverbindung die Abonnements erneuert werden.
    client.subscribe(MQTT_PATH)
    
# nicht verwendet
def on_disconnect(client, userdata,rc=0):
    logging.debug("DisConnected result code "+str(rc))
    client.loop_stop()
 
# topic und payload (Daten) ist die Ausgabe vom Server, wenn er
# eine PUBLISH-Nachricht empfangen hat.
# Daten werden empfangen und in txt- und csv-File geschrieben.
def on_message(client, userdata, msg):
    topic = msg.topic
    mqttData = msg.payload
    txt.write(topic)
    txt.write("\t")
    txt.write(mqttData)
    txt.write("\n")
    csv.write(topic)
    csv.write("\t")
    csv.write(mqttData)
    csv.write("\n")
    insertValuesDB(topic, mqttData)

# Datenbank befuellen mit Datensatz aus der on_message Methode
def insertValuesDB(topic, mqttData):    
    mqttData = mqttData.split(" ")
    date = getDatetime()
    temp = mqttData[0]
    lat = mqttData[1]
    lng = mqttData[2]
    cur.execute("INSERT INTO "+tableName+" (date, topic, temp, lat, lng) VALUES ('"
                +date+"', '"+topic+"', '"+temp+"', '"+lat+"', '"+lng+"')")
    db.commit()

# Funktionen aufrufen
writeHeaderTXT()
writeHeaderCSV()
 
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# MQTT - Port ist 1883
client.connect(MQTT_SERVER, 1883, 60)

# Offen fuer den Client fuer t Sekunden
client.loop_start()
time.sleep(t)
client.loop_stop()

# Unbegrenzt offen fuer den Client
#client.loop_forever()