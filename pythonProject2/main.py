import cv2
import time


def main():
    camera = cv2.VideoCapture(2)

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to capture frame")
            break
        # Thiết lập kích thước hình vuông
        x = 300  # Chiều dài hình vuông
        y = 300  # Chiều rộng hình vuông
        # Tính toán vị trí của hình vuông
        top_left = (250, 0)
        bottom_right = (top_left[0] + x, top_left[1] + y)
        # cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)
        cropped_frame = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
        #
        cv2.imshow("Camera Test", frame)
        # cv2.imshow("Camera Test", frame)
        if cv2.waitKey(1) == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
