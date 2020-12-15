import RPi.GPIO as GPIO
import time
import os
import sys
import subprocess

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin

trigger = False
videoPlaying = False
audioPlaying = False
videoPath = "/home/pi/Desktop/jellyfish-25-mbps-hd-h264.mkv"
audioPath = "/home/pi/Desktop/Sensing_scripts/igloo.mp3"

os.system("killall omxplayer.bin")

while True:
	i=GPIO.input(8)
	if i==1:                 #When output from motion sensor is LOW
		print ("No intruders",i)
		GPIO.output(3, 0)  #Turn OFF LED
		time.sleep(0.1)
                if trigger:
                    trigger = False
                    os.system("killall omxplayer.bin")
	elif i==0:               #When output from motion sensor is HIGH
		print ("Intruder detected",i)
		GPIO.output(3, 1)  #Turn ON LED
		if not trigger:
                    trigger = True
                    print ("now Triggered")
                    os.system("killall omxplayer.bin")
                    subprocess.Popen("omxplayer --alpha 120 --no-osd --adev local " + videoPath, shell=True)
                    subprocess.Popen("omxplayer -o hdmi " +  audioPath, shell=True)
                time.sleep(4.1)
