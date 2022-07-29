from machine import ADC, Pin
import time


class LightSensor:
    def __init__(self, pin):
        self.pin = pin
        self.pot = ADC(Pin(self.pin))
        self.pot.atten(ADC.ATTN_11DB)  # Full range: 3.3v

    def get_value(self):
        return self.pot.read()


if __name__ == "__main__":
    light_sensor = LightSensor(35)
    print(light_sensor.get_value())
