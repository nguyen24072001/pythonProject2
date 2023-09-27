# import argparse
import cv2
import numpy as np


def anh_histogram(image):
    # Chuyển đổi ảnh sang ảnh grayscale
    anh_xam = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Cân bằng histogram tự động => Phân bổ mức xám
    anh_can_bang = cv2.equalizeHist(anh_xam)

    # Chuyển đổi ảnh xám thành ảnh màu
    anh_can_bang_mau = cv2.cvtColor(anh_can_bang, cv2.COLOR_GRAY2BGR)

    # Tìm giá trị Max và Min trong ảnh cân bằng
    gia_tri_toi_thieu, gia_tri_toi_da, _, _ = cv2.minMaxLoc(anh_can_bang)

    # Đặt ngưỡng để lọc các pixel có độ tương phản cao hơn ngưỡng
    nguong = gia_tri_toi_da * 0.95

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


def main():
    cap = cv2.VideoCapture(2)

    while True:
        # Đọc khung hình từ luồng ảnh
        ret, frame = cap.read()
        if not ret:
            break

        anh_cai_tien = anh_histogram(frame)

        vung_trang = xac_dinh_vung_trang(anh_cai_tien)
        print("Thông số vùng trắng: ", vung_trang)

        # Trích xuất giá trị phổ từ vùng trắng
        gia_tri_pho = frame[vung_trang]
        print("Giá trị phổ của vùng trắng: ", gia_tri_pho)

        # Chuyển đổi giá trị phổ thành giá trị ngưỡng
        threshold_value = np.mean(gia_tri_pho)
        print("Ngưỡng: ", threshold_value)

        # Hiển thị giá trị lên frame
        text = f"          {threshold_value:.2f}"
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Đèn sáng nếu ngưỡng ảnh LED_ON nằm trong khoảng x đơn vị
        if abs(threshold_value - 243) < 3:
            cv2.putText(frame, "LED ON !", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Đèn tắt nếu ngưỡng ảnh LED_OFF nằm trong khoảng x đơn vị
        if abs(threshold_value - 162) < 3:
            cv2.putText(frame, "LED OFF !", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # Tạo một ảnh có cùng kích thước với khung hình gốc để hiển thị vùng trắng
        vung_trang_image = np.zeros_like(frame)
        # ADD màu xanh lá cây phân biệt vùng trắng => Đảm bảo xác định đúng
        vung_trang_image[vung_trang] = (0, 255, 0)

        # Tính toán tọa độ khung vuông
        square_center_x = frame.shape[1] // 2
        square_center_y = frame.shape[0] // 2
        square_size = int(frame.shape[0] * 0.8)  # Kích thước vuông x% chiều cao của frame

        # Tính toán các tọa độ góc của khung vuông
        top_left_x = square_center_x - square_size // 2
        top_left_y = square_center_y - square_size // 2
        bottom_right_x = square_center_x + square_size // 2
        bottom_right_y = square_center_y + square_size // 2

        # Vẽ khung vuông
        cv2.rectangle(frame, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (0, 165, 255), 2)

        # Hiển thị khung hình gốc
        cv2.imshow("Camera", frame)

        # Hiển thị ảnh vùng trắng
        cv2.imshow("Vung Trang", vung_trang_image)

        # Thoát khỏi vòng lặp nếu nhấn phím 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Giải phóng bộ nhớ và đóng luồng ảnh
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
