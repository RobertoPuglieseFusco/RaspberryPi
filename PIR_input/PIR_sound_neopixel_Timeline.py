# Simple test for NeoPixels on Raspberry Pi

import time
import board
import digitalio
import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy
import threading
import sys
import pygame as pg
import os

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 60

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness= 0.5, auto_write=False, pixel_order=ORDER)

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


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

def pulsatingHSV(wait, gValue):
    for j in range(256):
        for i in range(num_pixels):
            colorHSV = fancy.CHSV(0.5, 1.0, j/255.)  # CYAN
            colorRGB = fancy.CRGB(colorHSV)
            #print(colorHSV.hue, colorHSV.saturation, colorHSV.value)
            #print("ramp up ", colorRGB.red, colorRGB.green, colorRGB.blue)
            #pixels.fill(colorRGB.red, colorRGB.green, colorRGB.blue)
            colorGamma = fancy.gamma_adjust(colorHSV, gamma_value=gValue)
            pixels[i] = colorGamma.pack()
        pixels.show()
        time.sleep(wait)
    for j in range(256):
        for i in range(num_pixels):
            colorHSV = fancy.CHSV(0.5, 1.0, 1.0 - j/255.)  # CYAN
            #print(colorHSV.hue, colorHSV.saturation, colorHSV.value)
            colorRGB = fancy.CRGB(colorHSV)
            #print("ramp down ", colorRGB.red, colorRGB.green, colorRGB.blue)
            colorGamma = fancy.gamma_adjust(colorHSV, gamma_value=gValue)
            pixels[i] = colorGamma.pack()
        pixels.show()
        time.sleep(wait)

def lerp(a, b, f):
   return a + f*(b-a)


def rampLight(startValueR, startValueG, startValueB, endValueR, endValueG, endValueB, deltaTime):
    timeSlice = 0.01
    stepDelta = timeSlice / deltaTime
    print(stepDelta)
    stepIncrement = 0.0
    while stepIncrement <= 1:
        r = lerp(startValueR,endValueR, stepIncrement)
        g = lerp(startValueG,endValueG, stepIncrement)
        b = lerp(startValueB,endValueB, stepIncrement)
        pixels.fill((int(r), int(g), int(b)))
        pixels.show()
        #print("current color " + str(int(r)) + " " + str(int(g)) + " " + str(int(b)))
        stepIncrement = stepIncrement + stepDelta
        if(stepIncrement >= 1):
            print("reached color " + str(endValueR) + " " + str(endValueG) + " " + str(endValueB))
        time.sleep(timeSlice * 0.5)

freq = 44100    # audio CD quality
bitsize = -16   # unsigned 16 bit
channels = 2    # 1 is mono, 2 is stereo
buffer = 2048   # number of samples (experiment to get right sound)
pg.mixer.init(freq, bitsize, channels, buffer)
# optional volume 0 to 1.0
pg.mixer.music.set_volume(1.0)

soundfile =  "/home/pi/Tomasz/Black_box_reaper_rough.mp3"
trigger = False
#play_music(soundfile)

led = digitalio.DigitalInOut(board.D2)
led.direction = digitalio.Direction.OUTPUT

pir = digitalio.DigitalInOut(board.D4)
pir.direction = digitalio.Direction.INPUT
pir.pull = digitalio.Pull.UP

keyframesColors = [[0, 20, 20, 20], [2, 20, 20, 20], [10, 243,216,216], [20, 47,44,44], [30, 185,196,187], [40, 187,205,71], [50, 217,250,3], [60, 250,168,3], [70, 155,145,126], [80, 247,89,110], [90, 85,216,214],
                   [100, 221, 247, 89], [105, 247, 89, 89], [110, 0, 0, 0], [120, 182, 99, 149], [130, 68, 46, 128], [140, 119, 116, 125], [155, 195, 172, 82], [160, 0, 0, 0], [167, 255, 205, 0], [180, 20, 20, 20]]
keyframesFlag = [False] * len(keyframesColors)
for i in range(len(keyframesFlag)):
    keyframesFlag[i] = False

keyframesTimes = (2, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 105, 110, 120, 130, 140, 155, 160, 167, 180  )

indexKeyFrame = 0
x = threading.Thread(target=rampLight, args=(0,0,0,0,0,0,0))

while True:
    try:
        if pir.value == False:                 #When output from motion sensor is LOW
            print ("No visitors")
            led.value = False  #Turn OFF LED
            trigger = False
        elif pir.value == True:               #When output from motion sensor is HIGH
            print ("Visitors detected")
            led.value = True  #Turn ON LED
            time.sleep(0.1)
            if not trigger and not pg.mixer.music.get_busy():
                trigger = True

        if trigger:
            print("play music")
            play_music(soundfile)
            clock = pg.time.Clock()
            trigger = False

        if not pg.mixer.music.get_busy():
            print("music not busy")
            trigger = False
            pixels.fill((0, 0, 0))
            pixels.show()
        #pixels.fill((0, 0, 0))
        #pixels.show()
        #time.sleep(1)
        #pulsatingHSV(0.01, 5.0)
        #time.sleep(1)
        #rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step


        while pg.mixer.music.get_busy():
            clock.tick(100)
            timelinePos = pg.mixer.music.get_pos()
            #print("timelinePos " + str(timelinePos))
            if indexKeyFrame < len(keyframesFlag) - 1:
                if (timelinePos > keyframesColors[indexKeyFrame][0]*1000 and keyframesFlag[indexKeyFrame+1] == False):

                    x = threading.Thread(target=rampLight, args=(keyframesColors[indexKeyFrame][1], keyframesColors[indexKeyFrame][2], keyframesColors[indexKeyFrame][3],
                                                                 keyframesColors[indexKeyFrame+1][1], keyframesColors[indexKeyFrame+1][2], keyframesColors[indexKeyFrame+1][3],
                                                                 (keyframesColors[indexKeyFrame+1][0]-keyframesColors[indexKeyFrame][0])))
                    x.start()
                    print("started " + str(indexKeyFrame + 1) + " keyframe")
                    indexKeyFrame = indexKeyFrame + 1
                    keyframesFlag[indexKeyFrame] = True


        if indexKeyFrame == len(keyframesFlag)-1 and not pg.mixer.music.get_busy():
            print("we reached the end of the timeline and we wait a little bit")
            time.sleep(5)
            indexKeyFrame = 0
            for i in range(len(keyframesFlag)):
                keyframesFlag[i] = False


    except KeyboardInterrupt:
            # if user hits Ctrl/C then exit
            # (works only in console mode)
            pg.mixer.music.fadeout(1000)
            pg.mixer.music.stop()
            raise SystemExit
