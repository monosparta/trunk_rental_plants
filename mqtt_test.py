import json
from mqtt import MQTT
import time

with open("./config.json", "r") as f:
    data = json.loads(f.read())



publisher = MQTT(
    host=data["mqtt"]["host"],
    topic=data["mqtt"]["topic"].encode(),
    username=data["mqtt"]["username"],
    password=data["mqtt"]["password"]
)


while 1:
    time.sleep(data["interval"])
    
    publisher.send_message(f"test")