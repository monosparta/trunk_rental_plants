import json
import time
import machine
import ntptime
from errorlog import ErrorLogger
from mqtt import MQTT
from soil import Soil
from bh1750 import BH1750


class RentalPlants():
    def __init__(self):
        # read json file
        with open('./config.json', 'r') as f:
            self.data = json.loads(f.read())

        self.__error_logger = ErrorLogger()

        try:
            # UTC offset
            self.UTC_OFFSET = 8 * 60 * 60
            ntptime.settime()
        except OSError as error:
            print(f'NTP Error {error}')
            error_times = self.__error_logger.add_error(f'NTP Error {error}')
            self.__error_logger.retry(error_times)

        # connect the mqtt server
        self.publisher = MQTT(
            host=self.data['mqtt']['host'],
            topic=self.data['mqtt']['topic'].encode(),
            error_topic=self.data['mqtt']['error_topic'].encode(),
            username=self.data['mqtt']['username'],
            password=self.data['mqtt']['password']
        )

        # create the soil object
        self.soil = Soil(self.data['soil']['pin'])

        self.bh1750 = BH1750(scl=self.data['light']['scl'], sda=self.data['light']['sda'])

        # check if soil moisture is capacity type
        self.is_capacity_soil_sensor = self.data['soil']['is_capacity_soil_sensor']

    def enable_sensor(self):
        while True:
            self.actual_time = time.localtime(time.time() + self.UTC_OFFSET)

            valid_time = self.data['interval']['normal_duration']
            if self.data['interval']['deep_start'] <= self.actual_time[3] <= self.data['interval']['deep_end']:
                valid_time = self.data['interval']['deep_duration']

            valid_time += self.data['interval']['valid']

            # calculate the soil moisture data
            if self.is_capacity_soil_sensor is True:
                # for capacity type soil moisture sensor
                soil_humi_percent = 100*(1 - self.soil.get_value() / 4095)
            else:
                # for non capacity type soil moisture sensor
                soil_humi_percent = (self.soil.get_value()/4095) * 100
            try:
                plant_data = {
                    'container_ID': self.data['container_ID'],
                    'soil_humi': f'{soil_humi_percent:4.2f}',
                    'light': f'{self.bh1750.value()}',
                    'time': list(self.actual_time),
                    'valid': valid_time
                }
            except OSError as error:
                print(f'Sensor Error {error}')
                error_times = self.__error_logger.add_error(f'Sensor Error {error}')
                self.__error_logger.retry(error_times)

            try:
                # send the data to mqtt
                self.publisher.send_message(json.dumps(plant_data))
                print(plant_data)
            except Exception as error:
                print(f'MQTT Error  {error}')
                error_times = self.__error_logger.add_error(f'MQTT Error  {error}')
                self.__error_logger.retry(error_times)

            # send historical error after first successful send
            self.__dump_error()

            # range of deepsleep mode
            if self.data['interval']['deep_start'] <= self.actual_time[3] <= self.data['interval']['deep_end']:
                machine.deepsleep(self.data['interval']['deep_duration'] * 1000)
                machine.reset()
            else:
                time.sleep(self.data['interval']['normal_duration'])

    def __dump_error(self):
        errors = self.__error_logger.read_error()
        if len(errors) != 0:
            errors.reverse()
            try:
                error_data = {
                    'container_ID': self.data['container_ID'],
                    'errors': errors
                }
                self.publisher.send_error_message(json.dumps(error_data))
            except Exception as error:
                print(f'MQTT Error {error} when sending error')
            else:
                self.__error_logger.clear_error()

rental_planter = RentalPlants()
rental_planter.enable_sensor()
