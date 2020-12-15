import time
import board
import digitalio

print("press the button!")

led = digitalio.DigitalInOut(board.D2)
led.direction = digitalio.Direction.OUTPUT

pir = digitalio.DigitalInOut(board.D4)
pir.direction = digitalio.Direction.INPUT
pir.pull = digitalio.Pull.UP

while True:
    led.value = pir.value # light when button is pressed!
    if pir.value == True:
        print(pir.value)
    time.sleep(1)
