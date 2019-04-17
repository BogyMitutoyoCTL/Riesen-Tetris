#!/bin/bash
cd /home/pi/Riesen-Tetris/
echo Tetris Bash Script
pwd
python3 webserver.py &
python3 MAIN.py

