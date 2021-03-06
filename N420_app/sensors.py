import numpy as np
from time import time, sleep
from soilmoist import SoilMoist
from bme680 import BME680


class Sensor():
    

    def __init__(self):
        SoilMoist(11, 'soil1')
        SoilMoist(9, 'soil2')
        BME680(0x77)
        

    @classmethod
    def get_data(cls):
        flag = True
        while flag:
            # try:  
                    _sensordata = {}
                    _sensordata['temp'] = round(BME680.get_temp(),1)
                    _sensordata['hum'] =  round(BME680.get_hum(),1)
                    _sensordata['air_quality'] =  round(BME680.get_gas(),1)
                    _sensordata['pres'] = round(BME680.get_pres(), 1)
                    _sensordata['soil1'] =  SoilMoist.get_data_mapped()['soil1']
                    _sensordata['soil2']= SoilMoist.get_data_mapped()['soil2']
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