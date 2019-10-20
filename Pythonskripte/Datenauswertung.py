import matplotlib.pyplot as plt
import numpy as np

file = open('2019-10-03-15-45-02_Messwerte_modifiziert.csv','r')
data = file.read().split()
n = len(data)
diff = []

# Gibt aus zwei date-Strings die Differenz in Sekunden.
# z.B. a = 2019-10-03-15-56-10, b = 2019-10-03-16-05-08,
# 16:05:08 - 15:56:20 = 8min 58sec = 538sec, return 538
# Funktioniert nur, wenn Tag sich nicht aendert.
def getDifferenceInSeconds(a,b):
    hourDiff    = 3600*   int(data[b][11:13])      - 3600* int(data[a][11:13])
    minuteDiff  = 60*     int(data[b][14:16])      - 60*   int(data[a][14:16])
    secondDiff  =         int(data[b][17:19])      -       int(data[a][17:19])
    return hourDiff + minuteDiff + secondDiff

for i in range(0,n-1):     #komplett
#for i in range(350,400):   #Teil der Daten
    diff.append(getDifferenceInSeconds(i,i+1))

x = np.arange(0,n-1)       #komplett
#x = np.arange(350,400)     #Teil der Daten

# Daten sortieren und spaeter ausgeben
#diff.sort()
#print(diff)

# Plotten und Speichern
fig, ax = plt.subplots()
ax.plot(x, diff, 'r')
ax.set_title("Zeitabstände zwischen zwei Messungen")
ax.set_xlabel("Nr. der Messung")
ax.set_ylabel("Zeitdifferenz in Sekunden")
plt.grid(True) 
plt.savefig("Datenauswertung.jpg")
