#!/usr/bin/env python3

from omxplayer.player import OMXPlayer
from pathlib import Path
from time import sleep
import logging
logging.basicConfig(level=logging.INFO)


VIDEO_1_PATH = "/home/pi/Desktop/video.mp4"
player_log = logging.getLogger("Player 1")

player = OMXPlayer(VIDEO_1_PATH, 
        dbus_name='org.mpris.MediaPlayer2.omxplayer1')

#args=['--no-osd','--no-keys','-b','--loop','--display=2','-o','local'])

player.playEvent += lambda _: player_log.info("Play")
player.pauseEvent += lambda _: player_log.info("Pause")
player.stopEvent += lambda _: player_log.info("Stop")

# it takes about this long for omxplayer to warm up and start displaying a picture on a rpi3
sleep(2.5)

player.set_position(5)
player.pause()


sleep(2)

player.set_aspect_mode('stretch')
player.set_video_pos(0, 0, 200, 200)
player.play()

sleep(5)

player.quit()