import RPi.GPIO as GPIO
import time
import os
import sys
import pygame as pg


def play_music(music_file):
    '''
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    '''
    clock = pg.time.Clock()
    try:
        pg.mixer.music.load(music_file)
        print("Music file {} loaded!".format(music_file))
    except pg.error:
        print("File {} not found! {}".format(music_file, pg.get_error()))
        return

    pg.mixer.music.play()
    
    # for x in range(0,100):
    #     pg.mixer.music.set_volume(float(x)/100.0)
    #     time.sleep(.0075)
    # # check if playback has finished
    while pg.mixer.music.get_busy():
        clock.tick(30)

freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 2048   # number of samples (experiment to get right sound)
pg.mixer.init(freq, bitsize, channels, buffer)
# optional volume 0 to 1.0
pg.mixer.music.set_volume(1.0)
soundfile =  "igloo.mp3"

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin

trigger = False

while True:
	i=GPIO.input(8)
	if i==0:                 #When output from motion sensor is LOW
		print ("No intruders",i)
		GPIO.output(3, 0)  #Turn OFF LED
		time.sleep(0.1)
		trigger = False
	elif i==1:               #When output from motion sensor is HIGH
		print ("Intruder detected",i)
		GPIO.output(3, 1)  #Turn ON LED
		time.sleep(0.1)
		if not trigger:
			trigger = True			
	if trigger:
		trigger = False
		play_music(soundfile)
		
