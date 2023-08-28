import argparse
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

#   parser = argparse.ArgumentParser(description='Đọc hình ảnh từ đường dẫn.')
#    parser.add_argument('image_path', type=str, help='Đường dẫn tệp hình ảnh')
#    args = parser.parse_args()

    # Đọc hình ảnh từ đường dẫn được cung cấp
    # anh = cv2.imread(args.image_path)
    anh = cv2.imread("LED_ON.jpg")

#    if anh is None:
#        print('None')
#    else:
#        print('OK !')

    anh_cai_tien = anh_histogram(anh)

    # cv2.imshow("Anh Goc", anh)
    # cv2.imshow("Anh Moi", anh_cai_tien)

    vung_trang = xac_dinh_vung_trang(anh_cai_tien)
    print("Thông số vùng trắng: ", vung_trang)

    # Trích xuất giá trị phổ từ vùng trắng
    spectral_values = anh[vung_trang]
    print("Giá trị phổ của vùng trắng: ", spectral_values)

    # Chuyển đổi spectral_values thành một con số ngưỡng (ví dụ: trung bình)
    threshold_value = np.mean(spectral_values)
    print("Ngưỡng: ", threshold_value)

    # Đèn sáng nếu ngưỡng ảnh LED_ON nằm trong khoảng 0.1 đơn vị
    if abs(threshold_value - 228.16) < 0.1:
        print("Đèn sáng")

    # Đèn tắt nếu ngưỡng ảnh LED_OFF nằm trong khoảng 0.1 đơn vị
    if abs(threshold_value - 177.78) < 0.1:
        print("Đèn tắt")

    # Tạo một ảnh có cùng kích thước với ảnh gốc để hiển thị vùng trắng
    vung_trang_image = np.zeros_like(anh)
    # ADD màu xanh lá cây phân biệt vùng trắng => Đảm bảo xác định đúng
    vung_trang_image[vung_trang] = (0, 255, 0)

    # cv2.imshow("Vung Trang", vung_trang_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()