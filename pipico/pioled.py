import board
import busio

# get adafruit_ssd1306 from the lib folder
import adafruit_ssd1306

i2c = busio.I2C(board.GP1, board.GP0)
oled = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# clear the display
oled.fill(0)
oled.show()

oled.pixel(0, 0, 1)
oled.pixel(64, 16, 1)
oled.pixel(127, 31, 1)
oled.show()
