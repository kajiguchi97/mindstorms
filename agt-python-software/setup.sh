#!/bin/bash

# exit on error
set -e

echo
echo -e "+--------------------------------------------------------------------+"
echo -e "| \033[0;34m   .oooooooo.   \033[0m             888                                   |"
echo -e "| \033[0;34m  d8P'    'Y8b  \033[0m   .oooo.    888   .ooooo.  oooo    ooo  .oooo.    |"
echo -e "| \033[0;34m 888        888 \033[0m  'P  )88b   888  d88' '88b  '88b..8P'  'P  )88b   |"
echo -e "| \033[0;34m 888        888 \033[0m   .oP'888   888  888ooo888    Y888'     .oP'888   |"
echo -e "| \033[0;34m '88bb    dd88' \033[0m  d8(  888   888  888    .o  .o8''88b   d8(  888   |"
echo -e "| \033[0;34m  'Y8bb,ood8P'  \033[0m  'Y888888o  888o 'Y8bod8P' o88'   888o 'Y888888o  |"
echo -e "+--------------------------------------------------------------------+"
echo

echo -e "Starting Alexa Gadgets Python Software setup..."

# update and install the latest system updates and install necessary bluetooth libraries
sudo apt-get -y update

sudo apt-get -y install bluetooth libbluetooth-dev libudev-dev bluez-hcidump

# add user to 'bluetooth' group
sudo usermod -a -G "bluetooth" "$USER"

# install pip
sudo apt-get -y install python3-pip
pip3 install --upgrade pip

# install protobuf
sudo pip3 install protobuf

# install agt library
sudo pip3 install -e src

# reboot
echo
echo -e "\033[0;32m+------------------------------+\033[0m"
echo -e "\033[0;32m|            SUCCESS           |\033[0m"
echo -e "\033[0;32m+------------------------------+\033[0m"
echo
read -p "Press any key to reboot to complete setup"
sudo reboot