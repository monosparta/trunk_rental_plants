import json
import time
from mqtt import MQTT
from soil import Soil

with open("./config.json", "r") as f:
    data = json.loads(f.read())

publisher = MQTT(
    host=data["mqtt"]["host"],
    topic=data["mqtt"]["topic"].encode(),
    username=data["mqtt"]["username"],
    password=data["mqtt"]["password"]
)

soil = Soil(data["soil"]["pin"])

while 1:
    time.sleep(data["interval"])
    soil_humi_percent = 100*(1 - soil.get_value() / 4095)
    publisher.send_message(f"{soil_humi_percent:4.2f}")
