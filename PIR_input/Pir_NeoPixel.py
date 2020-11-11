# Simple test for NeoPixels on Raspberry Pi

import time
import board
import digitalio
import neopixel
import adafruit_fancyled.adafruit_fancyled as fancy

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

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness= 1.0, auto_write=False, pixel_order=ORDER)

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

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


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




trigger = False
#play_music(soundfile)

led = digitalio.DigitalInOut(board.D2)
led.direction = digitalio.Direction.OUTPUT

pir = digitalio.DigitalInOut(board.D4)
pir.direction = digitalio.Direction.INPUT
pir.pull = digitalio.Pull.UP

while True:    
    
    if pir.value == False:                 #When output from motion sensor is LOW
        print ("No visitors")
        led.value = False  #Turn OFF LED
        trigger = False
    elif pir.value == True:               #When output from motion sensor is HIGH
        print ("Visitors detected")
        led.value = True  #Turn ON LED
        time.sleep(0.1)
        if not trigger:
            trigger = True  
    
    if trigger:
        trigger = False
        
        pixels.fill((0, 0, 0))
        pixels.show()
        time.sleep(1)
        pulsatingHSV(0.01, 5.0)    
        time.sleep(1)
        #rainbow_cycle(0.001)  # rainbow cycle with 1ms delay per step 
        pixels.fill((0, 0, 0))
        pixels.show()

               
    
