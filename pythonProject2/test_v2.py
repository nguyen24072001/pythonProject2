import cv2
import numpy as np


def led1(img):
    # img = cv2.GaussianBlur(img, (5, 5), 0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detected_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 150, param1=50, param2=30, minRadius=30,
                                        maxRadius=40)
    # img = cv2.GaussianBlur(img, (5, 5), 0)
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    point_list = []
    sum_list = []
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            # img = cv2.GaussianBlur(img, (5, 5), 0)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # histogram
            img, point = calculator_color(img, gray, a, b, r)

            point_list.append(point)  # Add point
            if len(point_list) > 100:
                point_list = point_list[-100:]  # SUM = 20
            average = sum(point_list) / len(point_list) if len(point_list) > 0 else 0

            # print("Average =", average)
            # Display point
            text = f"{average}"
            cv2.putText(img, "1|", (a-40, b), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

            cv2.putText(img, text, (a-12, b), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            if average > 230:

                cv2.putText(img, "ON", (25, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
            elif 170 < average < 230:

                cv2.putText(img, "OFF", (40, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
            elif average < 170:

                cv2.putText(img, "Z", (40, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

            # print("point 1 =", point)

    return img


def led2(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detected_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 150, param1=50, param2=30, minRadius=30,
                                        maxRadius=40)
    point_list = []
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            img, point = calculator_color(img, gray, a, b, r)
            point_list.append(point)  # Add point
            if len(point_list) > 100:
                point_list = point_list[-100:]  # SUM = 20
            average = sum(point_list) / len(point_list) if len(point_list) > 0 else 0

            # print("Average 2 =", average)
            # Display point
            text = f"{average}"
            cv2.putText(img, "2|", (a - 40, b), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

            cv2.putText(img, text, (a - 12, b), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            if average > 230:
                cv2.putText(img, "ON", (25, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
            elif 180 < average < 230:
                cv2.putText(img, "OFF", (40, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
            elif average < 190:
                cv2.putText(img, "Z", (40, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

            print("point 2 =", point)

    return img


def led3(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detected_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 150, param1=50, param2=30, minRadius=30,
                                        maxRadius=40)
    point_list = []
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            img, point = calculator_color(img, gray, a, b, r)
            point_list.append(point)  # Add point
            if len(point_list) > 100:
                point_list = point_list[-100:]  # SUM = 20
            average = sum(point_list) / len(point_list) if len(point_list) > 0 else 0

            # print("Average =", average)
            # Display point
            text = f"{average}"
            cv2.putText(img, "3|", (a - 40, b), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

            cv2.putText(img, text, (a - 12, b), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            if average > 230:
                cv2.putText(img, "ON", (25, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
            elif 180 < average < 230:
                cv2.putText(img, "OFF", (40, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
            elif average < 190:
                cv2.putText(img, "Z", (40, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

            # print("point 3 =", point)

    return img


def led4(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detected_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 150, param1=50, param2=30, minRadius=30,
                                        maxRadius=40)
    point_list = []
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            img, point = calculator_color(img, gray, a, b, r)
            point_list.append(point)  # Add point
            if len(point_list) > 100:
                point_list = point_list[-100:]  # SUM = 20
            average = sum(point_list) / len(point_list) if len(point_list) > 0 else 0

            # print("Average =", average)
            # Display point
            text = f"{average}"
            cv2.putText(img, "4|", (a - 42, b), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

            cv2.putText(img, text, (a - 14, b), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            if average > 225:
                cv2.putText(img, "ON", (25, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
            elif 180 < average < 225:
                cv2.putText(img, "OFF", (40, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
            elif average < 190:
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
            # center = (a, b)

            # Hiển thị tọa độ tâm
            # text = "({}, {})".format(a, b)
            # cv2.putText(img, text, (a, b), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # Vẽ chấm xanh dương
            # cv2.circle(img, center, 2, (255, 0, 0), -1)

            # Nguong
            img, point = calculator_color(img, gray, a, b, r)
            # print("point = ", point)
            save_center_values(a, b)
    return img


min_a = float('inf')  # Initialize min_a with infinity
min_b = float('inf')  # Initialize min_b with infinity
max_a = float('-inf')  # Initialize max_a with negative infinity
max_b = float('-inf')  # Initialize max_b with negative infinity


def save_center_values(a, b):
    global min_a, min_b, max_a, max_b

    # Update the minimum values
    if a < min_a:
        min_a = a
    if b < min_b:
        min_b = b

    # Update the maximum values
    if a > max_a:
        max_a = a
    if b > max_b:
        max_b = b


def calculator_color(img, gray, a, b, r):
    points = []
    for r in range(r - 3, r, 1):
        for x in range(a - r, a + r, 1):
            y = int(-(r ** 2 - (x - a) ** 2) ** 0.5 + b)
            points.append(gray[y, x])
            # cv2.rectangle(img, (x, y), (x, y), (0, 0, 255), 1)

        for x in range(a - r, a + r, 1):
            y = int((r ** 2 - (x - a) ** 2) ** 0.5 + b)
            points.append(gray[y, x])
            # cv2.rectangle(img, (x, y), (x, y), (0, 0, 255), 1)

    return img, int(sum(points)/len(points))


def main():
    # video = cv2.VideoCapture("demo_gray.mp4")
    video = cv2.VideoCapture(2)
    if not video.isOpened():
        print("Failed to open the video file.")
        return

    save_images = False
    frame_count = 0

    while True:
        ret, frame = video.read()

        if not ret:
            break
        # frame = cv2.GaussianBlur(frame, (9, 9), 0)
        frame = cv2.blur(frame,(5, 5))
        anh_xam = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        anh_tron = circle_detection(frame)

        anh1 = crop_image_case1(frame, max_a, max_b, 97)
        anh2 = crop_image_case2(frame, min_a, max_b, 97)
        anh3 = crop_image_case3(frame, max_a, min_b, 97)
        anh4 = crop_image_case4(frame, min_a, min_b, 97)



        final1 = led1(anh1)
        final2 = led2(anh2)
        final3 = led3(anh3)
        final4 = led4(anh4)

        cv2.imshow("Anh Goc", anh_xam)
        cv2.imshow("Anh 2", anh_tron)
        # cv2.imshow("LED 1", anh1)
        # cv2.imshow("LED 2", anh2)
        # cv2.imshow("LED 3", anh3)
        # cv2.imshow("LED 4", anh4)
        # cv2.imshow("final1", final1)
        # cv2.imshow("final2", final2)
        # cv2.imshow("final3", final3)
        # cv2.imshow("final4", final4)
        # cv2.imshow("test", anhhis)
        if save_images:
            cv2.imwrite(f"anh1_on_{frame_count}.jpg", anh1)
            cv2.imwrite(f"anh2_on_{frame_count}.jpg", anh2)
            cv2.imwrite(f"anh3_on_{frame_count}.jpg", anh3)
            cv2.imwrite(f"anh4_on_{frame_count}.jpg", anh4)
            frame_count += 1
            save_images = False

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            save_images = True

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
