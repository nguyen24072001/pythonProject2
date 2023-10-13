# import argparse
import cv2
import numpy as np


def anh_histogram(image):
    # Chuyển đổi ảnh sang ảnh grayscale
    anh_xam = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Cân bằng lược đồ màu
    anh_can_bang = cv2.equalizeHist(anh_xam)

    # Chuyển đổi ảnh xám thành ảnh màu
    anh_can_bang_mau = cv2.cvtColor(anh_can_bang, cv2.COLOR_GRAY2BGR)

    # Tìm giá trị tối đa và tối thiểu trong ảnh cân bằng
    gia_tri_toi_thieu, gia_tri_toi_da, _, _ = cv2.minMaxLoc(anh_can_bang)

    # Đặt ngưỡng để lọc các pixel có độ tương phản cao hơn ngưỡng
    nguong = gia_tri_toi_da * 0.85

    # Cắt ảnh theo phần có độ tương phản tương đối cao
    anh_cai_tien_tuong_phan = anh_can_bang_mau.copy()
    anh_cai_tien_tuong_phan[anh_can_bang_mau < nguong] = 0

    return anh_cai_tien_tuong_phan


def xac_dinh_vung_trang(anh):
    # Chuyển đổi ảnh sang ảnh grayscale
    anh_xam = cv2.cvtColor(anh, cv2.COLOR_BGR2GRAY)

    # Áp dụng phép toán nhị phân hóa để chuyển đổi ảnh sang dạng nhị phân
    _, anh_nhi_phan = cv2.threshold(anh_xam, 0, 255, cv2.THRESH_BINARY)

    # Tìm các vị trí có giá trị pixel là màu trắng
    vung_trang = np.where(anh_nhi_phan == 255)
    return vung_trang


led_text = ""


def detect_and_draw_circles(image):
    global led_text
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)
    circles = cv2.HoughCircles(gray_blur, cv2.HOUGH_GRADIENT, 1, 20, param1=50, param2=30, minRadius=0, maxRadius=0)

    if circles is not None:
        circles = np.round(circles[0, :]).astype(int)

        if len(circles) >= 4:
            points = circles[:4, :2]  # Lấy tọa độ 4 điểm đầu tiên
            for i, (x, y, r) in enumerate(circles):
                # cv2.circle(image, (x, y), r, (0, 0, 255), 3)
                cv2.circle(image, (x, y), 2, (255, 0, 0), 3, cv2.LINE_AA)

            # Vẽ 4 đường thẳng màu vàng nối 4 điểm
            # cv2.line(image, tuple(points[0]), tuple(points[1]), (0, 255, 255), 2)
            # cv2.line(image, tuple(points[1]), tuple(points[2]), (0, 255, 255), 2)
            # cv2.line(image, tuple(points[2]), tuple(points[3]), (0, 255, 255), 2)
            # cv2.line(image, tuple(points[3]), tuple(points[0]), (0, 255, 255), 2)

            # Tìm giao điểm cách đều 4 chấm xanh dương
            average_point = np.mean(points, axis=0).astype(int)
            # cv2.circle(image, tuple(average_point), 5, (255, 0, 255), -1)

            # Thiết lập tọa độ Oxy dựa vào tâm
            relative_points = points - average_point

            # Hiển thị tọa độ của cả 4 chấm xanh dương và văn bản LED tương ứng
            for i, (x, y) in enumerate(relative_points):
                text = f"({x}, {y})"
                # cv2.putText(image, text, tuple(points[i]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2, cv2.LINE_AA)

                if x < 0 < y:
                    led_text = "1"
                elif x < 0 and y < 0:
                    led_text = "2"
                elif x > 0 and y > 0:
                    led_text = "3"
                elif x > 0 > y:
                    led_text = "4"

                cv2.putText(image, led_text, tuple(points[i]), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 165, 255), 2,
                            cv2.LINE_AA)

                # Cắt ảnh gốc từ tâm của từng tọa độ LED
                radius = circles[i][2]
                diameter = 2 * radius
                center = tuple(circles[i][:2])
                x1 = center[0] - radius - 5
                y1 = center[1] - radius - 5
                x2 = center[0] + radius + 5
                y2 = center[1] + radius + 5
                cropped_img = image[y1:y2, x1:x2]
                # In số lượng pixel vùng trắng của ảnh cắt
                white_pixels = np.sum(cropped_img == [255, 255, 255])
                print(f"Số lượng pixel vùng trắng của ảnh cắt {led_text}: {white_pixels}")

                if white_pixels < 800:
                    print(f"Trạng thái LED {led_text}: OFF")
                    cv2.putText(image, "OFF", tuple(points[i]), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 165, 255), 2,
                                cv2.LINE_AA)
                elif white_pixels > 900:
                    print(f"Trạng thái LED {led_text}: ON")
                    cv2.putText(image, "ON", tuple(points[i]), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 165, 255), 2,
                                cv2.LINE_AA)
                else:
                    print(f"Trạng thái LED {led_text}: Không xác định được")

                cv2.imshow(f"Cropped LED {led_text}", cropped_img)

    return image


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

        anh = frame
        anh_cai_tien = anh_histogram(anh)

        vung_trang = xac_dinh_vung_trang(anh_cai_tien)
        # print("Thông số vùng trắng: ", vung_trang)

        # Trích xuất giá trị phổ từ vùng trắng
        spectral_values = anh[vung_trang]
        # print("Giá trị phổ của vùng trắng: ", spectral_values)

        # Chuyển đổi spectral_values thành một con số ngưỡng (ví dụ: trung bình)
        threshold_value = np.mean(spectral_values)
        # print("Ngưỡng: ", threshold_value)

        # Tạo một ảnh có cùng kích thước với ảnh gốc để hiển thị vùng trắng
        vung_trang_image = np.zeros_like(anh)
        # ADD màu xanh lá cây phân biệt vùng trắng => Đảm bảo xác định đúng
        vung_trang_image[vung_trang] = (0, 255, 0)
        detect_and_draw_circles(vung_trang_image)
        cv2.imshow("Anh Goc", anh)
        cv2.imshow("Vung Trang", vung_trang_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
