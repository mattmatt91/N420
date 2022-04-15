import time
import RPi.GPIO as GPIO
import numpy as np
from threading import Thread


class SoilMoist():

    GPIO.setmode(GPIO.BCM)
    sample_cycle = 1
    sensors = []


    def __init__(self, pin, name):
        print('starting soilmoist sensor...')
        GPIO.setup(pin, GPIO.IN)
        self.pin = pin
        self.counts = 0
        self.name = name
        SoilMoist.sensors.append(self)

        self.start_loop()

    
    def loop(self):
        while True:
            last = time.time()
            counts = 0
            while time.time() <= last + SoilMoist.sample_cycle:
                GPIO.wait_for_edge(self.pin, GPIO.FALLING)
                counts += 1
            last = time.time()
            self.counts = counts
            print(self.counts)
    
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
        print(data)

    
if __name__ == '__main__':
    sensor1 = SoilMoist(5, 'soil1')
    sensor1 = SoilMoist(25, 'soil2')
    for i in range(10):
        time.sleep(1)
        SoilMoist.get_data()


            
    

            


