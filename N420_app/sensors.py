import numpy as np
from time import time, sleep
import bme280
import soilmoist as sm

class Sensor():
    my_bme280 = bme280

    def __init__(self):
        pass

    @classmethod
    def get_data(cls):
        flag = True
        while flag:
            try:  
                    temperature,pressure,humidity = cls.my_bme280.readBME280All()
                    _sensordata = {}
                    _sensordata['temp'] = temperature
                    _sensordata['hum'] =  humidity*100
                    _sensordata['soil1'] =  round(abs(np.sin(time())),2)
                    _sensordata['soil2']= round(abs(np.sin(time())),2)
                    _sensordata['soil3']= round(abs(np.sin(time())),2)
                    _sensordata['pres'] = pressure
                    flag = False
            except:
                print('waiting for sensor...')
                sleep(0.1)
                
        return _sensordata


if __name__ == '__main__':
    sensor = Sensor()
    print(sensor.get_data())