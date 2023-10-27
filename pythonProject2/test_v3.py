import json
import cv2
import time
import numpy as np
import sys
import logging
import math
import paho.mqtt.client as mqtt
from paho.mqtt import publish

# CAMERA = "CASE_4blink.mp4"
CAMERA = 2
R_MIN = 35
R_MAX = 40
DISTANCE_SWITCH = 100
DISTANCE_THRESH = 18
NUM_SWITCH = 4
delta_blink = 11

MQTT_SERVER = "localhost"
MQTT_PORT = 1883
message_id = 0

topic_camera_blink_receive = "clear"
topic1 = "led1"
topic2 = "led2"
topic3 = "led3"
topic4 = "led4"

topic5 = "get1"
topic6 = "get2"
topic7 = "get3"
topic8 = "get4"

topic9 = "receive1"
topic10 = "receive2"
topic11 = "receive3"
topic12 = "receive4"


def on_connect(client, userdata, flags, rc):
    print('Đã kết nối với mã kết quả: ' + str(rc))

    client.subscribe(topic_camera_blink_receive)
    client.subscribe(topic1)
    client.subscribe(topic2)
    client.subscribe(topic3)
    client.subscribe(topic4)
    client.subscribe(topic5)
    client.subscribe(topic6)
    client.subscribe(topic7)
    client.subscribe(topic8)


def on_message(client, userdata, msg):
    if msg.topic == topic_camera_blink_receive and msg.payload == b'Clear':
        clear()
    if msg.topic == topic5 and msg.payload == b'get':
        publish.single(topic9, payload=led1, hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)
    if msg.topic == topic6 and msg.payload == b'get':
        publish.single(topic10, payload=led2, hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)
    if msg.topic == topic7 and msg.payload == b'get':
        publish.single(topic11, payload=led3, hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)
    if msg.topic == topic8 and msg.payload == b'get':
        publish.single(topic12, payload=led4, hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)

# Start the MQTT client loop
client.loop_start()


def add_thresh(thresh_list, thresh=0):
    for i in thresh_list:
        if abs(int(thresh) - int(i)) >= DISTANCE_THRESH:
            continue
        else:
            return thresh_list
    thresh_list.append(thresh)
    return thresh_list


def add_switch(switch_list, switch=(0, 0, 0)):
    for i in switch_list:
        if abs(int(switch[0]) - int(i[0])) >= DISTANCE_SWITCH or abs(int(switch[1]) - int(i[1])) >= DISTANCE_SWITCH:
            continue
        else:
            return switch_list
    switch_list.append(switch)
    return switch_list


def cal_average_and_draw_circle1(img, _a, _b, _r):
    points = []
    _gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for _r in range(_r - 5, _r - 1, 1):
        # 1, 2
        for x in range(_a - _r, _a + _r, 1):
            y = int(-(_r ** 2 - (x - _a) ** 2) ** 0.5 + _b)
            points.append(_gray[y, x])
            cv2.rectangle(img, (x, y), (x, y), (0, 0, 255), 1)

    return img, int(sum(points) / len(points))


def cal_average_and_draw_circle2(img, _a, _b, _r):
    points = []
    _gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for _r in range(_r - 5, _r - 1, 1):

        # 3, 4
        for x in range(_a - _r, _a + _r, 1):
            y = int((_r ** 2 - (x - _a) ** 2) ** 0.5 + _b)
            points.append(_gray[y, x])
            cv2.rectangle(img, (x, y), (x, y), (255, 0, 0), 1)
    return img, int(sum(points) / len(points))


def cal_average_circle(img, _a, _b, _r):
    points = []
    _gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for _r in range(_r - 5, _r - 1, 1):
        for x in range(_a - _r, _a + _r, 1):
            y = int(-(_r ** 2 - (x - _a) ** 2) ** 0.5 + _b)
            points.append(_gray[y, x])

        for x in range(_a - _r, _a + _r, 1):
            y = int((_r ** 2 - (x - _a) ** 2) ** 0.5 + _b)
            points.append(_gray[y, x])

    return int(sum(points) / len(points))


