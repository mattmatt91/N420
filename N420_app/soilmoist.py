import time
import RPi.GPIO as GPIO
import numpy as np
from threading import Thread


class SoilMoist():

    GPIO.setmode(GPIO.BCM)
    sample_cycle = 3
    sensors = []


    def __init__(self, pin, name):
        print('starting soilmoist sensor...')
        GPIO.setup(pin, GPIO.IN,GPIO.PUD_UP)
        self.pin = pin
        self.counts = 0
        self.name = name
        self.flag = False
        SoilMoist.sensors.append(self)

        self.start_loop()

    
    def loop(self):
        while True:
            last = time.time()
            counts = 2
            while time.time() <= last + SoilMoist.sample_cycle:
                if GPIO.input(self.pin) == 0 and self.flag:
                    counts += 1
                    self.flag = False
                    
                elif GPIO.input(self.pin) == 1 and not self.flag:
                    self.flag = True
                else:
                    pass

            last = time.time()
            self.counts = counts
    
    def start_loop(self):
        Thread(target=self.loop).start()

    def get_values(self):
        return self.counts

    @classmethod
    def get_data(cls):
        data = {}
        sensors = cls.sensors
        for sensor in sensors:
            data[sensor.name] = sensor.get_values()
        return data
        

    
if __name__ == '__main__':
    
    SoilMoist(11, 'soil1')
    SoilMoist(9, 'soil2')
    while True:
        time.sleep(2.5)
        print(SoilMoist.get_data())


            
    

            


