#!/bin/bash

read -p "Enter Your Name: "  username
echo "Welcome $username!"

sleep 5  # Waits 5 seconds.
echo "Hello World!"
python /home/pi/Desktop/PIR_input/pir_loopingVideo_unmuteSound_muteAtTheEnd.py
