import threading
import json
import os

from typing import List
from flask import Flask
from flask_mqtt import Mqtt

from features.publishers.temperature_publisher import TemperaturePublisher
from features.publishers.humidity_publisher import HumidityPublisher
from shared.mqtt_connection import MqttConnection
from features.publishers.publisher_abs import Publisher
from features.subscribers.subscriber import Subscriber

broker = os.getenv("MQTT_BROKER_URL", "127.0.0.1")
port = int(os.getenv("MQTT_BROKER_PORT", "1883"))

app = Flask(__name__)
app.config["MQTT_BROKER_URL"] = broker
app.config["MQTT_BROKER_PORT"] = port
app.config["MQTT_USERNAME"] = ""
app.config["MQTT_PASSWORD"] = ""
app.config["MQTT_KEEPALIVE"] = 5
app.config["MQTT_TLS_ENABLED"] = False

mqtt = Mqtt(app)

publishers: List[Publisher] = []
subscriber = Subscriber(mqtt)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# ----------------------------------------------------------------------------
# Publishers
# ----------------------------------------------------------------------------
def create_publishers(config_file = "publishers.json"):
    with open(f"/simulator/src/data/{config_file}", "r") as file:
        sensors = json.load(file)

    for sensor in sensors:
        if sensor["type"] == "temperatura":
            publisher_temp = TemperaturePublisher(
                mqtt_client=mqtt,
                topic=sensor["topic"],
                id=sensor["id"],
                min_value=sensor.get("min_value", 0),
                max_value=sensor.get("max_value", 100),
                interval=sensor.get("interval", 2),
            )
            publishers.append(publisher_temp)
            
        if sensor["type"] == "umidade":
            publisher_temp = HumidityPublisher(
                mqtt_client=mqtt,
                topic=sensor["topic"],
                id=sensor["id"],
                min_value=sensor.get("min_value", 0),
                max_value=sensor.get("max_value", 100),
                interval=sensor.get("interval", 2),
            )
            publishers.append(publisher_temp)

    for publisher in publishers:
        print(f"🚀 Publisher {publisher_temp.__class__.__name__} iniciado no tópico {publisher_temp.topic}")
        threading.Thread(target=publisher.publish_data, daemon=True).start()


# ----------------------------------------------------------------------------
# Subscribers
# ----------------------------------------------------------------------------
def setup_subscribers():
    for publisher in publishers:
        subscriber.add_connection(new_connection=MqttConnection(publisher.topic))

    subscriber.subscribe_to_connections()


# ----------------------------------------------------------------------------
# Setup
# ----------------------------------------------------------------------------
@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Conectado com sucesso ao broker")
        create_publishers()
        setup_subscribers()
    else:
        print("Falha na comunicação. Cod: ", rc)


if __name__ == "__main__":
    mqtt.init_app(app)
    print("Serviço iniciado")
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
