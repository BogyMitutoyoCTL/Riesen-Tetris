# Raspberry Einrichtung

Damit das Riesen-Tetris programmierbar und spielbar wird, müssen einige Dinge berücksichtigt werden:

1. das LED-Matrix-Modul wird über SPI angesteuert.
2. um den Raspberry später ohne Display noch anpassen zu können, brauchen wir einen SSH Zugang.
3. Die Luma-Bibliothek hat eine Abhängigkeit zum Paket Pillow. Pillow wiederum braucht JPEG-Funktionen. Diese müssen vom Betriebssystem bereitgestellt werden.
4. die WS2812 LEDs benötigen einen Timer zur Ansteuerung. Da es nur einen Timer auf dem Raspberry gibt, kann dieser nicht mehr die interne Soundkarte ansteuern. Damit wir trotzdem Musik haben, verwenden wir eine externe USB Soundkarte. Daher muss die interne Soundkarte muss deaktiviert werden und die USB Soundkarte als Default-Soundkarte eingerichtet werden.
5. PyCharm brauche eine neuere Java-Version.
6. Die Pygame-Bibliothek braucht ebenfalls Funktionen vom Betriebssystem.
7. PyCharm kann das Git Passwort speichern. Allerdings funktioniert auf dem Raspberry die Unterstützung der Keychain nicht.
8. Sollte die SD Karte vom Raspberry voll sein könnt ihr auch einige Sachen darauf löschen, die wir nicht brauchen.
9. PyCharm mit "sudo" laufen lassen, damit kein Fehler "Permission denied" kommt wenn ihr auf LED Matrix zugreifen wollt...

zu 1.) wird vom Shell-Script `check.sh` überprüft und ggf. aktiviert. 

zu 2.) kann mit `sudo raspi-config` aktiviert werden. Der Punkt SSH befindet sich unter "Interfacing".

zu 3.) wird vom Shell-Script `check.sh` überprüft und ggf. installiert.

zu 4.) wird vom Shell-Script `check.sh` überprüft und ggf. aktiviert.

zu 5.) wird vom Skript `pycharm.sh` überprüft und ggf. umgestellt.

zu 6.) wird vom Shell-Script `check.sh` überprüft und ggf. installiert.

zu 7.) PyCharm kann die Passwörter auch in einer KeePass-Datei speichern. Diese Option lässt sich unter "Settings/Appearence/System Settings/Passwords" umstellen.

zu 8.) hier könnt ihr lesen wie ihr wieder Platz auf der SD Karte schafft: https://raspberry.tips/faq/raspberry-pi-speicherplatz-voll-sd-karte-aufraeumen

zu 9.) wird vom Skript `pycharm.sh` eingerichtet.

## Python Pakete

Grundsätzlich können Paketanforderungen bei Python in eine Datei geschrieben werden. Dann können alle Abhängigkeiten mit einem einzigen Befehl installiert werden:

    sudo pip3 install -r requirements.txt

## Tetris Service

Scripte ausführbar machen:

    chmod +x /home/pi/Riesen-Tetris/start_main.sh
    chmod +x /home/pi/Riesen-Tetris/stop_main.sh
    
Service anlegen, aktivieren und starten: wird übernommen vom Skript `installservice.sh`:

    cd service
    chmod +x installservice.sh
    sudo ./installservice.sh
