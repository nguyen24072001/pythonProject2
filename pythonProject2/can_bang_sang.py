import cv2


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


def main():
    anh = cv2.imread("Xanh_tron.jpg")

    anh_cai_tien = anh_histogram(anh)

    cv2.imshow("Anh Goc", anh)
    cv2.imshow("Anh Moi", anh_cai_tien)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()