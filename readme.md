# halloweend 🎃

## About

Halloween Daemon (halloweend) is a simple program to manage and animate groups of LEDs that form a decoration representing eyes in the night.
Each group of two leds will blink, turn on and turn off to behave as close as possible to what eyes do.

<div align="center">
<img src="https://gitlab.com/rootmout.perso/halloweend/-/raw/main/images/result_by_night.jpg" width="100%">
</div>

## Hardware

The rest of this page will explain what I used to build a setup with 16 groups of leds (16 being the number of outputs of the PWM controller).

### Bill of Material (BOM)
| ID | Part ref            | Nbr | Description    |
|----|---------------------|-----|----------------|
| 1  | Raspberry Pi Zero W | 1   | Computer       |
| 2  | PCA9685             | 1   | PWM module     |
| 3  | RND 135-00155       | 32  | Red led        |
| 4  | PN2222ABU           | 16  | NPN Transistor |
| 5  | 75 Ohm resistor     | 16  | Resistor       |

Also consider to have:
- a prototype PCB
- a 12v power supply
- terminale poles

### Schematic
The above represent the wiring for only two groups of led but the pattern is the same for more groups.
<div align="center">
<img src="https://gitlab.com/rootmout.perso/halloweend/-/raw/main/images/shematic.png" width="100%">
</div>
The PWM controller bord is shipped with a power regulator that provide a 5v current from an input (VCC) between 5 and 12v. 
To power 32 leds this regulator will perfectly do the job. Note that it will also supply the raspberry pi.

## Software

The code is implemented in python and use poetry as dependency manager. You can use the official Raspberry Pi Imager tool
to provision the raspberry with an OS preconfigured to connect to your WIFI network.

### Installation
SSH into the Raspberry PI and run the above command.
```shell
# This will download the installation script which will:
# - enable I2C communication
# - install required apt dependencies
# - download the source code
# - create, enable and start a systemd service
curl -sSL https://gitlab.com/rootmout.perso/halloweend/-/raw/main/install.sh | sh
```

Once the installation script is complete, the halloweend service start and if your raspberry pi is connected
to the PWM module (and that it's night) you should see animations.

Usefull commands to debug:
```shell
# Check the I2C interface see the PWM module, a normal output looks like that:
# rootmout@raspberrypi:~ $ sudo i2cdetect -y 1
#      0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
# 00:                         -- -- -- -- -- -- -- --
# 10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 40: 40 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# 70: -- -- -- -- -- -- -- --
sudo i2cdetect -y 1

# See systemd service status, normal behavior looks like:
# rootmout@raspberrypi:~ $ sudo systemctl status halloweend.service 
# ● halloweend.service - halloweend Service
#      Loaded: loaded (/lib/systemd/system/halloweend.service; enabled; vendor preset: enabled)
#      Active: active (running) since Sun 2023-10-29 04:40:07 CET; 10h ago
# [...]
sudo systemctl status halloweend.service
```


# Sources
- https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython
- https://www.berrybase.de/en/16-kanal-servo-driver-uhat-i2c-fuer-raspberry-pi