from abc import ABC, abstractmethod
from typing import Any
from flask_mqtt import Mqtt

import time

from shared.payload import Payload


class Publisher(ABC):
    def __init__(
        self,
        mqtt_client: Mqtt,
        topic: str,
        id: str,
        interval: float = 2.0,
        min_value: int = 0,
        max_value: int = 100,
    ) -> None:
        self.mqtt_client = mqtt_client
        self.topic = topic
        self.id = id
        self.interval = interval
        self.min_value = min_value
        self.max_value = max_value
        self.running: bool = True

    @abstractmethod
    def generate_data(self) -> Payload:
        pass

    def publish_data(self) -> None:
        while self.running:
            data: Payload = self.generate_data()
            message: str = data.get_payload()
            print(f"Publicando mensagem: {message} no tópico {self.topic}")
            self.mqtt_client.publish(self.topic, message)
            time.sleep(self.interval)

    def stop(self) -> None:
        self.running = False
