from typing import List
from flask_mqtt import Mqtt

from shared.mqtt_connection import MqttConnection


class Subscriber:
    def __init__(
        self,
        mqtt: Mqtt,
    ):
        self.mqtt = mqtt
        self._connections: List[MqttConnection] = []
        self._callbacks = {}

    def add_connection(self, new_connection: MqttConnection, callback=None):
        self._connections.append(new_connection)
        if callback:
            self._callbacks[new_connection.topic] = callback

    def get_connections(self) -> List[MqttConnection]:
        return self._connections

    def subscribe_to_connections(self):
        mqtt = self.mqtt

        for connection in self._connections:
            self.mqtt.subscribe(connection.topic, connection.qos)

        @mqtt.on_message()
        def handle_mqtt_message(client, userdata, message):
            topic = message.topic
            payload = message.payload.decode()

            if topic in self._callbacks:
                self._callbacks[topic](payload)
            else:
                print(f"Valor recebido: [{topic}] {payload}")
