from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

pump = 27
valve1 = 17
valve2 = 22
GPIO.setup(pump, GPIO.OUT)
GPIO.output(pump, False)
GPIO.setup(valve1, GPIO.OUT)
GPIO.output(valve1, False)
GPIO.setup(valve2, GPIO.OUT)
GPIO.output(valve2, False)

