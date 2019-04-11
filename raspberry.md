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

zu 1.) mit `sudo raspi-config` kann das Konfigurationsprogramm für den Raspberry gestartet werden. Unter dem Punkt "Interfacing" gibt es den Punkt "SPI". SPI muss aktiviert werden.

zu 2.) ebenfalls mit `sudo raspi-config` kann SSH aktiviert werden. Der Punkt befindet sich ebenfalls unter "Interfacing".

zu 3.) ein `sudo apt-get install libjpeg-dev zlib1g-dev` stellt die nötigen Pakete bereit, damit das Pillow-Paket für Python erfolgreich installiert werden kann.

zu 4.) ALSA (Advanced Liux Sound System) übernimmt die Verwaltung der Soundkarten. Mit `cat /proc/asound/modules` und `cat /proc/asound/cards` können die Soundkarten aufgelistet werden. Zu Beginn müssten zwei Soundkarten gefunden werden: die eingebaute BCM2835 und die externe USB Audio-Karte.

Um die interne Soundkarte zu deaktivieren wird die Konfigurationsdatei angepasst mit `sudo nano /boot/config.txt` und der Eintrag ganz am Ende der Datei geändert in `dtparam=audio=off`.

Um die Default-Soundkarte auf USB umzustellen wird `sudo nano /usr/share/alsa/alsa.conf` aufgerufen und die Einträge `defaults.ctl.card` sowie `defaults.pcm.card` jeweils auf `1` gesetzt.

zu 5.) Hier gibt es zwei Möglichkeiten: a) [Oracle Java auf eine neuere Version bringen](https://gist.github.com/ribasco/fff7d30b31807eb02b32bcf35164f11f) oder b) die [Ice-T Version von Java verwenden](https://raspberrypi.stackexchange.com/questions/79500/pycharm-2017-3-3-hangs).

zu 6.) Mit `sudo apt-get install python-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev   libsdl1.2-dev libsmpeg-dev python-numpy subversion libportmidi-dev ffmpeg libswscale-dev libavformat-dev libavcodec-dev` werden die nötigen Abhängigkeiten für PyGame installiert.

zu 7.) PyCharm kann die Passwörter auch in einer KeePass-Datei speichern. Diese Option lässt sich unter "Settings/Appearence/System Settings/Passwords" umstellen.

zu 8.) hier könnt ihr lesen wie ihr wieder Platz auf der SD Karte schafft: https://raspberry.tips/faq/raspberry-pi-speicherplatz-voll-sd-karte-aufraeumen

zu 9.) Um PyCharm mit "sudo" zu starten, müsst ihr die Schaltfläche ändern, mit der ihr PyCharm aufruft. Im Schaltflächen Editor gibt es 3 Zeilen, die ihr seht wenn Ihr die Schaltfläche bearbeitet. In der mittleren Zeile steht der Programmaufruf. Dort schreibt ihr einfach "sudo" davor. (ohne Anführungszeichen natürlich)


pip3 install luma luma.core luma.led_matrix numpy pillow  pygame datetime flask

erster Befehl: "~/Riesen-Tetris $ chmod +x MAIN.py"
zweiter Befehl: "sudo nano /lib/systemd/system/LED.service "
in folgende Datei muss:
"
[Unit]
Description=LED
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
ExecStart=/home/pi/Riesen-Tetris/MAIN.py
WorkingDirectory=/home/pi/Riesen-Tetris/
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=tetris
Restart=always
RestartSec=15
User=root 
Group=root

[Install]
WantedBy=multi-user.target
Alias=LED.service
"

dritter Befehl: "sudo systemctl daemon-reload"
vierter Befehl: "sudo systemctl enable LED.service"
letzer Befehl: "sudo systemctl start LED.service" 
