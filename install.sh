#!/bin/bash

echo "----- Enable I2C communication -----"
# https://www.raspberrypi.com/documentation/computers/configuration.html#i2c-nonint
sudo raspi-config nonint do_i2c 0

echo "----- Install required APT packages -----"
sudo apt update
sudo apt-get install -y \
  vim \
  libffi6 libffi-dev \
  i2c-tools \
  python3-distutils python3-dev python3-rpi.gpio \
  openssl libssl-dev \
  pkg-config

echo "----- Install Rust -----"
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sudo sh

echo "----- Install Poetry -----"
curl -sSL https://install.python-poetry.org | sudo POETRY_HOME=/opt/poetry/ python3 -

echo "----- Download code from gitlab -----"
sudo git -C /opt/halloweend pull || sudo git clone https://gitlab.com/rootmout.perso/halloweend.git /opt/halloweend

echo "----- Install python dependencies -----"
sudo /opt/poetry/bin/poetry --directory /opt/halloweend install

echo "----- Install systemd service -----"
sudo cp halloweend.service /lib/systemd/system/
sudo chmod 644 /lib/systemd/system/halloweend.service
sudo systemctl daemon-reload

echo "----- Enable and start systemd service -----"
sudo systemctl enable halloweend.service
sudo systemctl start halloweend.service