import time
import cv2
from btn_test import calculate_percentage_loss, sw01_get_status, led1
from paho.mqtt import publish

MQTT_SERVER = "localhost"
MQTT_PORT = 1883
message_id = 0
# MQTT topic => publish
MQTT_TOPIC = "SUM_BLINK"


def main():
    # video = cv2.VideoCapture("CASE_BLINK_LED1.mp4")
    # video = cv2.VideoCapture("CASE_BLINK_LED1v2.mp4")
    # video = cv2.VideoCapture("CASE_BLINK_LED1v3.mp4")
    video = cv2.VideoCapture(2)
    if not video.isOpened():
        print("Failed to open the video file.")
        return

    start_time = time.time()
    frame_count = 0
    threshold_time_total = 0
    threshold_count = 0
    previous_threshold_value = None
    total_threshold_diff = 0
    previous_total_threshold_diff = 0
    previous_total_threshold_diff_time = None

    while True:
        # Đọc frame từ video
        ret, frame = video.read()

        # Kiểm tra nếu không thể đọc thêm frame
        if not ret:
            break

        # Xử lý ảnh và xác định vùng trắng
        anh = frame
        sw01_get_status(anh)
        percentage_loss = abs(calculate_percentage_loss(anh)) / 1000

        # Tính giá trị ngưỡng
        start_threshold_time = time.time()
        end_threshold_time = time.time()
        threshold_time_ms = (end_threshold_time - start_threshold_time) * 1000
        # print("Loss 1: {}".format(abs(percentage_loss) / 1000))
        # print("Thời gian tính ngưỡng (ms): ", threshold_time_ms)
        # print(percentage_loss)
        threshold_time_total += threshold_time_ms

        if percentage_loss > 45:
            threshold_count += 1

        # Tính tổng số lần mà giá trị ngưỡng hiện tại trừ giá trị ngưỡng trước đó lớn hơn 50
        if previous_threshold_value is not None:
            threshold_diff = percentage_loss - previous_threshold_value
            if 7 < threshold_diff < 23:
                total_threshold_diff += 1
                if total_threshold_diff - previous_total_threshold_diff == 1:
                    if previous_total_threshold_diff_time is not None:
                        current_time = time.time()
                        time_diff = (current_time - previous_total_threshold_diff_time)
                        print("Khoảng thời gian (s) nháy {} lần và {} lần:".format(total_threshold_diff-1,
                                                                                   total_threshold_diff), time_diff)
                        if time_diff > 3:
                            print("change")
                            publish.single(MQTT_TOPIC, payload=total_threshold_diff-1, hostname=MQTT_SERVER,
                                           port=MQTT_PORT, qos=1)
                            total_threshold_diff = 1
                    previous_total_threshold_diff_time = time.time()

        previous_threshold_value = percentage_loss
        previous_total_threshold_diff = total_threshold_diff
        print("LED Đã Nháy {} Lần !".format(total_threshold_diff))

        # Tính FPS và hiển thị lên frame
        frame_count += 1
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time
        cv2.putText(
            anh,
            f"FPS: {fps:.2f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        current_frame_time = time.time()
        time_diff = current_frame_time - start_time

        cv2.putText(
            anh,
            f"Time: {time_diff:.2f}s",
            (10, 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        cv2.imshow("Anh Goc", anh)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

    total_time = time.time() - start_time
    # print("Tổng số lần ngưỡng trên 200: ", threshold_count)
    # print("Tổng thời gian tính ngưỡng (ms): ", threshold_time_total)
    print("Tổng thời gian (s): ", total_time)
    # print("Tổng số lần mà giá trị ngưỡng hiện tại trừ giá trị ngưỡng trước đó > 50: ", total_threshold_diff)




if __name__ == "__main__":
    main()
