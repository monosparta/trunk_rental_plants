import time
from umqttsimple import MQTTClient
import ubinascii
from machine import unique_id, reset


class MQTT:
    def __init__(self, host, topic, username, password, error_topic=None, port=1883, keepalive=60):
        self.host = host
        self.port = port
        self.topic = topic
        self.error_topic = error_topic
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

    def send_message(self, msg):
        self.publisher.publish(self.topic, msg)

    def send_error_message(self, msg):
        if self.error_topic is not None:
            self.publisher.publish(self.error_topic, msg)
