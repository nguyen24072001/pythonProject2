import paho.mqtt.client as mqtt
from paho.mqtt import publish

from blink_test import _calculator_blink, add_status

MQTT_SERVER = "localhost"
MQTT_PORT = 1883
test = "test"
data = 1


def on_connect(client, userdata, flags, rc):
    print('Đã kết nối với mã kết quả: ' + str(rc))
    client.subscribe(test)


def on_message(client, userdata, msg):
    global data
    if msg.topic == test and msg.payload == b'1':
        data = 1
    if msg.topic == test and msg.payload == b'2':
        data = 2
    if msg.topic == test and msg.payload == b'0':
        data = 3


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)

# Start the MQTT client loop
client.loop_start()

while True:
    ketqua = add_status(0, data)
    print(ketqua)
    blink = _calculator_blink(ketqua)
    print("sum", blink)
