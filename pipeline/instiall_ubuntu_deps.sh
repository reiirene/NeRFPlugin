#!/bin/bash

echo "Installing system dependencies for instant-ngp..."

sudo apt update
sudo apt install -y build-essential git cmake libglfw3-dev libglew-dev \
    libomp-dev libopenexr-dev libxi-dev libxinerama-dev libxcursor-dev \
    libpython3-dev python3-pip

echo "Done installing Ubuntu system packages!"