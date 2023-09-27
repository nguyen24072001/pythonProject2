import cv2


def repeat_video(input_file, output_file, repeat_count):
    # Mở video đầu vào
    video = cv2.VideoCapture(input_file)
    if not video.isOpened():
        print("Failed to open the video file.")
        return

    # Lấy thông tin về video
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Tạo video writer để ghi video mới
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    # Đọc từng frame từ video đầu vào và ghi vào video mới
    frames = []
    while True:
        ret, frame = video.read()
        if not ret:
            break

        frames.append(frame)

    # Lặp lại video và ghi frame vào video mới
    for _ in range(repeat_count):
        for frame in frames:
            writer.write(frame)

    # Giải phóng các tài nguyên
    video.release()
    writer.release()
    cv2.destroyAllWindows()

    print("Video has been repeated and saved to:", output_file)


# Thực hiện lặp lại video 3 lần và lưu vào file mới
repeat_video("CASE_BLINK_LED1.mp4", "CASE_BLINK_LED1v3.mp4", 3)
