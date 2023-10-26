import cv2
import time
import numpy as np
import sys
import os
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

MQTT_SERVER = "localhost"
MQTT_PORT = 1883
message_id = 0

topic_camera_blink_receive = "clear"


def on_connect(client, userdata, flags, rc):
    print('Đã kết nối với mã kết quả: ' + str(rc))

    client.subscribe(topic_camera_blink_receive)


def on_message(client, userdata, msg):
    if msg.topic == topic_camera_blink_receive and msg.payload == b'Clear':
        clear()
        print("OK 2")


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
    # for t in range(11):
    # print(t*10, "%", end=' ')
    # time.sleep(1)
    # if t > 11:
    # break
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

    if thresh_list[1] > thresh_list[2]:
        temp = thresh_list[1]
        thresh_list[1] = thresh_list[2]
        thresh_list[2] = temp

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


def clear():
    global dem_am1, dem_am2, dem_am3, dem_am4
    dem_am1 = 0
    dem_am2 = 0
    dem_am3 = 0
    dem_am4 = 0


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
    print("OK")
    start_time = time.time()
    while True:
        ret, frame = video.read()
        if not ret:
            logging.error("Camera error")
            break

        a_sum = 0
        b_sum = 0

        for pos in switch_pos:
            a_sum += pos[0]
            b_sum += pos[1]

        a_avg = a_sum / NUM_SWITCH
        b_avg = b_sum / NUM_SWITCH
        # cv2.circle(frame, (int(a_avg), int(b_avg)), 2, (0, 165, 255), -1)
        center = (int(a_avg), int(b_avg))
        # print("center", center)
        # print("data", switch_pos)

        item1 = []
        for i in range(4):
            item = tuple(switch_pos[i][:2])
            item1.append(item)

        for i in range(0, NUM_SWITCH, 1):
            # print(item1[i])
            if item1[i][0] > center[0] and item1[i][1] > center[1]:

                frame, point = cal_average_and_draw_circle1(frame, item1[i][0], item1[i][1], switch_pos[i][2])
                frame = put_state_to_img(frame, switch_pos[i], state(thresh_level, delta_thresh, point))
                status = state(thresh_level, delta_thresh, point)
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
                    elif 11 < abs(threshold_diff1):

                        dem_am1 = dem_am1 + 1
                        print("-", dem_am1)
                    # Case Z chen vao qua trinh

                previous_threshold_value1 = point

                sum_blink = math.ceil((dem_am1 - 1) / 2)
                # print("sum", sum_blink)
                cv2.putText(frame, f"LED 1:{point}:{final}:{sum_blink}", (item1[i][0] - 50, item1[i][1] + 55),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 0, 0), 2)
            elif item1[i][0] < center[0] and item1[i][1] > center[1]:

                frame, point = cal_average_and_draw_circle1(frame, item1[i][0], item1[i][1], switch_pos[i][2])
                frame = put_state_to_img(frame, switch_pos[i], state(thresh_level, delta_thresh, point))
                status = state(thresh_level, delta_thresh, point)
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
                    elif 11 < abs(threshold_diff2):

                        dem_am2 = dem_am2 + 1
                        print("-", dem_am2)
                    # Case Z chen vao qua trinh

                previous_threshold_value2 = point

                sum_blink = math.ceil((dem_am2 - 1) / 2)
                # print("sum", sum_blink)
                cv2.putText(frame, f"LED 2:{point}:{final}:{sum_blink}", (item1[i][0] - 50, item1[i][1] + 55),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 0, 0), 2)
            elif item1[i][0] > center[0] and item1[i][1] < center[1]:

                frame, point = cal_average_and_draw_circle2(frame, item1[i][0], item1[i][1], switch_pos[i][2])
                frame = put_state_to_img(frame, switch_pos[i], state(thresh_level, delta_thresh, point))
                status = state(thresh_level, delta_thresh, point)
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
                    elif 11 < abs(threshold_diff3):

                        dem_am3 = dem_am3 + 1
                        print("-", dem_am3)
                    # Case Z chen vao qua trinh

                previous_threshold_value3 = point

                sum_blink = math.ceil((dem_am3 - 1) / 2)
                # print("sum", sum_blink
                cv2.putText(frame, f"LED 3:{point}:{final}:{sum_blink}", (item1[i][0] - 50, item1[i][1] + 55),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 0, 0), 2)
            elif item1[i][0] < center[0] and item1[i][1] < center[1]:

                frame, point = cal_average_and_draw_circle2(frame, item1[i][0], item1[i][1], switch_pos[i][2])
                frame = put_state_to_img(frame, switch_pos[i], state(thresh_level, delta_thresh, point))
                status = state(thresh_level, delta_thresh, point)
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
                    elif 11 < abs(threshold_diff4):

                        dem_am4 = dem_am4 + 1
                        print("-", dem_am4)
                    # Case Z chen vao qua trinh

                previous_threshold_value4 = point

                sum_blink = math.ceil((dem_am4 - 1) / 2)
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
