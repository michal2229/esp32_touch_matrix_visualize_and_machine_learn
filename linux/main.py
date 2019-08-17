#!/usr/bin/env python3

## Ubuntu 19.04:
# sudo adduser $USER dialout  # for connecting to serial without root privileges
# sudo reboot
# sudo apt install python3-opencv  # OpenCV 3.2
# sudo apt install python3-pip
# pip3 install numpy
# pip3 install pyserial
# pip3 install esptool
# pip3 install thonny  # for ESP32 Micropython development, very handy in recent version
# # There is also PyCharm Micropython plugin for deploy, but Thonny can read, edit and save files residing on board.

import serial as ser
import cv2
import numpy as np

fps = 12
sec = 10
nsensors = 9

T = np.zeros((fps * sec, nsensors))  # our input for NN  # TODO: make NN
mavg = None  # moving average of measurements, for detecting changes

with ser.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:  # Linux specific, "COMx" on Windows, or something like that
    while True:
        line = ser.readline().decode("utf-8", "strict")  # reading serial data from ESP32
        try:
            measurement = eval(line)['m']  # getting measurement vector
            mimage = np.array(measurement)  # making numpy array from measurements

            # some preprocessing
            mimage = mimage / 1024
            if mavg is None:
                mavg = mimage
            mavg = mimage / 32 + mavg * 31 / 32
            mm = mavg - mimage
            mm *= 32
            mm += 0.5
            mm[mm < 0] = 0
            mm[mm > 1] = 1

            T = np.roll(T, 1, axis=0)  # rolling T matrix down
            T[0] = mm  # putting sensor data to the top; T is now ready

            cv2.imshow('image', cv2.resize(np.array(T * 255, dtype=np.uint8), None, fx=96, fy=96 * nsensors / fps / sec,
                                           interpolation=cv2.INTER_NEAREST))
            cv2.waitKey(1)
            print(mm)
        except:
            continue
