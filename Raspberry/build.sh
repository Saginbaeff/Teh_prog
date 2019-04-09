#!/bin/bash
sudo git clone https://github.com/raspberrypi/tools
sudo apt-get install gcc-arm-linux-gnueabihf g++-arm-linux-gnueabihf
sudo mkdir build
cd $PWD/build
sudo mkdir inst
sudo cmake $OLDPWD -DON_PI=ON -DSYSROOT=$OLDPWD/tools/arm-bcm2708/arm-rpi-4.9.3-linux-gnueabihf/arm-linux-gnueabihf/sysroot 
sudo make
sudo make DESTDIR=$PWD/inst install
sudo zip -r 'installed' $PWD/inst/
