import math
import sys
import json
import cv2
import numpy as np
import logging
import time
from time import sleep
import paho.mqtt.client as mqtt
from paho.mqtt import publish

from blink_test import add_status, add_color, _calculator_blink, clean_blink, get1

R_MIN = 35
R_MAX = 40
DISTANCE_SWITCH = 100
DISTANCE_THRESH = 18
DELAY = 0.4

MQTT_SERVER = "localhost"
MQTT_PORT = 1883

test = "test"
post = "host/camera"
get = "client/camera"

led1 = ""
led2 = ""
led3 = ""
led4 = ""

sum_blink1 = 0
sum_blink2 = 0
sum_blink3 = 0
sum_blink4 = 0

ketqua1 = []
ketqua2 = []
ketqua3 = []
ketqua4 = []

color1 = ""
color2 = ""
color3 = ""
color4 = ""

cmd = ""
event = ""

clear1 = 0


def ketqua():
    global ketqua1
    print("ok1", ketqua1)
    ketqua1 = []


def on_connect(client, userdata, flags, rc):
    print('Đã kết nối với mã kết quả: ' + str(rc))
    client.subscribe(test)
    client.subscribe(post)
    client.subscribe(get)


def on_message(client, userdata, msg):
    global cmd, event, ketqua1, clear1
    host_data = {
        "switch": 0,
        "cmd": cmd,
        "event": event
    }
    data = json.dumps(host_data)
    if msg.topic == test and msg.payload == b'start':
        cmd = "start"
    if msg.topic == test and msg.payload == b'get':
        cmd = "get"
    if msg.topic == test and msg.payload == b'blink':
        event = "blink"
    if msg.topic == test and msg.payload == b'status':
        event = "status"
    if msg.topic == test and msg.payload == b'color':
        event = "color"
    print(data)
    if msg.topic == post and msg.payload == b'test':
        publish.single(get, payload=data, hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)

    if msg.topic == post and msg.payload == b'clear':
        clear()

    if msg.topic == get and json.loads(msg.payload) == host_data:
        if host_data["cmd"] == "get":
            if host_data["event"] == "blink":
                publish.single(post, payload=case_blink, hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)
            elif host_data["event"] == "status":
                publish.single(post, payload=case_status, hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)
            elif host_data["event"] == "color":
                publish.single(post, payload=case_color, hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)

# Start the MQTT client loop
client.loop_start()


# ok
def _add_thresh(thresh_list, thresh=0):
    for i in thresh_list:
        if abs(int(thresh) - int(i)) >= DISTANCE_THRESH:
            continue
        else:
            return thresh_list
    thresh_list.append(thresh)
    return thresh_list

# ok


def _add_switch(switch_list, switch=(0, 0, 0)):
    for i in switch_list:
        if abs(int(switch[0]) - int(i[0])) >= DISTANCE_SWITCH or abs(int(switch[1]) - int(i[1])) >= DISTANCE_SWITCH:
            continue
        else:
            return switch_list
    switch_list.append(switch)
    return switch_list


def average_and_draw_circle1(img, _a, _b, _r):
    points = []
    _gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for _r in range(_r - 5, _r - 1, 1):
        # 2 1
        for x in range(_a - _r, _a + _r, 1):
            y = int(-(_r ** 2 - (x - _a) ** 2) ** 0.5 + _b)
            points.append(_gray[y, x])
            cv2.rectangle(img, (x, y), (x, y), (0, 0, 255), 1)

    return img, int(sum(points) / len(points))


def average_and_draw_circle2(img, _a, _b, _r):
    points = []
    _gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for _r in range(_r - 5, _r - 1, 1):

        # 3 4
        for x in range(_a - _r, _a + _r, 1):
            y = int((_r ** 2 - (x - _a) ** 2) ** 0.5 + _b)
            points.append(_gray[y, x])
            cv2.rectangle(img, (x, y), (x, y), (255, 0, 0), 1)
    return img, int(sum(points) / len(points))


def average_circle(img, _a, _b, _r):
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


def detect_state(thresh_list, delta_list, current_thresh=0):
    # logging.info("Thresh:%d - %d - %d - %d", current_thresh, thresh_list[0], thresh_list[1], thresh_list[2])

    if thresh_list[0] + delta_list[0] > current_thresh:
        return 0
    elif thresh_list[1] + delta_list[1] > current_thresh > thresh_list[1] - delta_list[0]:
        return 1
    elif current_thresh > thresh_list[2] - delta_list[2]:
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


def put_number_to_img(img, pos):
    for i in range(0, len(pos), 1):
        number = i + 1
        cv2.putText(img, str(number), (pos[i][0] - 20, pos[i][1]), cv2.FONT_HERSHEY_SIMPLEX, 1, color=(255, 0, 0), thickness=2)
    return img


