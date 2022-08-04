import json
import time
import machine
from mqtt import MQTT
from soil import Soil
from bh1750 import BH1750

# read json file
with open('./config.json', 'r') as f:
    data = json.loads(f.read())

# connect the mqtt server
publisher = MQTT(
    host=data['mqtt']['host'],
    topic=data['mqtt']['topic'].encode(),
    username=data['mqtt']['username'],
    password=data['mqtt']['password']
)

# publisher = MQTT(
#     host=data["van-mqtt"]["host"],
#     topic=data["van-mqtt"]["topic"].encode(),
#     username=data["van-mqtt"]["username"],
#     password=data["van-mqtt"]["password"]
# )

# create the soil object
soil = Soil(data['soil']['pin'])

bh1750 = BH1750(scl=data['light']['scl'], sda=data['light']['sda'])

while True:
    time.sleep(data['interval'])

    # calculate the soil mositure data
    soil_humi_percent = 100*(1 - soil.get_value() / 4095)

    plant_data = {
        'container_ID': data['container_ID'],
        'soil_humi': f'{soil_humi_percent:4.2f}',
        'light': f'{bh1750.value()}'
    }

    # send the data to mqtt
    publisher.send_message(json.dumps(plant_data))
    # publisher.send_message(f"test")

    # machine.deepsleep(5000) # deepsleep mode for 5s
