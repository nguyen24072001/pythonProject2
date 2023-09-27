import cv2
import numpy as np


def anh_histogram(image):
    anh_xam = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    anh_can_bang = cv2.equalizeHist(anh_xam)
    anh_can_bang_mau = cv2.cvtColor(anh_can_bang, cv2.COLOR_GRAY2BGR)
    gia_tri_toi_thieu, gia_tri_toi_da, _, _ = cv2.minMaxLoc(anh_can_bang)

    # change !
    nguong = gia_tri_toi_da * 0
    anh_cai_tien_tuong_phan = anh_can_bang_mau.copy()
    anh_cai_tien_tuong_phan[anh_can_bang_mau < nguong] = 0
    return anh_cai_tien_tuong_phan


def xac_dinh_vung_trang(anh):
    anh_xam = cv2.cvtColor(anh, cv2.COLOR_BGR2GRAY)
    _, anh_nhi_phan = cv2.threshold(anh_xam, 0, 255, cv2.THRESH_BINARY)
    vung_trang = np.where(anh_nhi_phan == 255)
    return vung_trang


def trich_xuat_hex_color(anh, vung_trang):
    anh_rgb = cv2.cvtColor(anh, cv2.COLOR_BGR2RGB)
    gia_tri_mau = anh_rgb[vung_trang]

    hex_colors = []
    for pixel in gia_tri_mau:
        hex_color = '#{:02x}{:02x}{:02x}'.format(pixel[0], pixel[1], pixel[2])
        hex_colors.append(hex_color)

    return hex_colors


def chuyen_doi_gia_tri_trung_binh(hex_colors):
    if len(hex_colors) == 0:
        return None

    red_values = []
    green_values = []
    blue_values = []

    for hex_color in hex_colors:
        red = int(hex_color[1:3], 16)
        green = int(hex_color[3:5], 16)
        blue = int(hex_color[5:7], 16)

        red_values.append(red)
        green_values.append(green)
        blue_values.append(blue)

    red_avg = int(np.mean(red_values))
    green_avg = int(np.mean(green_values))
    blue_avg = int(np.mean(blue_values))

    avg_hex_color = '#{:02x}{:02x}{:02x}'.format(red_avg, green_avg, blue_avg)
    return avg_hex_color


def main():
    anh = cv2.imread("color_led1_on.jpg")

    anh_cai_tien = anh_histogram(anh)

    cv2.imshow("Anh Goc", anh)

    vung_trang = xac_dinh_vung_trang(anh_cai_tien)

    hex_colors = trich_xuat_hex_color(anh, vung_trang)

    avg_hex_color = chuyen_doi_gia_tri_trung_binh(hex_colors)
    print("Giá trị trung bình hex color của vùng trắng: ", avg_hex_color)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
