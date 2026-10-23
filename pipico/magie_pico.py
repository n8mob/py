import time

import board
import digitalio


class MAGiE:
  DEBOUNCE_DELAY = 0.01  # 10 milliseconds debounce delay

  def __init__(self):
    self.IN_BUTTONS = None
    self.OUT_BITS = None
    self.next_bit = None
    self.button_states = None
    self.inputs = None
    self.current_byte = None
    self.memory = []
    self.OUT_BITS = [
      board.GP16,
      board.GP17,
      board.GP18,
      board.GP19,
      board.GP20,
      board.GP21,
      board.GP22,
      board.GP26,
    ]
    self.IN_BUTTONS = [
      board.GP13,
      board.GP14,
      board.GP15
    ]
    self.current_byte = self.load_the_lights()
    self.inputs = self.load_the_buttons()
    self.button_states = [button.value for button in self.inputs]
    self.next_bit = 0

  def load_the_lights(self):
    lights = []
    for bit_index, pin in enumerate(self.OUT_BITS):
      io_for_pin = digitalio.DigitalInOut(pin)
      io_for_pin.direction = digitalio.Direction.OUTPUT
      lights.append(io_for_pin)
      io_for_pin.value = True
      time.sleep(0.04)
      io_for_pin.value = False
    return lights

  def load_the_buttons(self):
    buttons = []
    for bit_index, pin in enumerate(self.IN_BUTTONS):
      io_for_pin = digitalio.DigitalInOut(pin)
      io_for_pin.direction = digitalio.Direction.INPUT
      io_for_pin.pull = digitalio.Pull.UP
      buttons.append(io_for_pin)
    return buttons

  def set_next_bit(self, value):
    self.current_byte[self.next_bit].value = value
    print(f'Setting bit {self.next_bit} to {value}')
    self.next_bit = (self.next_bit + 1) % len(self.current_byte)
    time.sleep(0.1)

  def reset_bits(self):
    print('Resetting bits')

    byte_value = 0
    for i, light in enumerate(self.current_byte):
      if light.value:
        byte_value |= (1 << i)
      light.value = False
      time.sleep(0.06) # a little animation effect
    self.memory.append(byte_value)
    self.next_bit = 0
    time.sleep(0.1)

  def debounce(self, button_index):
    initial_state = self.inputs[button_index].value
    time.sleep(self.DEBOUNCE_DELAY)
    return self.inputs[button_index].value == initial_state

  def update(self):
    for i in range(len(self.inputs)):
      if self.inputs[i].value != self.button_states[i]:
        if self.debounce(i):
          self.button_states[i] = self.inputs[i].value
          if i == 0 and not self.button_states[0]:
            self.set_next_bit(False)
          elif i == 1 and not self.button_states[1]:
            self.set_next_bit(True)
          elif i == 2 and not self.button_states[2]:
            self.reset_bits()


magie = MAGiE()

while True:
  magie.update()
