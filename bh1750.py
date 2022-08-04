from machine import Pin,SoftI2C
import bh1750_driver


class BH1750:
    def __init__(self,scl, sda):
        self.scl = scl,
        self.sda = sda
        self.bh1750 = SoftI2C(scl=Pin(scl), sda=Pin(sda))

    def value(self):
        return bh1750_driver.sample(self.bh1750)
