import cv2
from btn_test import sw01_get_status, blink_led1


def main():
    # video = cv2.VideoCapture("CASE_BLINK_LED1.mp4")
    # video = cv2.VideoCapture("CASE_BLINK_LED1v2.mp4")
    # video = cv2.VideoCapture("CASE_BLINK_LED1v3.mp4")
    # video = cv2.VideoCapture(2)
    video = cv2.VideoCapture("blink_off.jpg")
    # video = cv2.VideoCapture("LED_ON.jpg")
    # video = cv2.VideoCapture("sw01_off_Z.jpg")
    if not video.isOpened():
        print("Failed to open the video file.")
        return

    while True:
        # Đọc frame từ video
        ret, frame = video.read()

        # Kiểm tra nếu không thể đọc thêm frame
        if not ret:
            break

        # Xử lý ảnh và xác định vùng trắng
        anh = frame
        sw01_get_status(anh)
        blink_led1(anh)
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
