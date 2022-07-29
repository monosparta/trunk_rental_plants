import json
import time
from mqtt import MQTT
from soil import Soil

# read json file
with open("./config.json", "r") as f:
    data = json.loads(f.read())

# connect the mqtt server
publisher = MQTT(
    host=data["mqtt"]["host"],
    topic=data["mqtt"]["topic"].encode(),
    username=data["mqtt"]["username"],
    password=data["mqtt"]["password"]
)

# publisher = MQTT(
#     host=data["van-mqtt"]["host"],
#     topic=data["van-mqtt"]["topic"].encode(),
#     username=data["van-mqtt"]["username"],
#     password=data["van-mqtt"]["password"]
# )

# create the soil object
soil = Soil(data["soil"]["pin"])

while 1:
    time.sleep(data["interval"])

    # calculate the soil mositure data
    soil_humi_percent = 100*(1 - soil.get_value() / 4095)

    plant_data = {
        "container_ID": data["container_ID"],
        "soil_humi": f"{soil_humi_percent:4.2f}"
    }

    # send the data to mqtt
    publisher.send_message(json.dumps(plant_data))
    # publisher.send_message(f"test")
