#!/bin/bash

# SPI checks
spi=`cat /boot/config.txt |grep ^dtparam=spi=on$| wc -l`
if [ "$spi" -eq "1" ]; then
	echo "SPI seems enabled";
else
	echo "SPI seems disabled. Enable it in raspi-config and reboot";
	exit 3
fi

spi=`lsmod | grep spi_bcm2835 | wc -l`
if [ "$spi" -eq "1" ]; then
	echo "SPI is already active";
else
	echo "SPI does not seem active yet. If you just enabled it, a reboot is required";
	exit 4
fi

if [[ -e /dev/spidev0.0 ]]; then
	echo "SPI kernel device found";
else
	echo "No SPI kernel device found";
	exit 5
fi

# Audio checks
if [ "`cat /proc/asound/modules | wc -l`" -gt "1" ]; then
	echo "Too many sound cards found. Disable internal sound card in /boot/config.txt. If you just disabled it, please reboot."
	exit 6
fi

if [ "`cat /proc/asound/modules | grep usb | wc -l`" -eq "1" ]; then
        echo "USB soundcard found.";
else
	echo "USB soundcard not found";
	exit 7
fi

if [ "`cat /proc/asound/cards | grep USB | wc -l`" -gt "1" ]; then
	echo "USB soundcard found.";
else
	echo "USB soundcard not found";
	exit 7
fi

if [ "`cat /boot/config.txt | grep ^dtparam=audio=off$ | wc -l`" -eq "1" ]; then
	echo "Internal sound card deactivated";
else
	echo "Internal sound card still active. Disable it in /boot/config.txt. If you just disabled it, please reboot.";
	exit 8
fi

if [ "`cat /usr/share/alsa/alsa.conf | grep 'defaults.ctl.card 1' | wc -l`" -eq "1" ]; then
	echo "Default CTL sound card is 1";
else
	echo "Default CTL sound card is still 0. Edit /usr/share/alsa/alsa.conf and set sound card to 1";
	exit 9
fi

if [ "`cat /usr/share/alsa/alsa.conf | grep 'defaults.pcm.card 1' | wc -l`" -eq "1" ]; then
        echo "Default PCM sound card is 1";
else
        echo "Default PCM sound card is still 0. Edit /usr/share/alsa/alsa.conf and set sound card to 1";
        exit 9
fi



package_check() {
	if [ "`dpkg -s $1 | grep Status | grep installed | wc -l`" -eq "1" ]; then
		echo "$1 is installed";
	else
		echo "Run sudo apt install $1";
		exit 10
	fi
}

# Pillow dependencies
package_check libjpeg-dev
package_check zlib1g-dev

# Pygame dependencies
package_check python-dev
package_check libsdl-image1.2-dev
package_check libsdl-mixer1.2-dev
package_check libsdl-ttf2.0-dev
package_check libsdl1.2-dev
package_check libsmpeg-dev
package_check python-numpy
package_check subversion
package_check libportmidi-dev
package_check ffmpeg
package_check libswscale-dev
package_check libavformat-dev
package_check libavcodec-dev

if [ "`which pip3 | wc -l`" -eq "1" ]; then
        echo "Found pip3";
else
        echo "pip3 not found";
        exit 11
fi

python_check() {
	if [ "`pip3 list --disable-pip-version-check 2>/dev/null | grep $1 | wc -l`" -gt "0" ]; then
		echo "Found python package $1";
	else
		echo "Python package $1 not found";
		exit 12
	fi
}

python_check pygame
python_check numpy
python_check Pillow
python_check luma.led-matrix
python_check luma
python_check luma.core
python_check aioredis
python_check setuptools
python_check aiohttp
python_check jinja2
python_check aiohttp-jinja2
python_check python-socketio
python_check redis

python_import() {
	if python3 -c "import $1" &> /dev/null; then
		echo "Python import $1 successful";
	else
		echo "Python import $1 failed";
		exit 13
	fi
}

python_import PIL
python_import pygame
python_import aiohttp
