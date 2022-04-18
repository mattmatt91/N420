import numpy as np
from time import time, sleep
from soilmoist import SoilMoist
from bmp280 import BMP280


class Sensor():
    

    def __init__(self):
        SoilMoist(11, 'soil1')
        SoilMoist(9, 'soil2')
        BMP280(0x76)
        

    @classmethod
    def get_data(cls):
        flag = True
        while flag:
            # try:  
                    _sensordata = {}
                    _sensordata['temp'] = round(BMP280.get_temp(),1)
                    _sensordata['hum'] =  50
                    _sensordata['pres'] = round(BMP280.get_pres(), 1)
                    _sensordata['soil1'] =  SoilMoist.get_data()['soil1']
                    _sensordata['soil2']= SoilMoist.get_data()['soil2']
                    flag = False
           
            # except:
                # print('waiting for sensor...')
                # sleep(0.1)
                
        return _sensordata


if __name__ == '__main__':
    sensor = Sensor()
    while True:
        sleep(1)
        print(sensor.get_data())