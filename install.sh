#!/bin/bash

sudo apt clean
sudo apt autoclean
sudo apt update
sudo apt -y upgrade
sudo apt -y dist-upgrade
sudo apt clean
sudo apt autoclean
sudo apt -y install python3 python3-pip
pip3 install pygame