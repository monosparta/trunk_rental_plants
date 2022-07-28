from machine import Pin, ADC


class Soil:
    def __init__(self, pin):
        self.pin = pin
        self.pot = ADC(Pin(self.pin))
        self.pot.atten(ADC.ATTN_11DB)  # Full range: 3.3v

    def get_value(self):
        return self.pot.read()