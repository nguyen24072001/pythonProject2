import paho.mqtt.client as mqtt
import time
import json
import random
from paho.mqtt import publish

MQTT_SERVER = "localhost"
MQTT_PORT = 1883
message_id = 0
# MQTT topics => publish
MQTT_TOPIC = "get_status"
MQTT_TOPIC4 = "SUM_BLINK"
MQTT_TOPIC_CALL = "call_get_status"


latest_status = ""


def publish_messages():
    publish.single(MQTT_TOPIC, payload=text_sum, hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)
    publish.single(MQTT_TOPIC4, payload=text4, hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)


def on_connect(client, userdata, flags, rc):
    print('Đã kết nối với mã kết quả: ' + str(rc))
    client.subscribe(MQTT_TOPIC)
    client.subscribe(MQTT_TOPIC4)
    client.subscribe(MQTT_TOPIC_CALL)


def on_message(client, userdata, msg):
    global latest_status
    latest_status = {
        "text_sum": json.loads(text_sum),
        "text4": json.loads(text4)
    }
    if msg.topic == MQTT_TOPIC_CALL and msg.payload == b'call1':
        publish.single(MQTT_TOPIC_CALL, payload=json.dumps(latest_status), hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('localhost', 1883, 60)

# Start the MQTT client loop
client.loop_start()

while True:
    text_sum = json.dumps({
        "text1": random.randint(0, 100),
        "text2": random.randint(0, 100),
        "text3": random.randint(0, 100)
    })
    text4 = json.dumps({
        "text4": random.randint(0, 100)
    })

    publish_messages()
