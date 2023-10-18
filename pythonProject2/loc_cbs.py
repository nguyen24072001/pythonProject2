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
    nguong = gia_tri_toi_da * 0.98

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


def circle_detection(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detected_circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 150, param1=50, param2=30, minRadius=1, maxRadius=200)
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            img, point = calculator_color(img, gray, a, b, r)
            print("SUM", point)

    return img


def calculator_color(img, gray, a, b, r):
    points = []
    for r in range(r - 8, r - 3, 1):
        for x in range(a - r, a + r, 1):
            y = int(-(r ** 2 - (x - a) ** 2) ** 0.5 + b)
            points.append(gray[y, x])
            cv2.rectangle(img, (x, y), (x, y), (0, 0, 255), 2)

        for x in range(a - r, a + r, 1):
            y = int((r ** 2 - (x - a) ** 2) ** 0.5 + b)
            points.append(gray[y, x])
            cv2.rectangle(img, (x, y), (x, y), (0, 0, 255), 2)

    return img, int(sum(points)/len(points))

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


        # Tạo một ảnh có cùng kích thước với ảnh gốc để hiển thị vùng trắng
        vung_trang_image = np.zeros_like(anh)
        # ADD màu xanh lá cây phân biệt vùng trắng => Đảm bảo xác định đúng
        vung_trang_image[vung_trang] = (0, 255, 0)
        circle_detection(vung_trang_image)
        # Resize the image to a smaller size
        # resized_image = cv2.resize(anh, (640, 360))
        # Display the resized image
        # cv2.imshow("Anh Goc", resized_image)
        cv2.imshow("Anh Goc", anh)
        cv2.imshow("Vung Trang", vung_trang_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # cv2.waitKey(0)
    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()