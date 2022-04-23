import board
from adafruit_bme680 import Adafruit_BME680_I2C


class BME680():

    def __init__(self, address):
        i2c = board.I2C()
        BME680.bme680 = Adafruit_BME680_I2C(i2c, debug=False) #,address=address)

    @classmethod
    def get_temp(cls):
        try:
            return cls.bme680.temperature
        except:
            return 0
    @classmethod
    def get_pres(cls):
        try:
            return cls.bme680.pressure
        except:
            return 0

    @classmethod
    def get_hum(cls):
        try:
            return cls.bme680.humidity
        except:
            return 0

    @classmethod
    def get_gas(cls):
        try:
            return cls.bme680.gas
        except:
            return 0


if __name__ == '__main__':
    BME680(0x77)
    print(BME680.get_pres())
    print(BME680.get_temp())
    print(BME680.get_hum())
    print(BME680.get_gas())