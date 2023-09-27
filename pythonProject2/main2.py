import cv2
import numpy as np


def anh_histogram(image):
    anh_xam = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    anh_can_bang = cv2.equalizeHist(anh_xam)
    anh_can_bang_mau = cv2.cvtColor(anh_can_bang, cv2.COLOR_GRAY2BGR)
    gia_tri_toi_thieu, gia_tri_toi_da, _, _ = cv2.minMaxLoc(anh_can_bang)
    nguong = gia_tri_toi_da * 0.95
    anh_cai_tien_tuong_phan = anh_can_bang_mau.copy()
    anh_cai_tien_tuong_phan[anh_can_bang_mau < nguong] = 0
    return anh_cai_tien_tuong_phan


def xac_dinh_vung_trang(anh):
    anh_xam = cv2.cvtColor(anh, cv2.COLOR_BGR2GRAY)
    _, anh_nhi_phan = cv2.threshold(anh_xam, 0, 255, cv2.THRESH_BINARY)
    vung_trang = np.where(anh_nhi_phan == 255)
    return vung_trang


def main():
    cap = cv2.VideoCapture(2)

    while True:
        # Đọc khung hình từ luồng ảnh
        ret, image = cap.read()
        if not ret:
            break

        # image = cv2.imread("4_led_on.jpg")

        anh_cai_tien = anh_histogram(image)

        vung_trang = xac_dinh_vung_trang(anh_cai_tien)
        print("Thông số vùng trắng: ", vung_trang)

        spectral_values = image[vung_trang]
        print("Giá trị phổ của vùng trắng: ", spectral_values)

        threshold_value = np.mean(spectral_values)
        print("Ngưỡng: ", threshold_value)

        if abs(threshold_value - 228.16) < 0.1:
            print("Đèn sáng")

        if abs(threshold_value - 177.78) < 0.1:
            print("Đèn tắt")

        vung_trang_image = np.zeros_like(image)
        vung_trang_image[vung_trang] = (0, 255, 0)

        # cv2.imshow("Vung Trang", vung_trang_image)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        dem_led = 0
        for contour in contours:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
            sides = len(approx)
            # cv2.drawContours(image, [approx], 0, (0, 255, 0), 2)

            if sides == 3:
                shape_name = "Tam Giac"
            elif sides == 4:
                x, y, w, h = cv2.boundingRect(approx)
                aspect_ratio = float(w) / h
                if 0.95 <= aspect_ratio <= 1.05:
                    shape_name = "Hinh Vuong"
                else:
                    shape_name = "Hinh Chu Nhat"
            elif sides == 5:
                shape_name = "Ngu Giac"
            elif sides == 6:
                shape_name = "Luc Giac"
            else:
                shape_name = "hinh tron"
                dem_led = dem_led + 1

            # x, y = approx[0][0]
            # cv2.putText(image, shape_name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if shape_name == "hinh tron":
                (x, y), radius = cv2.minEnclosingCircle(approx)
                # center = (int(x), int(y))
                radius = int(radius)

                # Tô đỏ hình tròn
                # cv2.circle(image, center, radius, (0, 0, 255), 2)

                # Hiển thị tọa độ
                # cv2.putText(image, f"Toa Do: ({x:.2f}, {y:.2f})", (int(x), int(y) + 30), cv2.FONT_HERSHEY_SIMPLEX,
                # 0.5, (0, 0, 255),2)
                print(f"Toa Do: ({x:.2f}, {y:.2f})")

                if 503 <= x <= 507 and 316 <= y <= 320:
                    print("Công tắc 1")
                    crop_img1 = image[int(y) - (radius + 2):int(y) + (radius + 2), int(x) - (radius + 2):int(x) +
                                                                                                         (radius + 2)]
                    # cv2.imshow("LED 1", crop_img1)
                    cv2.putText(crop_img1, "LED1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
                    cv2.putText(crop_img1, "{:.2f}".format(threshold_value), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 165, 255), 2)

                    anh_cai_tien = anh_histogram(crop_img1)
                    vung_trang = xac_dinh_vung_trang(anh_cai_tien)
                    spectral_values = crop_img1[vung_trang]
                    threshold_value = np.mean(spectral_values)
                    print("Ngưỡng 1: ", threshold_value)
                    if abs(threshold_value - 243.23) < 0.2:
                        print("Led 1 On")
                        cv2.putText(crop_img1, "      ON", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

                    elif abs(threshold_value - 243.36) < 0.1:
                        print("Led 1 Off")
                        cv2.putText(crop_img1, "      OFF", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
                    else:
                        print("1 No Power")
                elif 176 <= x <= 180 and 354 <= y <= 358:
                    print("Công tắc 2")
                    crop_img2 = image[int(y) - (radius + 2):int(y) + (radius + 2), int(x) - (radius + 2):int(x) +
                                                                                                         (radius + 2)]
                    # cv2.imshow("LED 2", crop_img2)
                    cv2.putText(crop_img2, "LED2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
                    cv2.putText(crop_img2, "{:.2f}".format(threshold_value), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 165, 255), 2)

                    anh_cai_tien = anh_histogram(crop_img2)
                    vung_trang = xac_dinh_vung_trang(anh_cai_tien)
                    spectral_values = crop_img2[vung_trang]
                    threshold_value = np.mean(spectral_values)
                    print("Ngưỡng 2: ", threshold_value)
                    if abs(threshold_value - 243.13) > 0.01:
                        print("Led 2 On")
                        cv2.putText(crop_img2, "      ON", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

                    elif abs(threshold_value - 243.08) == 0:
                        print("Led 2 Off")
                        cv2.putText(crop_img2, "      OFF", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

                    else:
                        print("2 No Power")
                elif 475 <= x <= 479 and 119 <= y <= 123:
                    print("Công tắc 3")
                    crop_img3 = image[int(y) - (radius + 2):int(y) + (radius + 2), int(x) - (radius + 2):int(x) +
                                                                                                         (radius + 2)]
                    # cv2.imshow("LED 3", crop_img3)
                    cv2.putText(crop_img3, "LED3", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
                    cv2.putText(crop_img3, "{:.2f}".format(threshold_value), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 165, 255), 2)

                    anh_cai_tien = anh_histogram(crop_img3)
                    vung_trang = xac_dinh_vung_trang(anh_cai_tien)
                    spectral_values = crop_img3[vung_trang]
                    threshold_value = np.mean(spectral_values)
                    print("Ngưỡng 3: ", threshold_value)
                    if abs(threshold_value - 243.03) < 0.2:
                        print("Led 3 On")
                        cv2.putText(crop_img3, "      ON", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

                    elif abs(threshold_value - 243.34) < 0.1:
                        print("Led 3 Off")
                        cv2.putText(crop_img3, "      OFF", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

                    else:
                        print("3 No Power")
                elif 171 <= x <= 175 and 124 <= y <= 128:
                    print("Công tắc 4")
                    crop_img4 = image[int(y) - (radius + 2):int(y) + (radius + 2), int(x) - (radius + 2):int(x) +
                                                                                                         (radius + 2)]
                    # cv2.imshow("LED 4", crop_img4)
                    cv2.putText(crop_img4, "LED4", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
                    cv2.putText(crop_img4, "{:.2f}".format(threshold_value), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 165, 255), 2)

                    anh_cai_tien = anh_histogram(crop_img4)
                    vung_trang = xac_dinh_vung_trang(anh_cai_tien)
                    spectral_values = crop_img4[vung_trang]
                    threshold_value = np.mean(spectral_values)
                    print("Ngưỡng 4: ", threshold_value)
                    if abs(threshold_value - 243.08) < 0.2:
                        print("Led 4 On")
                        cv2.putText(crop_img4, "      ON", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

                    elif abs(threshold_value - 243.27) < 0.1:
                        print("Led 4 Off")
                        cv2.putText(crop_img4, "     :OFF", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

                    else:
                        print("4 No Power")

        print("Số lượng : ", dem_led)
        cv2.putText(image, "TYPE:4 LED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        cv2.imshow("Camera", image)
        # Thoát khỏi vòng lặp nếu nhấn phím 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        # Giải phóng bộ nhớ và đóng luồng ảnh
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
