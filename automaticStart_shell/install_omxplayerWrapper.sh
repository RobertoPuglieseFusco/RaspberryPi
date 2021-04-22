#!/bin/bash

read -p "Enter Your Name: "  username
echo "Welcome $username!"

sleep 5  # Waits 5 seconds.
echo "Hello World!"

sudo apt-get update && sudo apt-get install -y libdbus-1{,-dev}
sudo apt-get install libglib2.0-dev

sudo apt install -y libdbus-1-3 libdbus-1-dev
sudo pip install omxplayer-wrapper

//sudo python3 /home/pi/Desktop/PIR_input/pir_playvideoFromStart_ControlSoundWithTrigger.py 

