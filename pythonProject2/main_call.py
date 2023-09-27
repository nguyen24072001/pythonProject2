import cv2
from btn_test import sw01_get_status, sw02_get_status, sw03_get_status, sw04_get_status


def main():
    # video = cv2.VideoCapture("CASE_BLINK_LED1.mp4")
    video = cv2.VideoCapture(2)
    if not video.isOpened():
        print("Failed to open the video file.")
        return

    while True:
        # Đọc frame từ video
        ret, frame = video.read()

        # Kiểm tra nếu không thể đọc thêm frame
        if not ret:
            break
        image1 = frame
        # cap = cv2.VideoCapture(2)

        # while True:
        # Đọc khung hình từ luồng ảnh
        # ret, image = cap.read()
        # if not ret:print("Số lượng:", dem_led)
        #     led_results.append(f"{int(dem_led)}")
        # break

        # image1 = cv2.imread("CASE_BLINK_LED1.mp4")
        # image2 = cv2.imread("sw02_on.jpg")
        # image3 = cv2.imread("sw03_on.jpg")
        # image4 = cv2.imread("/home/lqptoptvt/PycharmProjects/pythonProject2/16led/1111.jpg")

        sw01_get_status(image1)

        # sw02_get_status(image2)
        # sw03_get_status(image3)
        # sw04_get_status(image4)

        # cv2.imshow("SW01", image1)
        # cv2.imshow("SW02", image2)
        # cv2.imshow("SW03", image3)
        # cv2.imshow("SW04", image4)

        # Display the resized image
        cv2.imshow("BLINK", image1)

        if cv2.waitKey(1) == ord('q'):
            break

        # cap.release()
        # cv2.waitKey(0)
    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
