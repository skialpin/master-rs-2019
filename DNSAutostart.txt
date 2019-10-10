# Quelle: 
# https://tutorials-raspberrypi.de/raspberry-pi-autostart-programm-skript/
	
case "$1" in
    start)
        echo "noip wird gestartet"
        # Starte Programm
        /usr/local/bin/noip2
        ;;
    stop)
        echo "noip wird beendet"
        # Beende Programm
        killall noip2
        ;;
    *)
        echo "Benutzt: /etc/init.d/noip {start|stop}"
        exit 1
        ;;
esac
 
exit 0