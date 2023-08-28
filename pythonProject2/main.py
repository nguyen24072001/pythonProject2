import cv2
import time


def main():
    camera = cv2.VideoCapture(2)

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to capture frame")
            break

        cv2.imshow("Camera Test", frame)

        if cv2.waitKey(1) == ord('q'):
            break
    # Sau 2s thi chup anh
    time.sleep(2)
    # Capture an image
    ret, frame = camera.read()
    if ret:
        cv2.imwrite("Xanh_tron_tat.jpg", frame)
        print("OK")
    else:
        print("None")

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
