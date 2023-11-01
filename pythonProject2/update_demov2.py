import cv2
import numpy as np
import sys
import os
import logging
from time import sleep

R_MIN = 35
R_MAX = 40
DISTANCE_SWITCH = 100
DISTANCE_THRESH = 18
DELAY = 0.5

def detect_switch(camera, num_switch):
    switch_list = []
    cv2.namedWindow("Switch Detection")

    for i in range(num_switch):
        while True:
            ret, image = camera.read()

            if not ret:
                logging.error("Failed to read frame from video")
                break

            cv2.imshow("Switch Detection", image)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('s'):
                switch_list.append((image, cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)))
                break

            if key == ord('q'):
                cv2.destroyAllWindows()
                return []

    cv2.destroyAllWindows()
    return switch_list

def detect_thresh(camera, switch_list, num_switch):
    thresh_list = []
    delta_list = []
    cv2.namedWindow("Threshold Detection")

    for i in range(num_switch):
        while True:
            ret, image = camera.read()

            if not ret:
                logging.error("Failed to read frame from video")
                break

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            switch_image, switch_gray = switch_list[i]

            diff = cv2.absdiff(gray, switch_gray)
            _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

            cv2.imshow("Threshold Detection", thresh)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('s'):
                thresh_list.append(thresh)
                delta_list.append(diff)
                break

            if key == ord('q'):
                cv2.destroyAllWindows()
                return [], []

    cv2.destroyAllWindows()
    return thresh_list, delta_list

def main():
    video_path = "CASE_4blink.mp4"  # Replace with the path to your video file
    camera = cv2.VideoCapture(video_path)

    if not camera.isOpened():
        logging.error("Failed to open video file")
        return

    num_switch = 4  # Update with the number of switches in your setup
    switch_list = detect_switch(camera, num_switch)

    if len(switch_list) != num_switch:
        logging.error("Failed to detect all switches")
        return

    thresh_list, delta_list = detect_thresh(camera, switch_list, num_switch)

    while True:
        ret, image = camera.read()

        if not ret:
            logging.error("Failed to read frame from video")
            break

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        for i in range(num_switch):
            switch_image, switch_gray = switch_list[i]
            thresh = thresh_list[i]
            delta = delta_list[i]

            diff = cv2.absdiff(gray, switch_gray)
            _, binary = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

            contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                area = cv2.contourArea(contour)

                if area < R_MIN or area > R_MAX:
                    continue

                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                distance = cv2.pointPolygonTest(contour, (x + w // 2, y + h // 2), True)

                if distance < DISTANCE_THRESH:
                    cv2.putText(image, "Switch {}".format(i + 1), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                (0, 255, 0), 2)
                else:
                    cv2.putText(image, "Switch {}".format(i + 1), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                                (0, 0, 255), 2)

        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()