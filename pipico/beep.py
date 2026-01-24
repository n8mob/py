import time
import board
import digitalio

BOARD_LED = board.GP25


def blink_when_press():
  led = digitalio.DigitalInOut(BOARD_LED)
  led.direction = digitalio.Direction.OUTPUT

  button = digitalio.DigitalInOut(board.GP15)
  button.switch_to_input(pull=digitalio.Pull.UP)

  while True:
    button_is_pulled_up = button.value
    led.value = not button_is_pulled_up
    time.sleep(0.1)

blink_when_press()
