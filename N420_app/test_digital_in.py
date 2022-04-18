#!/usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time

KEY = 11 # 9
# pin numbers are interpreted as BCM pin numbers.
GPIO.setmode(GPIO.BCM)
# Sets the pin as input and sets Pull-up mode for the pin.

GPIO.setup(KEY,GPIO.IN,GPIO.PUD_UP)
while True:
    time.sleep(0.05)
    if GPIO.input(KEY) == 0:
            print("KEY PRESS:", KEY)
            while GPIO.input(KEY) == 0:
                time.sleep(0.01)

            


