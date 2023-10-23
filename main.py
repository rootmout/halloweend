# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This simple test outputs a 50% duty cycle PWM single on the 0th channel. Connect an LED and
# resistor in series to the pin to visualize duty cycle changes and its impact on brightness.

from board import SCL, SDA
import busio
import time

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)

# Set the PWM frequency to 60hz.
pca.frequency = 60

# Set all channels to 20% duty cycle
for channel in range(16):
    pca.channels[channel].duty_cycle = 2048  # 20% of the full range


# Set the PWM duty cycle for channel zero to 50%. duty_cycle is 16 bits to match other PWM objects
# but the PCA9685 will only actually give 12 bits of resolution.
while True:
    for channel in range(16):
        # Increase duty cycle to 20% over 3 seconds

        #time.sleep(3)  # Wait for 3 seconds

        # Decrease duty cycle to 0 over 1 second
        for duty_cycle in range(4096, -1, -1000):
            pca.channels[channel].duty_cycle = duty_cycle
            time.sleep(0.1)  # Adjust this for the desired rate of change

        # Increase back to 20% over 3 seconds
        for duty_cycle in range(0, 4096, 1000):
            pca.channels[channel].duty_cycle = duty_cycle
            time.sleep(0.15)  # Adjust this for the desired rate of change

        #time.sleep(3)  # Wait for 3 seconds
