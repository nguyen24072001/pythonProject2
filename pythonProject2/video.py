import cv2
import time


def main():
    camera = cv2.VideoCapture(2)

    # Get the video dimensions and FPS
    width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(camera.get(cv2.CAP_PROP_FPS))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('CASE_4blink.mp4', fourcc, fps, (width, height))

    while True:
        ret, frame = camera.read()
        if not ret:
            print("Failed to capture frame")
            break

        cv2.imshow("Camera Test", frame)
        out.write(frame)

        if cv2.waitKey(1) == ord('q'):
            break

    # Release the video writer, camera, and close windows
    out.release()
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
