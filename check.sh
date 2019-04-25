#!/bin/bash

reboot_required=no
connect_usbsound=no

# Make Java compatible with PyCharm
if [ "`java -version 2>&1 | grep version | grep 1.8.0_65 | wc -l`" -eq "1" ]; then
    echo "Java is problematic Oracle version 1.8.0.65."
    echo "Switching to OpenJDK Ice-T version"
    apt-get purge -y oracle*
    apt-get update
    apt-get upgrade
    apt-get remove -y oracle*
    apt-get install -y openjdk-8-jre
    if [ "`java -version 2>&1 | grep version | grep 1.8.0_65 | wc -l`" -eq "0" ]; then
        echo "Java update seems good."
    else
        echo "Java is still 1.8.0_65."
        echo "Do you have an active Internet connection?"
        exit 3
    fi
else
    echo "Java is not the broken version 1.8.0.65. Probably fine. Leaving as is.";
fi

# Back up config files
cp /boot/config.txt /boot/config.txt$(date +%Y%m%d)
cp /usr/share/alsa/alsa.conf /usr/share/alsa/alsa.conf$(date +%Y%m%d)

# SPI checks
if [ "`raspi-config nonint get_spi`" -eq "1" ]; then
    echo "SPI seems enabled (reported by raspi-config)";
else
    echo "SPI seems disabled (reported by raspi-config). Enabling now.";
    raspi-config nonint do_spi 0
    reboot_required=yes
fi

if [ "`cat /boot/config.txt |grep ^dtparam=spi=on$| wc -l`" -eq "1" ]; then
	echo "SPI seems enabled (/boot/config.txt)";
else
	echo "SPI seems disabled. Enable it in raspi-config and reboot";
	sed -i -e "s/dtparam=spi=off/dtparam=spi=on/g" /boot/config.txt
    reboot_required=yes
fi

if [ "`lsmod | grep spi_bcm2835 | wc -l`" -eq "1" ]; then
	echo "SPI is already active";
else
	echo "SPI does not seem active yet. If you just enabled it, a reboot is required";
	reboot_required=yes
fi

if [[ -e /dev/spidev0.0 ]]; then
	echo "SPI kernel device found";
else
	echo "No SPI kernel device found";
	reboot_required=yes
fi

# Audio checks
if [ "`cat /boot/config.txt | grep ^dtparam=audio=off$ | wc -l`" -eq "1" ]; then
	echo "Internal sound card is deactivated.";
else
	echo "Internal sound card still active. Disabling it in /boot/config.txt.";
	sed -i -e "s/dtparam=audio=off/dtparam=audio=off/g" /boot/config.txt
    reboot_required=yes
fi

if [ "`cat /proc/asound/modules | wc -l`" -gt "1" ]; then
	echo "Too many sound cards found. Disable internal sound card in /boot/config.txt. If you just disabled it, please reboot."
	reboot_required=yes
fi

if [ "`cat /proc/asound/modules | grep usb | wc -l`" -eq "1" ]; then
    echo "USB soundcard found.";
else
	echo "USB soundcard not found in /proc/asound/modules. Please connect the USB sound card.";
	connect_usbsound=yes
fi

if [ "`cat /proc/asound/cards | grep USB | wc -l`" -gt "1" ]; then
	echo "USB soundcard found.";
else
	echo "USB soundcard not found";
	connect_usbsound=yes
fi


if [ "`cat /usr/share/alsa/alsa.conf | grep 'defaults.ctl.card 1' | wc -l`" -eq "1" ]; then
	echo "Default CTL sound card is 1";
else
	echo "Default CTL sound card is still 0 in /usr/share/alsa/alsa/alsa.conf.";
	echo "Setting CTL sound card to 1";
	sed -i -e "s/defaults.ctl.card 0/defaults.ctl.card 1" /usr/share/alsa/alsa.conf
fi

if [ "`cat /usr/share/alsa/alsa.conf | grep 'defaults.pcm.card 1' | wc -l`" -eq "1" ]; then
    echo "Default PCM sound card is 1";
else
    echo "Default PCM sound card is still 0 in /usr/share/alsa/alsa.conf";
    echo "Setting PCM sound card to 1";
    sed -i -e "s/defaults.pcm.card 0/defaults.pcm.card 1" /usr/share/alsa/alsa.conf
fi


package_check() {
	if [ "`dpkg -s $1 | grep Status | grep installed | wc -l`" -eq "1" ]; then
		echo "$1 is installed";
	else
		echo "Package $1 is not installed. Installing now...";
		apt install $1
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
package_check python3-pip

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
		echo "Python package $1 not found. Installing ...";
		pip3 install $1
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
python_import random
python_import pickle
python_import datetime
python_import threading
python_import signal
python_import time
python_import luma.core
python_import luma.core.virtual
python_import luma.core.render
python_import luma.led_matrix.device
python_import luma.core.legacy.font
python_import luma.core.interface.serial
python_import colorsys
python_import os
python_import jinja2
python_import aiohttp_jinja2
python_import socketio

if [ "$reboot_required" -eq "yes" ]; then
    echo "A reboot seems required";
fi

if [ "$connect_usbsound" -eq "yes" ]; then
    echo "The USB sound card seems not connected. Please connect.";
fi