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
    anh = cv2.imread("Xanh_tron.jpg")
    anh_cai_tien = anh_histogram(anh)

    cv2.imshow("Anh Goc", anh)
    cv2.imshow("Anh Moi", anh_cai_tien)

    vung_trang = xac_dinh_vung_trang(anh_cai_tien)
    print("Thông số vùng trắng :", vung_trang)

    # Tạo một ảnh có cùng kích thước với ảnh gốc để hiển thị vùng trắng
    vung_trang_image = np.zeros_like(anh)
    vung_trang_image[vung_trang] = (0, 255, 0)  # Màu xanh lá cây cho vùng trắng

    cv2.imshow("Vung Trang", vung_trang_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()