import paho.mqtt.client as mqtt
import time
from paho.mqtt import publish

MQTT_SERVER = "localhost"
MQTT_PORT = 1883
message_id = 0
# MQTT topics => publish
MQTT_TOPIC_CALL = "call_get_status"
MQTT_TOPIC2 = "enter"
text_sum4 = ""


def on_connect(client, userdata, flags, rc):
    print('Đã kết nối với mã kết quả: ' + str(rc))
    client.subscribe(MQTT_TOPIC_CALL)
    client.subscribe(MQTT_TOPIC2)

def on_message(client, userdata, msg):
    global text_sum4
    if msg.topic == MQTT_TOPIC_CALL and msg.payload == b'e':
        publish.single(MQTT_TOPIC_CALL, payload="enroll", hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)
    elif msg.topic == MQTT_TOPIC_CALL and msg.payload == b'd':
        publish.single(MQTT_TOPIC_CALL, payload="delete", hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)
    elif msg.topic == MQTT_TOPIC_CALL and msg.payload == b'f':
        publish.single(MQTT_TOPIC_CALL, payload="find", hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)
    elif msg.topic == MQTT_TOPIC_CALL and msg.payload == b'l':
        text_sum4 = "loop"
    elif msg.topic == MQTT_TOPIC_CALL and msg.payload == b's':
        text_sum4 = "stop"
    elif msg.topic == MQTT_TOPIC_CALL:
        if msg.payload.isdigit():
            number = int(msg.payload)
            if 1 <= number <= 127:
                data = number
                print("Data: ", data)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('localhost', 1883, 60)

# Start the MQTT client loop
client.loop_start()

while True:
    publish.single(MQTT_TOPIC2, payload="4", hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)
    time.sleep(3)
    if text_sum4 == "loop":
        print("loop")
        time.sleep(5)
        if text_sum4 == "stop":
            print("stop")
            pass

