import cv2
from btn_test import sw01_get_status, blink_led1
import paho.mqtt.client as mqtt
from paho.mqtt import publish
import json

MQTT_SERVER = "localhost"
MQTT_PORT = 1883
message_id = 0

MQTT_TOPIC_CALL = "call_get_status"


latest_status = ""
ket_qua = ""
blink = ""


def on_connect(client, userdata, flags, rc):
    print('Đã kết nối với mã kết quả: ' + str(rc))

    client.subscribe(MQTT_TOPIC_CALL)


def on_message(client, userdata, msg):
    global latest_status
    latest_status = {
        "STATUS": json.loads(ket_qua),
        "BLINK": json.loads(blink)
    }
    if msg.topic == MQTT_TOPIC_CALL and msg.payload == b'call1':
        publish.single(MQTT_TOPIC_CALL, payload=json.dumps(latest_status), hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('localhost', 1883, 60)

# Start the MQTT client loop
client.loop_start()


def main():
    # video = cv2.VideoCapture("CASE_BLINK_LED1.mp4")
    # video = cv2.VideoCapture("CASE_BLINK_LED1v2.mp4")
    # video = cv2.VideoCapture("CASE_BLINK_LED1v3.mp4")
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

        # Xử lý ảnh và xác định vùng trắng
        anh = frame
        ket_qua = sw01_get_status(anh)
        # print(ket_qua)
        blink = blink_led1(anh)
        # print(blink)
        # text_sum v2
        cv2.imshow("Anh Goc", anh)

        if cv2.waitKey(1) & 0xFF == ord('q'):
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
