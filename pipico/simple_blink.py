import time

import board
import digitalio

BOARD_LED = board.GP25


def blink_led():
  led = digitalio.DigitalInOut(BOARD_LED)
  led.direction = digitalio.Direction.OUTPUT
  while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)


blink_led()
