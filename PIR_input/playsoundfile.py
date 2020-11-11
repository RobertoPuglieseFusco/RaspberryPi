#!/usr/bin/python

import sys
import pygame as pg
import os
import time

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

        

freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 2048   # number of samples (experiment to get right sound)
pg.mixer.init(freq, bitsize, channels, buffer)
# optional volume 0 to 1.0
pg.mixer.music.set_volume(1.0)

soundfile =  "/home/pi/Tomasz/igloo.mp3"
#soundfile =  "/home/pi/Desktop/SnareSamp.mp3"

play_music(soundfile)

clock = pg.time.Clock()

while pg.mixer.music.get_busy():
	clock.tick(30)
	timelinePos = pg.mixer.music.get_pos()
	print(timelinePos)
	if timelinePos > 5000:
		print("let's stop after 5 seconds")
		pg.mixer.music.stop()

	