def bubbleSort(arr):
    n = len(arr)
    for i in range(n - 1):

        for j in range(0, n - i - 1):

            if arr[j] > arr[j + 1]:
                # swapped = True
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def state(thresh_list, delta_list, current_thresh=0):
    logging.info("Thresh:%d - %d - %d - %d", current_thresh, thresh_list[0], thresh_list[1], thresh_list[2])

    if thresh_list[0] + delta_list[0] > current_thresh > thresh_list[0] - delta_list[0]:
        return 0
    elif thresh_list[1] + delta_list[1] > current_thresh > thresh_list[1] - delta_list[0]:
        return 1
    elif thresh_list[2] + delta_list[2] > current_thresh > thresh_list[2] - delta_list[2]:
        return 2
    else:
        return 3


def put_state_to_img(img, pos=(0, 0, 0), _state=3):
    if _state == 3:
        return img
    if _state == 0:
        cv2.putText(img, "Z", (pos[0], pos[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, color=(255, 0, 0), thickness=2)
    elif _state == 1:
        cv2.putText(img, "OFF", (pos[0], pos[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, color=(255, 0, 0), thickness=2)
    elif _state == 2:
        cv2.putText(img, "ON", (pos[0], pos[1]), cv2.FONT_HERSHEY_SIMPLEX, 1, color=(255, 0, 0), thickness=2)
    return img


def detect_switch(switch_list, camera, num_switch):
    while True:
        if len(switch_list) >= num_switch:
            logging.info("Detect switch success!")
            break
        _ret, _image = camera.read()
        if not _ret:
            logging.error("Camera error")
            break

        _gray = cv2.cvtColor(_image, cv2.COLOR_BGR2GRAY)
        detected_circles = cv2.HoughCircles(_gray, cv2.HOUGH_GRADIENT, 1, DISTANCE_SWITCH, param1=50, param2=30,
                                            minRadius=R_MIN, maxRadius=R_MAX)
        if detected_circles is not None:
            detected_circles = np.uint16(np.around(detected_circles))
            for pt in detected_circles[0, :]:
                a, b, r = pt[0], pt[1], pt[2]

                switch_list = add_switch(switch_list, (a, b, r))
    return switch_list


def detect_thresh(thresh_list, delta_list, camera):
    while True:
        if len(thresh_list) >= 3:
            logging.info("Detect thresh success!")

            break
        _ret, _image = camera.read()
        if not _ret:
            logging.error("Camera error")
            break
        sum_point = 0
        for i in range(0, NUM_SWITCH, 1):
            sum_point += cal_average_circle(_image, switch_pos[i][0], switch_pos[i][1], switch_pos[i][2])
        thresh_list = add_thresh(thresh_list, int(sum_point / NUM_SWITCH))

    thresh_list = bubbleSort(thresh_list)

    delta_list.append(int((thresh_list[1] - thresh_list[0]) / 2))
    delta_list.append(int((thresh_list[2] - thresh_list[1]) * 2 / 3))
    delta_list.append(int((thresh_list[2] - thresh_list[1]) * 1 / 3))

    return thresh_list, delta_list


previous_threshold_value1 = None
previous_threshold_value2 = None
previous_threshold_value3 = None
previous_threshold_value4 = None
dem_am1 = 0
dem_am2 = 0
dem_am3 = 0
dem_am4 = 0
fps = 0
frame_count = 0

status1 = ""
status2 = ""
status3 = ""
status4 = ""

sum_blink1 = ""
sum_blink2 = ""
sum_blink3 = ""
sum_blink4 = ""


def get_status1():
    global status1, sum_blink1
    return status1, sum_blink1


def get_status2():
    global status2, sum_blink2
    return status2, sum_blink2


def get_status3():
    global status3, sum_blink3
    return status3, sum_blink3


def get_status4():
    global status4, sum_blink4
    return status4, sum_blink4


def clear():
    global dem_am1, dem_am2, dem_am3, dem_am4
    dem_am1 = 0
    dem_am2 = 0
    dem_am3 = 0
    dem_am4 = 0


def get_led_state1(_point, _thresh_level, _delta_thresh):
    global status1
    status1 = state(thresh_level, delta_thresh, point)
    return str(status1)


def get_led_state2(_point, _thresh_level, _delta_thresh):
    global status2
    status2 = state(thresh_level, delta_thresh, point)
    return str(status2)


def get_led_state3(_point, _thresh_level, _delta_thresh):
    global status3
    status3 = state(thresh_level, delta_thresh, point)
    return str(status3)


def get_led_state4(_point, _thresh_level, _delta_thresh):
    global status4
    status4 = state(thresh_level, delta_thresh, point)
    return str(status4)


def get_led_blink1(_dem_am1):
    global sum_blink1
    sum_blink1 = math.ceil((dem_am1 - 1) / 2)
    return str(sum_blink1)


def get_led_blink2(_dem_am2):
    global sum_blink2
    sum_blink2 = math.ceil((dem_am2 - 1) / 2)
    return str(sum_blink2)


def get_led_blink3(_dem_am3):
    global sum_blink3
    sum_blink3 = math.ceil((dem_am3 - 1) / 2)
    return str(sum_blink3)


def get_led_blink4(_dem_am4):
    global sum_blink4
    sum_blink4 = math.ceil((dem_am4 - 1) / 2)
    return str(sum_blink4)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    video = cv2.VideoCapture(CAMERA)
    if not video.isOpened():
        logging.error("Failed to open the video file.")
        sys.exit()

    for temp in range(0, 100, 1):
        ret, frame = video.read()

    switch_pos = list()
    thresh_level = list()
    delta_thresh = list()

    switch_pos = detect_switch(switch_pos, video, NUM_SWITCH)

    thresh_level, delta_thresh = detect_thresh(thresh_level, delta_thresh, video)
    # thresh_level =
    print("OK")
    start_time = time.time()
    while True:
        ret, frame = video.read()
        if not ret:
            logging.error("Camera error")
            break

        status1, sum_blink1 = get_status1()
        status2, sum_blink2 = get_status2()
        status3, sum_blink3 = get_status3()
        status4, sum_blink4 = get_status4()
        data1 = {
            "LED": 1,
            "status": status1,
            "blinks": sum_blink1
        }
        data2 = {
            "LED": 2,
            "status": status2,
            "blinks": sum_blink2
        }
        data3 = {
            "LED": 3,
            "status": status3,
            "blinks": sum_blink3
        }
        data4 = {
            "LED": 4,
            "status": status4,
            "blinks": sum_blink4
        }
        led1 = json.dumps(data1)
        led2 = json.dumps(data2)
        led3 = json.dumps(data3)
        led4 = json.dumps(data4)

        # print("LED1", status1, sum_blink1)
        publish.single(topic1, payload=led1, hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)
        # print("LED2", status2, sum_blink2)
        publish.single(topic2, payload=led2, hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)
        # print("LED3", status3, sum_blink3)
        publish.single(topic3, payload=led3, hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)
        # print("LED4", status4, sum_blink4)
        publish.single(topic4, payload=led4, hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)

        a_sum = 0
        b_sum = 0

        for pos in switch_pos:
            a_sum += pos[0]
            b_sum += pos[1]

        a_avg = a_sum / NUM_SWITCH
        b_avg = b_sum / NUM_SWITCH
        # cv2.circle(frame, (int(a_avg), int(b_avg)), 2, (0, 165, 255), -1)
        center = (int(a_avg), int(b_avg))
        item1 = []
        for i in range(4):
            item = tuple(switch_pos[i][:2])
            item1.append(item)

        for i in range(0, NUM_SWITCH, 1):
            # print(item1[i])
            if item1[i][0] > center[0] and item1[i][1] > center[1]:

                frame, point = cal_average_and_draw_circle1(frame, item1[i][0], item1[i][1], switch_pos[i][2])
                frame = put_state_to_img(frame, switch_pos[i], state(thresh_level, delta_thresh, point))
                # status = state(thresh_level, delta_thresh, point)
                status = get_led_state1(thresh_level, delta_thresh, point)

                final = ""
                if status == 0:
                    final = "Z"
                elif status == 1:
                    final = "OFF"
                elif status == 2:
                    final = "ON"
                # print("LED 1", point, item1[i][0], item1[i][1])
                if previous_threshold_value1 is not None:
                    threshold_diff1 = point - previous_threshold_value1
                    if abs(threshold_diff1) <= 5:
                        pass
                    elif delta_blink < abs(threshold_diff1):

                        dem_am1 = dem_am1 + 1
                        # print("-", dem_am1)
                previous_threshold_value1 = point

                # sum_blink = math.ceil((dem_am1 - 1) / 2)
                sum_blink = get_led_blink1(dem_am1)
                # print("sum", sum_blink)
                cv2.putText(frame, f"LED 1:{point}:{final}:{sum_blink}", (item1[i][0] - 50, item1[i][1] + 55),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 0, 0), 2)
            elif item1[i][0] < center[0] and item1[i][1] > center[1]:

                frame, point = cal_average_and_draw_circle1(frame, item1[i][0], item1[i][1], switch_pos[i][2])
                frame = put_state_to_img(frame, switch_pos[i], state(thresh_level, delta_thresh, point))
                status = get_led_state2(thresh_level, delta_thresh, point)
                final = ""
                if status == 0:
                    final = "Z"
                elif status == 1:
                    final = "OFF"
                elif status == 2:
                    final = "ON"
                # print("LED 2", point, item1[i][0], item1[i][1])
                if previous_threshold_value2 is not None:
                    threshold_diff2 = point - previous_threshold_value2
                    if abs(threshold_diff2) <= 5:
                        pass
                    elif delta_blink < abs(threshold_diff2):

                        dem_am2 = dem_am2 + 1
                        # print("-", dem_am2)
                previous_threshold_value2 = point

                sum_blink = get_led_blink2(dem_am2)
                # print("sum", sum_blink)
                cv2.putText(frame, f"LED 2:{point}:{final}:{sum_blink}", (item1[i][0] - 50, item1[i][1] + 55),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 0, 0), 2)
            elif item1[i][0] > center[0] and item1[i][1] < center[1]:

                frame, point = cal_average_and_draw_circle2(frame, item1[i][0], item1[i][1], switch_pos[i][2])
                frame = put_state_to_img(frame, switch_pos[i], state(thresh_level, delta_thresh, point))
                status = get_led_state3(thresh_level, delta_thresh, point)
                final = ""
                if status == 0:
                    final = "Z"
                elif status == 1:
                    final = "OFF"
                elif status == 2:
                    final = "ON"
                # print("LED 3", point, item1[i][0], item1[i][1])
                if previous_threshold_value3 is not None:
                    threshold_diff3 = point - previous_threshold_value3
                    if abs(threshold_diff3) <= 5:
                        pass
                    elif delta_blink < abs(threshold_diff3):

                        dem_am3 = dem_am3 + 1
                        # print("-", dem_am3)

                previous_threshold_value3 = point

                sum_blink = get_led_blink3(dem_am3)
                # print("sum", sum_blink
                cv2.putText(frame, f"LED 3:{point}:{final}:{sum_blink}", (item1[i][0] - 50, item1[i][1] + 55),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 0, 0), 2)
            elif item1[i][0] < center[0] and item1[i][1] < center[1]:

                frame, point = cal_average_and_draw_circle2(frame, item1[i][0], item1[i][1], switch_pos[i][2])
                frame = put_state_to_img(frame, switch_pos[i], state(thresh_level, delta_thresh, point))
                status = get_led_state4(thresh_level, delta_thresh, point)
                final = ""
                if status == 0:
                    final = "Z"
                elif status == 1:
                    final = "OFF"
                elif status == 2:
                    final = "ON"
                # print("LED 4", point, item1[i][0], item1[i][1])
                if previous_threshold_value4 is not None:
                    threshold_diff4 = point - previous_threshold_value4
                    if abs(threshold_diff4) <= 5:
                        pass
                    elif delta_blink < abs(threshold_diff4):

                        dem_am4 = dem_am4 + 1
                        # print("-", dem_am4)

                previous_threshold_value4 = point

                sum_blink = get_led_blink4(dem_am4)
                # print("sum", sum_blink)
                cv2.putText(frame, f"LED 4:{point}:{final}:{sum_blink}", (item1[i][0] - 50, item1[i][1] + 55),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 0, 0), 2)
        cv2.putText(
            frame,
            f"LED(1-4):(Threshold):(Status):(Blink)",
            (90, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 0, 0),
            2
        )
        frame_count += 1
        if frame_count > 0:
            end_time = time.time()
            elapsed_time = end_time - start_time
            fps = frame_count / elapsed_time
            frame_count = 0
            start_time = time.time()

        cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.imshow("Test Led", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
    video.release()
    cv2.destroyAllWindows()
