import time
from umqttsimple import MQTTClient
import ubinascii
from machine import unique_id, reset


class MQTT:
    def __init__(self, host, topic, username, password, port=1883, keepalive=60):
        self.host = host
        self.port = port
        self.topic = topic
        self.username = username
        self.password = password
        self.keepalive = keepalive

        # connect to mqtt client
        self.publisher = MQTTClient(
            client_id=ubinascii.hexlify(unique_id()),
            server=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            keepalive=self.keepalive
        )


        self.publisher.connect()


    def restart_and_reconnect(self):
        print('Failed to connect to MQTT broker. Reconnecting...')
        time.sleep(10)
        reset()

    def send_message(self, msg):
        self.publisher.publish(self.topic, msg)
