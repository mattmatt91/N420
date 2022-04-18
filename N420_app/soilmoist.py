
import time
import RPi.GPIO as GPIO
import numpy as np
from threading import Thread


class SoilMoist():
    # raw values:
    # air : 2000 - 3500
    # dry = 350 - 500
    # moist = 200


    GPIO.setmode(GPIO.BCM)
    sample_cycle = 3
    sensors = []


    def __init__(self, pin, name):
        GPIO.setup(pin, GPIO.IN,GPIO.PUD_UP)
        self.pin = pin
        self.offset_dry = 500
        self.offfset_moist = 200
        self.counts = 0
        self.name = name
        self.flag = False
        self.last_values = []
        SoilMoist.sensors.append(self)

        self.start_loop()

    
    def loop(self):
        while True:
            last = time.time()
            counts = 0
            while time.time() <= last + SoilMoist.sample_cycle:
                if GPIO.input(self.pin) == 0 and self.flag:
                    counts += 1
                    self.flag = False
                    
                elif GPIO.input(self.pin) == 1 and not self.flag:
                    self.flag = True
                else:
                    pass

            last = time.time()
            if counts < self.offset_dry and counts > self.offfset_moist:
                counts = (self.offset_dry -(counts-self.offfset_moist))//5
            elif counts > self.offset_dry:
                counts = 100
            elif counts < self.offfset_moist:
                counts = 100
            else:
                print(f'problems with reading {self.name}')

            self.last_values.insert(0, counts)
            self.list = self.last_values[:10]
            self.counts =  counts
    
    def start_loop(self):
        print(f'starting soilmoist sensor {self.name}...')
        Thread(target=self.loop).start()

    def get_values(self):
        return round(np.mean(self.last_values),0)

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


            
    

            


