import cv2
from btn_test import sw01_get_status, blink_led1, ClearCounter
import paho.mqtt.client as mqtt
from paho.mqtt import publish
import json

MQTT_SERVER = "broker.hivemq.com"
MQTT_PORT = 1883
message_id = 0

MQTT_TOPIC_CALL = "call_get_status"
MQTT_TOPIC_CONTROL = "control"

#topic for for camera blink
topic_camera_blink_receive = "duanlc/test/cam-blink-slave"
topic_camera_blink_send = "duanlc/test/cam-blink-main"

topic_camera_status_receive = "duanlc/test/cam-status-slave"
topic_camera_status_send = "duanlc/test/cam-status-main"


latest_status = ""
ket_qua = ""
blink = ""


def on_connect(client, userdata, flags, rc):
    print('Đã kết nối với mã kết quả: ' + str(rc))

    client.subscribe(topic_camera_blink_receive)
    client.subscribe(topic_camera_status_receive)


def on_message(client, userdata, msg):
    global latest_status, ket_qua, blink
    stringSend = str(blink)
    # latest_status = {
    #     "STATUS": json.loads(ket_qua),
    #     "BLINK": json.loads(blink)
    # }

    #publish.single(topic_camera_status_send, payload="Receive", hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)

    if msg.topic == topic_camera_blink_receive and msg.payload == b'GetCount':
        print("OK 1")
        publish.single(topic_camera_blink_send, payload=stringSend, hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)
    elif msg.topic == topic_camera_blink_receive and msg.payload == b'Clear':
        ClearCounter()
        print("OK 2")
    elif msg.topic == topic_camera_status_receive and msg.payload == b'GetStatus':
        publish.single(topic_camera_status_send, payload=str(ket_qua), hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)
        print("OK 3")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)

# Start the MQTT client loop
client.loop_start()


def main():
    # video = cv2.VideoCapture("CASE_BLINK_LED1.mp4")
    # video = cv2.VideoCapture("CASE_BLINK_LED1v2.mp4")
    # video = cv2.VideoCapture("CASE_BLINK_LED1v3.mp4")
    # video = cv2.VideoCapture("CASE_ADD_LED.mp4")
    # video = cv2.VideoCapture("CASE_REMOVE_LED.mp4")
    video = cv2.VideoCapture(2)
    # video = cv2.VideoCapture("blink_off.jpg")
    # video = cv2.VideoCapture("LED_ON.jpg")
    # video = cv2.VideoCapture("sw01_off_Z.jpg")
    if not video.isOpened():
        print("Failed to open the video file.")
        return
    global ket_qua, blink
    while True:
        # Đọc frame từ video
        ret, frame = video.read()

        # Kiểm tra nếu không thể đọc thêm frame
        if not ret:
            break
        x = 300  # Chiều dài hình vuông
        y = 300  # Chiều rộng hình vuông
        # Tính toán vị trí của hình vuông
        top_left = (250, 0)
        bottom_right = (top_left[0] + x, top_left[1] + y)
        # cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
        cropped_frame = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        # Xử lý ảnh và xác định vùng trắng
        # anh = frame
        anh = cropped_frame
        ket_qua = sw01_get_status(anh)
        # print(ket_qua)
        blink = blink_led1(anh)
        # print(blink)
        # text_sum v2
        cv2.imshow("Anh Goc", anh)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

    # total_time = time.time() - start_time
    # print("Tổng số lần ngưỡng trên 200: ", threshold_count)
    # print("Tổng thời gian tính ngưỡng (ms): ", threshold_time_total)
    # print("Tổng thời gian (s): ", total_time)
    # print("Tổng số lần mà giá trị ngưỡng hiện tại trừ giá trị ngưỡng trước đó > 50: ", total_threshold_diff)


if __name__ == "__main__":
    main()
