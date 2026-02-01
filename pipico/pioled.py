import adafruit_ssd1306
import board
import busio
import digitalio
from time import sleep

i2c = busio.I2C(board.GP1, board.GP0)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
oled.init_display()

oled.fill(0)
oled.text('<--- Click!', 2, 0, 1)
oled.show()

button = digitalio.DigitalInOut(board.GP15)
button.switch_to_input(pull=digitalio.Pull.UP)


print('waiting for button press to start animation')
while button.value:
  sleep(0.12)

oled.fill(1)
oled.show()
sleep(0.1)
oled.fill(0)
oled.show()
sleep(0.5) # debounce delay

# loop until button is pressed again
frame = 0
while True:
  frame_seconds = 2.7
  if frame == 0:
    oled.fill(0)

    oled.text("They're trashing", 8, 0, 1)
    oled.show()
    sleep(frame_seconds / 6)

    oled.text("our rights!", 20, 14, 1)
    oled.show()
    sleep(frame_seconds)

    frame += 1
  elif frame == 1:
    oled.fill(0)

    oled.text("They're trashing", 8, 4, 1)
    oled.show()
    sleep(frame_seconds / 6)

    oled.text("the flow of data!", 6, 18, 1)
    oled.show()
    sleep(frame_seconds)

    frame += 1
  elif frame == 2:
    oled.fill(0)

    oled.text("They're trashing!", 8, 0, 1)
    oled.show()
    sleep(frame_seconds / 3)

    oled.text("Trashing!!", 20, 16, 1)
    oled.show()
    sleep(frame_seconds)

    frame += 1
  elif frame == 3:
    oled.fill(0)
    oled.text("Hack the planet!", 5, 4, 1)
    oled.show()
    sleep(frame_seconds / 2)
    frame += 1
  elif frame == 4:
    oled.fill(0)
    oled.text("Hack", 10, 2,1)
    oled.show()
    sleep(frame_seconds / 6)
    oled.text("the", 30, 12, 1)
    oled.show()
    sleep(frame_seconds / 6)
    oled.text("planet!", 50, 24, 1)
    oled.show()

    frame = 0
    sleep(frame_seconds)

print('button pressed, stopping animation')
oled.fill(0)
oled.text("Goodbye!", 32, 12, 1)
