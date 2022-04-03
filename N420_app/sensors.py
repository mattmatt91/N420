import numpy as np
from time import time, sleep
import board
# from adafruit_bme280 import basic as adafruit_bme280

class Sensor():
    def __init__(self):
        i2c = board.I2C()   # uses board.SCL and board.SDA
        # Sensor.bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c, 0x76)

    @classmethod
    def get_data(cls):
        flag = True
        while flag:
            try:
                    _sensordata = {}
                    _sensordata['temp'] = 20# round(cls.bme280.temperature,2)
                    _sensordata['hum'] =  50 # round(cls.bme280.relative_humidity,2)
                    _sensordata['soil1'] =  round(abs(np.sin(time())),2)
                    _sensordata['soil2']= round(abs(np.sin(time())),2)
                    _sensordata['soil3']= round(abs(np.sin(time())),2)
                    _sensordata['pres'] = 1009 #round(cls.bme280.pressure,2)
                    flag = False
            except:
                print('waiting for sensor...')
                sleep(0.1)
                
        return _sensordata


if __name__ == '__main__':
    sensor = Sensor()
    print(sensor.get_data())