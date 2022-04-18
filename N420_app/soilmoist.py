
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
    sample_cycle = 1
    sensors = []


    def __init__(self, pin, name):
        GPIO.setup(pin, GPIO.IN,GPIO.PUD_UP)
        self.pin = pin
        self.offset_dry = 500
        self.offset_moist = 100
        self.offset_delta = 4
        self.name = name
        self.flag = False
        self.last_values = [0]
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
            self.last_values_raw.insert(0, counts)
            self.last_values_raw = self.last_values_raw[:10]
            last = time.time()

    def get_values_mapped(self):
        mapped_value = np.mean(self.last_values_raw)
        if mapped_value > self.offset_dry or mapped_value < self.offset_moist:
            if mapped_value == 0:
                mapped_value = 100
            else:
                print('measurement out of range: ', mapped_value)
            mapped_value = 100
        elif mapped_value <  self.offset_dry and mapped_value >self.offset_moist:
            mapped_value = 100-((mapped_value - self.offset_moist)/self.offset_delta)
        else:
            print('error while measuring: ', mapped_value)
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
        time.sleep(2.5)
        print(SoilMoist.get_data_mapped())
        print(SoilMoist.get_data_raw())


            
    

            


