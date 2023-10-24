# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# This simple test outputs a 50% duty cycle PWM single on the 0th channel. Connect an LED and
# resistor in series to the pin to visualize duty cycle changes and its impact on brightness.

from board import SCL, SDA
import busio
import time
from datetime import datetime
import random

# Import the PCA9685 module.
from adafruit_pca9685 import PCA9685

# Create the I2C bus interface.
i2c_bus = busio.I2C(SCL, SDA)

# Create a simple PCA9685 class instance.
pca = PCA9685(i2c_bus)

# Set the PWM frequency to 60hz.
pca.frequency = 60

# Define the start and end hours for daytime
day_start_hour = 8  # 8:00 AM
day_end_hour = 19  # 7:00 PM

# # Set all channels to 20% duty cycle
# for channel in range(16):
#     pca.channels[channel].duty_cycle = 2048  # 20% of the full range

brightnessHeight = 20
transitionSpeed = 0.3
nextBlink = [0] * 16
turnOn = []
turnOff = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

def turn_all_off(pca):
    for ch in range(16):
        pca.channels[ch].duty_cycle = 0  # All to 0%


nextOnOffSession = 1
while True:
    time.sleep(0.1)
    nextOnOffSession -= 1
    if nextOnOffSession < 0:
        nextOnOffSession = random.randint(3, 7) * 10
        print("-----")
        print("session duration: ", nextOnOffSession / 10, "sec")

        # Get the current time
        current_hour = time.localtime().tm_hour

        is_daytime = day_start_hour <= current_hour < day_end_hour

        if is_daytime:
            print("now: ", current_hour, "| is day time: all leds OFF")
            turn_all_off(pca)
            time.sleep(10)
            continue

        numberToTurnOn = random.randint(-3, 3)
        print("nbr to turn ON: ", numberToTurnOn)
        if numberToTurnOn > 0:
            # Move x numbers from list one to list two
            for _ in range(numberToTurnOn):
                if turnOff:
                    number = random.choice(turnOff)
                    turnOff.remove(number)
                    turnOn.append(number)
                else:
                    break
        elif numberToTurnOn < 0:
            # Move -x numbers from list two to list one
            for _ in range(-numberToTurnOn):
                if turnOn:
                    number = random.choice(turnOn)
                    turnOn.remove(number)
                    turnOff.append(number)
                else:
                    break
        print("Leds ON: ", turnOn)
        print("Leds OFF: ", turnOff)

    for _, channel in enumerate(turnOn):
        nextBlink[channel] -= 1
        brightness = brightnessHeight
        if nextBlink[channel] < -5:
            nextBlink[channel] = random.randint(7,17)*10
        if nextBlink[channel] < 0:
            brightness += nextBlink[channel] * 10
        if brightness < 0:
            brightness = 0
        pca.channels[channel].duty_cycle = brightness * 600

    for _, channel in enumerate(turnOff):
        pca.channels[channel].duty_cycle = 0