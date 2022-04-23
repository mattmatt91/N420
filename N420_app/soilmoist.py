
import time
import RPi.GPIO as GPIO
import numpy as np
from threading import Thread


class SoilMoist():

    GPIO.setmode(GPIO.BCM)
    sample_cycle = 1
    sensors = []


    def __init__(self, pin, name):
        GPIO.setup(pin, GPIO.IN,GPIO.PUD_UP)
        self.pin = pin
        self.max_counts = 1000
        self.name = name
        self.flag = False
        self.last_values_raw = [0]
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
                if counts > self.max_counts:
                    self.max_counts = counts
                    print(f'increasing max counts for {self.name}')
            self.last_values_raw.insert(0, counts)
            self.last_values_raw = self.last_values_raw[0:10]
            last = time.time()

    def get_values_mapped(self):
        mapped_value = (1-(np.mean(self.last_values_raw)/self.max_counts))*100
        return round(mapped_value,0)
            
    def start_loop(self):
        print(f'starting soilmoist sensor {self.name}...')
        Thread(target=self.loop).start()

    def get_values_raw(self):
        return round(np.mean(self.last_values_raw),0)

    
    @classmethod
    def get_data_mapped(cls):
        data = {}
        for sensor in cls.sensors:
            data[sensor.name ] = sensor.get_values_mapped()
        return data

    @classmethod
    def get_data_raw(cls):
        data = {}
        for sensor in cls.sensors:
            data[sensor.name] = sensor.get_values_raw()
        return data
    
        

    
if __name__ == '__main__':
    
    SoilMoist(11, 'soil1')
    SoilMoist(9, 'soil2')
    while True:
        time.sleep(1)
        # print('#'*(int(SoilMoist.get_data_mapped()['soil1']/4)), SoilMoist.get_data_mapped()['soil1'])
        print('mapped: ',SoilMoist.get_data_mapped())
        print('raw; ',SoilMoist.get_data_raw())

        print()


            
    

            


