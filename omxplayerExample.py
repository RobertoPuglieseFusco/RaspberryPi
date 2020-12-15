#!/usr/bin/env python3

from omxplayer.player import OMXPlayer
from time import sleep

VIDEO_PATH = "/home/pi/Desktop/jellyfish-25-mbps-hd-h264.mkv"

player = OMXPlayer(VIDEO_PATH, dbus_name='org.mpris.MediaPlayer2.omxplayer1')
player.set_video_pos(200, 200, 800, 699)
player.pause()
player.set_position(0)
player.set_video_pos(0, 0, 1920, 1080)
# it takes about this long for omxplayer to warm up and start displaying a picture on a rpi3
sleep(1.5)
player.play()

while player.playback_status() == "Playing":
    player.set_alpha(player.position()*25)
    print(player.position())
    if player.position() > 10:
        player.pause()

sleep(5)

player.quit()