import adafruit_ssd1306
import board
import busio


class OledUI:
  """Simple OLED UI for displaying Morse code characters and words.
  From PyCharm AI Chat (model is set to "Auto"... not sure which one it used...)
  """
  def __init__(self, width=128, height=32, scl=board.GP1, sda=board.GP0):
    i2c = busio.I2C(scl, sda)
    self.oled = adafruit_ssd1306.SSD1306_I2C(width, height, i2c)
    self.oled.fill(0)
    self.oled.show()

  def update(self, morser):
    # Simple two-line display for 128x32: 16 chars per line at the default font size.
    text = " ".join(morser.word_buffer) + " " + "".join(morser.char_buffer)
    line1 = text[-16:]  # keep it simple; could be smarter with wrapping
    line2 = text[:-16] if len(text) > 16 else ""

    self.oled.fill(0)
    self.oled.text(line1, 0, 0, 1)
    self.oled.text(line2, 0, 16, 1)
    self.oled.show()
