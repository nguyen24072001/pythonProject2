import cv2
import time
import numpy as np


def led1(img, a1_value, b1_value, r1_value):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    point_list = []

    img, point = calculator_color(img, gray, a1_value, b1_value, r1_value)
    point_list.append(point)
    if len(point_list) > 100:
        point_list = point_list[-100:]

    average = sum(point_list) / len(point_list) if len(point_list) > 0 else 0

    text = f"{average:.2f}"
    cv2.putText(img, "1|", (a1_value-40, b1_value), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
    cv2.putText(img, text, (a1_value-12, b1_value), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    if average > 230:
        cv2.putText(img, "ON", (25, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
    elif 180 < average < 230:
        cv2.putText(img, "OFF", (40, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
    elif average < 180:
        cv2.putText(img, "Z", (40, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

    # print("point 1 =", average)

    return img


def led2(img, a2_value, b2_value):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    point_list = []
    img, point = calculator_color(img, gray, a2_value, b2_value, r1)

    point_list.append(point)  # Add point
    if len(point_list) > 100:
        point_list = point_list[-100:]  # SUM = 20
    average = sum(point_list) / len(point_list) if len(point_list) > 0 else 0

    # print("Average 2 =", average)
    # Display point
    text = f"{average}"
    cv2.putText(img, "2|", (a2_value - 40, b2_value), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

    cv2.putText(img, text, (a2_value - 12, b2_value), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    if average > 230:
        cv2.putText(img, "ON", (25, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
    elif 180 < average < 230:
        cv2.putText(img, "OFF", (40, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
    elif average < 180:
        cv2.putText(img, "Z", (40, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

    # print("point 2 =", point)

    return img


def led3(img, a3_value, b3_value):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    point_list = []
    img, point = calculator_color(img, gray, a3_value, b3_value, r1)

    point_list.append(point)  # Add point
    if len(point_list) > 100:
        point_list = point_list[-100:]  # SUM = 20
    average = sum(point_list) / len(point_list) if len(point_list) > 0 else 0

    # print("Average =", average)
    # Display point
    text = f"{average}"
    cv2.putText(img, "3|", (a3_value - 40, b3_value), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

    cv2.putText(img, text, (a3_value - 12, b3_value), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    if average > 230:
        cv2.putText(img, "ON", (25, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
    elif 180 < average < 230:
        cv2.putText(img, "OFF", (40, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
    elif average < 180:
        cv2.putText(img, "Z", (40, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

    # print("point 3 =", point)

    return img


def led4(img, a4_value, b4_value):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    point_list = []
    img, point = calculator_color(img, gray, a4_value, b4_value, r1)

    point_list.append(point)  # Add point
    if len(point_list) > 100:
        point_list = point_list[-100:]  # SUM = 20
    average = sum(point_list) / len(point_list) if len(point_list) > 0 else 0

    # print("Average =", average)
    # Display point
    text = f"{average}"
    cv2.putText(img, "4|", (a4_value - 42, b4_value), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

    cv2.putText(img, text, (a4_value - 14, b4_value), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    if average > 230:
        cv2.putText(img, "ON", (25, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
    elif 180 < average < 230:
        cv2.putText(img, "OFF", (40, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
    elif average < 180:
        cv2.putText(img, "Z", (40, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

    # print("point 4 =", point)

    return img


def crop_image_case1(img, a, b, square_length):
    x1 = a - square_length // 2
    y1 = b - square_length // 2
    x2 = a + square_length // 2
    y2 = b + square_length // 2
    cropped_img = img[y1:y2, x1:x2]
    return cropped_img


def crop_image_case2(img, a, b, square_length):
    x1 = a - square_length // 2
    y1 = b - square_length // 2
    x2 = a + square_length // 2
    y2 = b + square_length // 2
    cropped_img = img[y1:y2, x1:x2]
    return cropped_img


def crop_image_case3(img, a, b, square_length):
    x1 = a - square_length // 2
    y1 = b - square_length // 2
    x2 = a + square_length // 2
    y2 = b + square_length // 2
    cropped_img = img[y1:y2, x1:x2]
    return cropped_img


def crop_image_case4(img, a, b, square_length):
    x1 = a - square_length // 2
    y1 = b - square_length // 2
    x2 = a + square_length // 2
    y2 = b + square_length // 2
    cropped_img = img[y1:y2, x1:x2]
    return cropped_img


def circle_detection(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detected_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 150, param1=50, param2=30, minRadius=30,
                                        maxRadius=40)
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            center = (a, b)

            # print("R all", r)

                # print("point = ", point)
            save_center_values(a, b, r)
    return img

sum1 = any
def ab1(img):
    global sum1
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detected_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 150, param1=50, param2=30, minRadius=30,
                                        maxRadius=40)
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            sum1 = (a, b, r)
            break
        # print("ab1", sum1)
    return sum1


sum2 = any
def ab2(img):
    global sum2
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detected_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 150, param1=50, param2=30, minRadius=30,
                                        maxRadius=40)
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            a, b = pt[0], pt[1]
            sum2 = (a, b)
        # print("ab2", sum2)
    return sum2

sum3 = any
def ab3(img):
    global sum3
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detected_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 150, param1=50, param2=30, minRadius=30,
                                        maxRadius=40)
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            a, b = pt[0], pt[1]
            sum3 = (a, b)
        # print("ab3", sum3)
    return sum3


sum4 = any
def ab4(img):
    global sum4
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detected_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 150, param1=50, param2=30, minRadius=30,
                                        maxRadius=40)
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            a, b = pt[0], pt[1]
            sum4 = (a, b)
        # print("ab1", sum4)
    return sum4


min_a = float('inf')  # Initialize min_a with infinity
min_b = float('inf')  # Initialize min_b with infinity
max_a = float('-inf')  # Initialize max_a with negative infinity
max_b = float('-inf')  # Initialize max_b with negative infinity
r1 = any


def save_center_values(a, b, r):
    global min_a, min_b, max_a, max_b, r1

    # Update the minimum values
    while a < min_a:
        min_a = a
        break
    while b < min_b:
        min_b = b
        break
    # Update the maximum values
    while a > max_a:
        max_a = a
        break
    while b > max_b:
        max_b = b
        break
    r1 = r


def calculator_color(img, gray, a, b, r):
    points = []
    for r in range(r - 6, r - 2, 1):
        for x in range(a - r, a + r, 1):
            y = int(-(r ** 2 - (x - a) ** 2) ** 0.5 + b)
            points.append(gray[y, x])
            cv2.rectangle(img, (x, y), (x, y), (0, 0, 255), 1)

        for x in range(a - r, a + r, 1):
            y = int((r ** 2 - (x - a) ** 2) ** 0.5 + b)
            points.append(gray[y, x])
            cv2.rectangle(img, (x, y), (x, y), (0, 0, 255), 1)

    return img, int(sum(points)/len(points))


def main():
    video = cv2.VideoCapture("demo_gray.mp4")
    # video = cv2.VideoCapture(2)
    if not video.isOpened():
        print("Failed to open the video file.")
        return

    save_images = False
    frame_count = 0
    start_time = time.time()

    while True:
        ret, frame = video.read()

        if not ret:
            break
        # frame = cv2.GaussianBlur(frame, (9, 9), 0)
        # frame = cv2.blur(frame, (5, 5))
        frame = cv2.medianBlur(frame, 9)
        anh_xam = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        anh_tron = circle_detection(frame)

        anh1 = crop_image_case1(frame, max_a, max_b, 90)
        anh2 = crop_image_case2(frame, min_a, max_b, 90)
        anh3 = crop_image_case3(frame, max_a, min_b, 90)
        anh4 = crop_image_case4(frame, min_a, min_b, 90)

        circle_center1 = ab1(anh1)
        a1_value, b1_value, r1_value = circle_center1
        # print("A1", a1_value, "B1", b1_value)

        circle_center2 = ab2(anh2)
        a2_value, b2_value = circle_center2
        # print("A2", a2_value, "B2", b2_value)

        circle_center3 = ab3(anh3)
        a3_value, b3_value = circle_center3
        # print("A3", a3_value, "B3", b3_value)

        circle_center4 = ab4(anh4)
        a4_value, b4_value = circle_center4
        # print("A4", a4_value, "B4", b4_value)

        final1 = led1(anh1, a1_value, b1_value, r1_value)
        final2 = led2(anh2, a2_value, b2_value)
        final3 = led3(anh3, a3_value, b3_value)
        final4 = led4(anh4, a4_value, b4_value)



        # cv2.imshow("Anh Goc", anh_xam)

        # cv2.imshow("LED 1", anh1)
        # cv2.imshow("LED 2", anh2)
        # cv2.imshow("LED 3", anh3)
        # cv2.imshow("LED 4", anh4)
        # cv2.imshow("final1", final1)
        # cv2.imshow("final2", final2)
        # cv2.imshow("final3", final3)
        # cv2.imshow("final4", final4)
        # cv2.imshow("test", anhhis)
        frame_count += 1
        if save_images:
            cv2.imwrite(f"anh1_on_{frame_count}.jpg", anh1)
            cv2.imwrite(f"anh2_on_{frame_count}.jpg", anh2)
            cv2.imwrite(f"anh3_on_{frame_count}.jpg", anh3)
            cv2.imwrite(f"anh4_on_{frame_count}.jpg", anh4)

            save_images = False
        # Calculate FPS
        end_time = time.time()
        elapsed_time = end_time - start_time
        fps = 1 / elapsed_time
        start_time = end_time

        # Display FPS on the frame
        cv2.putText(anh_tron, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.imshow("Anh Goc", anh_tron)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            save_images = True
    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
