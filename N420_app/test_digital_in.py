import time
import RPi.GPIO as GPIO

# Pins definitions
btn_pins = [i for i in range(30)]


# Set up pins
GPIO.setmode(GPIO.BCM)


# If button is pushed, light up LED
last_check =time.time()
buffer =  0
last_value = False
sample_cycle = 1
print(time.time())
time.sleep(1)
print(btn_pins)
for btn_pin in btn_pins:
    flag = True
    while flag:
        GPIO.setup(btn_pin, GPIO.IN)
        if GPIO.input(btn_pin) and not last_value:
            buffer += 1
        if not GPIO.input(btn_pin) and last_value:
            last_value = False
        if time.time() - last_check >= sample_cycle:
            print(btn_pin, '  ', buffer)
            buffer = 0
            last_check = time.time()
            flag = False
    

            


