import cv2
import time
import numpy as np
import sys
import os
import logging

CAMERA = 2
# CAMERA = "CASE_4blink.mp4"
R_MIN = 35
R_MAX = 40
DISTANCE_SWITCH = 100
DISTANCE_THRESH = 18
NUM_SWITCH = 4


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


def cal_average_and_draw_circle(img, _a, _b, _r):
    points = []
    _gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for _r in range(_r - 5, _r - 1, 1):
        for x in range(_a - _r, _a + _r, 1):
            y = int(-(_r ** 2 - (x - _a) ** 2) ** 0.5 + _b)
            points.append(_gray[y, x])
            cv2.rectangle(img, (x, y), (x, y), (0, 0, 255), 1)

        for x in range(_a - _r, _a + _r, 1):
            y = int((_r ** 2 - (x - _a) ** 2) ** 0.5 + _b)
            points.append(_gray[y, x])
            cv2.rectangle(img, (x, y), (x, y), (0, 0, 255), 1)
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
        print(switch_list)
        # cv2.imshow("Test Led", _gray)
        # key = cv2.waitKey(1) & 0xFF
        # if key == ord('q'):
          #   break
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

    delta_list.append(int((thresh_list[1] - thresh_list[0]) / 2))
    delta_list.append(int((thresh_list[2] - thresh_list[1]) * 2 / 3))
    delta_list.append(int((thresh_list[2] - thresh_list[1]) * 1 / 3))
    return thresh_list, delta_list
frame_count = 0
fps = 0

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
    print(switch_pos)
    thresh_level, delta_thresh = detect_thresh(thresh_level, delta_thresh, video)
    start_time = time.time()
    while True:
        ret, frame = video.read()
        if not ret:
            logging.error("Camera error")
            break
        for j in range(0, NUM_SWITCH, 1):
            frame, point = cal_average_and_draw_circle(frame, switch_pos[j][0], switch_pos[j][1], switch_pos[j][2])
            frame = put_state_to_img(frame, switch_pos[j], state(thresh_level, delta_thresh, point))
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