class MqttConnection:
    def __init__(
        self,
        topic: str,
        qos: int = 1,
    ):
        self.topic = topic
        self.qos = qos
