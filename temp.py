# Quelle:
# Weigend, M. (2019). Raspberry Pi programmieren mit Python. Rheinbreitbach.
# Seiten: 319,320
# Online abrufbar unter www.mitp.de/912 => Download
# Pfad: /programme_auflage_4/kap-12/temp.py

import os, time

# Initialisierung des 1-Wire-Bus
os.system('modprobe w1-gpio')
os.system("modprobe w1-therm")

# Pfad fuer Datei mit Temperaturwerten, Platzhalter {}
PATH = "/sys/bus/w1/devices/{}/w1_slave"

# os.listdir liefert Liste aller Verzeichniseintraege des ausgegeben Ordners.
# Datei des verwendeteten Sensors DS18S20 beginnt mit 10.
# Platzhalter {} im Pfad wird durch den Ordner 10... ersetzt.
for d in os.listdir("/sys/bus/w1/devices/"):
    if d.startswith("10") or d.startswith("28"):
        path = PATH.format(d)

# first = 1. Zeile, second = 2.Zeile der Datei.
# In 1. Zeile sollte YES stehen, am Ende der 2. Zeile die Temperatur in 1/1000 Celsius.
# 2. Zeile wird aufgespalten in a und b und Gleichheitszeichen als Trennsymbol verwendet.
# Somit ist 2. Element der 2. Zeile ist die Temperatur (Variable b).
def readTemp():
    ok = False                                 
    while not ok:
        f = open(path, 'r')                    
        first, second = f.readlines()       
        f.close()                           
        if 'YES' in first:                   
            ok = True
    a, b = second.split('=')        
    return int(b)/1000                

# Einmalig Pfad und sekuendlich Temperatur auf der Konsole ausgeben
if __name__ == "__main__":
    print("Pfad zur Daten-Datei des Thermosensors:", path)
    while True:
        print(readTemp(),'Grad Celsius')
        time.sleep(1)