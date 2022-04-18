import board
import adafruit_bmp280


class BMP280():

    def __init__(self, address):
        i2c = board.I2C()
        BMP280.bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c,address=address)

    @classmethod
    def get_temp(cls):
        return cls.bmp280.temperature

    @classmethod
    def get_pres(cls):
        return cls.bmp280.pressure
