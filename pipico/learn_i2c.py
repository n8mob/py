import time

import board
import busio
import digitalio
from busio import I2C

PIN = board.D18


def say_hello():
    print('Hello, blinka!')
    led = digitalio.DigitalInOut(PIN)
    led.direction = digitalio.Direction.OUTPUT
    while True:
        led.value = True
        time.sleep(0.5)
        led.value = False
        time.sleep(0.5)


say_hello()

i2c_channel = busio.I2C(2, 1)

device_addresses = i2c_channel.scan()

for device_address in device_addresses:
    print(f'i2c at [{device_address}]')