def put_color_to_img(img, pos=(0, 0, 0), color=0):
    if color > 2:
        cv2.putText(img, "Z", (pos[0], pos[1] + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color=(0, 255, 255), thickness=2)
    if color == 0:
        cv2.putText(img, "RED", (pos[0], pos[1] + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color=(0, 0, 255), thickness=2)
    elif color == 1:
        cv2.putText(img, "GREEN", (pos[0], pos[1] + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color=(0, 255, 0), thickness=2)
    elif color == 2:
        cv2.putText(img, "BLUE", (pos[0], pos[1] + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, color=(255, 0, 0), thickness=2)
    return img


def _bubblesort(elements):
    for n in range(len(elements)-1, 0, -1):
        for i in range(n):
            if elements[i] > elements[i + 1]:
                elements[i], elements[i + 1] = elements[i + 1], elements[i]
    return elements


def detect_switch(camera, num_switch):
    switch_list = []
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
                switch_list = _add_switch(switch_list, (a, b, r))

    x_average = 0
    y_average = 0
    for i in range(0, num_switch, 1):
        x_average += switch_list[i][0]
        y_average += switch_list[i][1]
    x_average = x_average / num_switch
    y_average = y_average / num_switch

    temp = list()
    if num_switch == 4:
        temp = [0, 0, 0, 0]
        for i in range(0, num_switch, 1):
            if switch_list[i][0] < x_average and switch_list[i][1] < y_average:
                temp[3] = switch_list[i]
            elif switch_list[i][0] > x_average and switch_list[i][1] < y_average:
                temp[2] = switch_list[i]
            elif switch_list[i][0] < x_average and switch_list[i][1] > y_average:
                temp[1] = switch_list[i]
            else:
                temp[0] = switch_list[i]
    switch_list = temp
    return switch_list


def detect_thresh(camera, switch_pos, num_switch):
    thresh_list = []
    delta_list = []
    while True:
        sleep(DELAY)
        if len(thresh_list) >= 3:
            logging.info("Detect thresh success!")
            break
        _ret, _image = camera.read()

        if not _ret:
            logging.error("Camera error")
            break
        cv2.imshow("Test Led", _image)
        _key = cv2.waitKey(1) & 0xFF
        if _key == ord('q'):
            break
        sum_point = 0
        for i in range(0, num_switch, 1):
            sum_point += average_circle(_image, switch_pos[i][0], switch_pos[i][1], switch_pos[i][2])
        thresh_list = _add_thresh(thresh_list, int(sum_point / num_switch))
    thresh_list = _bubblesort(thresh_list)
    delta_list.append(int((thresh_list[1] - thresh_list[0]) / 2))
    delta_list.append(int((thresh_list[2] - thresh_list[1]) * 2 / 3))
    delta_list.append(int((thresh_list[2] - thresh_list[1]) * 1 / 3))
    return thresh_list, delta_list


def detect_color(_img, _a, _b, _r):
    r = list()
    g = list()
    b = list()
    for _r in range(_r - 5, _r - 1, 1):
        for x in range(_a - _r, _a + _r, 1):
            y = int(-(_r ** 2 - (x - _a) ** 2) ** 0.5 + _b)
            pixel = _img[y, x]
            r.append(pixel[2])
            g.append(pixel[1])
            b.append(pixel[0])

        for x in range(_a - _r, _a + _r, 1):
            y = int((_r ** 2 - (x - _a) ** 2) ** 0.5 + _b)
            pixel = _img[y, x]
            r.append(pixel[2])
            g.append(pixel[1])
            b.append(pixel[0])

    average_r = int(sum(r) / len(r))
    average_g = int(sum(g) / len(g))
    average_b = int(sum(b) / len(b))
    # print("R=", average_r, "G=", average_g, "B=", average_b)
    if average_r < 175 and average_g < 175 and average_b < 175:
        return 3
    if average_r > average_g and average_r > average_b:
        return 0
    if average_g > average_r and average_g > average_b:
        return 1
    if average_b > average_g and average_b > average_r:
        return 2
    return 3


previous_threshold_value1 = None
previous_threshold_value2 = None
previous_threshold_value3 = None
previous_threshold_value4 = None
dem_am1 = 0
dem_am2 = 0
dem_am3 = 0
dem_am4 = 0
base = 10
delta_blink = 12
fps = 0
frame_count = 0


def get_status1():
    global led1, sum_blink1
    return led1, sum_blink1


def get_status2():
    global led2, sum_blink2
    return led2, sum_blink2


def get_status3():
    global led3, sum_blink3
    return led3, sum_blink3


def get_status4():
    global led4, sum_blink4
    return led4, sum_blink4


def clear():
    get1()


if __name__ == "__main__":
    video = cv2.VideoCapture(2)
    if not video.isOpened():
        logging.error("Failed to open the video file.")
        sys.exit()

    switch_pos1 = detect_switch(video, 4)
    thresh_level, delta_thresh = detect_thresh(video, switch_pos1, 4)
    time.sleep(2)
    start_time = time.time()
    while True:
        ret, frame = video.read()
        if not ret:
            logging.error("Camera error")
            break

        led1, sum_blink1 = get_status1()
        led2, sum_blink2 = get_status2()
        led3, sum_blink3 = get_status3()
        led4, sum_blink4 = get_status4()

        blink_data = {
            "switch": 0,
            "blink": [sum_blink1, sum_blink2, sum_blink3, sum_blink4]
        }
        status_data = {
            "switch": 0,
            "status": [led1, led2, led3, led4]
        }
        color_data = {
            "switch": 0,
            "color": [color1, color2, color3, color4]
        }
        case_blink = json.dumps(blink_data)
        case_status = json.dumps(status_data)
        case_color = json.dumps(color_data)

        a_sum = 0
        b_sum = 0

        for pos in switch_pos1:
            a_sum += pos[0]
            b_sum += pos[1]

        a_avg = a_sum / 4
        b_avg = b_sum / 4
        center = (int(a_avg), int(b_avg))
        item1 = []
        for i in range(0, 4, 1):
            item = tuple(switch_pos1[i][:2])
            item1.append(item)
            if item1[i][0] > center[0] and item1[i][1] > center[1]:
                color1 = detect_color(frame, item1[i][0], item1[i][1], switch_pos1[i][2])
                frame, point = average_and_draw_circle1(frame, item1[i][0], item1[i][1], switch_pos1[i][2])
                frame = put_color_to_img(frame, switch_pos1[i], color1)
                led1 = detect_state(thresh_level, delta_thresh, point)
                frame = put_state_to_img(frame, switch_pos1[i], detect_state(thresh_level, delta_thresh, point))
                frame = put_number_to_img(frame, switch_pos1)
                # call blink_test.py
                ketqua1 = add_status(0, detect_state(thresh_level, delta_thresh, point))
                sum_blink1 = _calculator_blink(ketqua1)
                cv2.putText(frame, f"{point}:{sum_blink1}:{led1}", (item1[i][0] - 50, item1[i][1] + 55),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 0, 0), 2)
            elif item1[i][0] < center[0] and item1[i][1] > center[1]:
                color2 = detect_color(frame, item1[i][0], item1[i][1], switch_pos1[i][2])
                frame, point = average_and_draw_circle1(frame, item1[i][0], item1[i][1], switch_pos1[i][2])
                frame = put_color_to_img(frame, switch_pos1[i], color2)
                led2 = detect_state(thresh_level, delta_thresh, point)
                frame = put_state_to_img(frame, switch_pos1[i], detect_state(thresh_level, delta_thresh, point))
                frame = put_number_to_img(frame, switch_pos1)
                # call blink_test.py
                ketqua2 = add_status(1, detect_state(thresh_level, delta_thresh, point))
                sum_blink2 = _calculator_blink(ketqua2)

                cv2.putText(frame, f"{point}:{sum_blink2}:{led2}", (item1[i][0] - 50, item1[i][1] + 55),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 0, 0), 2)
            elif item1[i][0] > center[0] and item1[i][1] < center[1]:
                color3 = detect_color(frame, item1[i][0], item1[i][1], switch_pos1[i][2])
                frame, point = average_and_draw_circle2(frame, item1[i][0], item1[i][1], switch_pos1[i][2])
                frame = put_color_to_img(frame, switch_pos1[i], color3)
                led3 = detect_state(thresh_level, delta_thresh, point)
                frame = put_state_to_img(frame, switch_pos1[i], detect_state(thresh_level, delta_thresh, point))
                frame = put_number_to_img(frame, switch_pos1)
                # call blink_test.py
                ketqua3 = add_status(2, detect_state(thresh_level, delta_thresh, point))
                sum_blink3 = _calculator_blink(ketqua3)
                cv2.putText(frame, f"{point}:{sum_blink3}:{led3}", (item1[i][0] - 50, item1[i][1] + 55),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 0, 0), 2)
            elif item1[i][0] < center[0] and item1[i][1] < center[1]:
                color4 = detect_color(frame, item1[i][0], item1[i][1], switch_pos1[i][2])
                frame, point = average_and_draw_circle2(frame, item1[i][0], item1[i][1], switch_pos1[i][2])
                frame = put_color_to_img(frame, switch_pos1[i], color4)
                led4 = detect_state(thresh_level, delta_thresh, point)
                frame = put_state_to_img(frame, switch_pos1[i], detect_state(thresh_level, delta_thresh, point))
                frame = put_number_to_img(frame, switch_pos1)
                # call blink_test.py
                ketqua4 = add_status(3, detect_state(thresh_level, delta_thresh, point))
                sum_blink4 = _calculator_blink(ketqua4)
                cv2.putText(frame, f"{point}:{sum_blink4}:{led4}", (item1[i][0] - 50, item1[i][1] + 55),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 0, 0), 2)

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
