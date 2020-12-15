import RPi.GPIO as GPIO
import time
import os
import sys
import subprocess

from omxplayer.player import OMXPlayer
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin

trigger = False
videoPlaying = False
audioPlaying = False
VIDEO_PATH = "/home/pi/Desktop/EVERYTHING_IS_URGENT_RAN SLAVIN.mov"
#VIDEO_PATH = "/home/pi/Desktop/ETUDES.mp4"
#audioPath = "/home/pi/Desktop/Sensing_scripts/igloo.mp3"


sound_length_on_trigger = 1

os.system("killall omxplayer.bin")

player = OMXPlayer(VIDEO_PATH, args=['--no-osd', '--loop'], dbus_name='org.mpris.MediaPlayer2.omxplayer1')
sleep(2.5)
player.set_video_pos(200, 200, 800, 699)
player.set_volume = 0
player.set_alpha(120)
player.pause()
player.set_position(0)
#player.set_video_pos(0, 0, 1920, 1080)
# it takes about this long for omxplayer to warm up and start displaying a picture on a rpi3

player.play()
player.mute()

while True:
    i=GPIO.input(8)
    if i==1:                 #When output from motion sensor is LOW
        print ("No intruders",i)
        GPIO.output(3, 0)  #Turn OFF LED
        time.sleep(0.1)
        if trigger:
            trigger = False
            player.mute()
    elif i==0:               #When output from motion sensor is HIGH
        print ("Intruder detected",i)
        GPIO.output(3, 1)  #Turn ON LED
        if not trigger:
            trigger = True
            print ("now Triggered")
            #os.system("killall omxplayer.bin")
            player.unmute()                    
            time.sleep(sound_length_on_trigger)

