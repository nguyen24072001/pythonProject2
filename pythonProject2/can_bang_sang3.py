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
    nguong = gia_tri_toi_da * 0.96655

    # Cắt ảnh theo phần có độ tương phản tương đối cao
    anh_cai_tien_tuong_phan = anh_can_bang_mau.copy()
    anh_cai_tien_tuong_phan[anh_can_bang_mau < nguong] = 0

    return anh_cai_tien_tuong_phan
def circle_detection(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detected_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 150, param1=50, param2=30, minRadius=30, maxRadius=40)
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            # cv2.circle(img, (a, b), r, (0, 0, 255), 2)
            img, point = calculator_color(img, gray, a, b, r)
            print("a =", a, "b = ", b, "point", point)

    return img


def calculator_color(img, gray, a, b, r):
    points = []
    for r in range(r - 3, r , 1):
        for x in range(a - r, a + r, 1):
            y = int(-(r ** 2 - (x - a) ** 2) ** 0.5 + b)
            points.append(gray[y, x])
            cv2.rectangle(img, (x, y), (x, y), (0, 0, 255), 1)

        for x in range(a - r, a + r, 1):
            y = int((r ** 2 - (x - a) ** 2) ** 0.5 + b)
            points.append(gray[y, x])
            cv2.rectangle(img, (x, y), (x, y), (0, 0, 255), 1)


    return img, int(sum(points)/len(points))

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

                if white_pixels < 1000:
                    print(f"Trạng thái LED {led_text}: OFF")
                    cv2.putText(image, "OFF", tuple(points[i]), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 165, 255), 2,
                                cv2.LINE_AA)
                elif white_pixels > 1000:
                    print(f"Trạng thái LED {led_text}: ON")
                    cv2.putText(image, "ON", tuple(points[i]), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 165, 255), 2,
                                cv2.LINE_AA)
                else:
                    print(f"Trạng thái LED {led_text}: Không xác định được")

                # cv2.imshow(f"Cropped LED {led_text}", cropped_img)

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


        anh_xam = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        anh2 = anh_xam
        # anh_cai_tien = anh_histogram(anh)

        # vung_trang = xac_dinh_vung_trang(anh_cai_tien)
        # print("Thông số vùng trắng: ", vung_trang)

        # Trích xuất giá trị phổ từ vùng trắng
        # spectral_values = anh[vung_trang]
        # print("Giá trị phổ của vùng trắng: ", spectral_values)

        # Chu
        # detect_and_draw_circles(vung_trang_image)
        anh_tron = circle_detection(frame)
        cv2.imshow("Anh Goc", anh_xam)
        cv2.imshow("Anh 2", anh_tron)
        # cv2.imshow("Vung Trang", vung_trang_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
