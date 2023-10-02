import cv2
import numpy as np
import math
import time
import json
import paho.mqtt.client as mqtt
from paho.mqtt import publish

MQTT_SERVER = "localhost"
MQTT_PORT = 1883
message_id = 0
# MQTT topic => publish
MQTT_TOPIC = "ON_ON"
MQTT_TOPIC2 = "ON_OFF"
MQTT_TOPIC3 = "OFF"
MQTT_TOPIC4 = "SUM_BLINK"
MQTT_TOPIC5 = "get_status"
MQTT_TOPIC_CALL = "call_get_status"

start_time = time.time()
frame_count = 0
threshold_time_total = 0
threshold_count = 0
previous_threshold_value = None
total_threshold_diff = 0
previous_total_threshold_diff = 0
previous_total_threshold_diff_time = None
dem_duong = 0
dem_am = 0
blink = 0


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


def tinh_nguong(image):
    anh_cai_tien = anh_histogram(image)
    vung_trang = xac_dinh_vung_trang(anh_cai_tien)
    spectral_values = image[vung_trang]
    threshold_value = np.mean(spectral_values)
    return threshold_value


def calculate_percentage_loss(crop_img):
    nguong = tinh_nguong(crop_img)

    # Calculate loss_value and percentage_loss
    mat_mat = crop_img - nguong
    loss_value = mat_mat.sum()

    # Calculate percentage_loss
    percentage_loss = (loss_value / (crop_img.shape[0] * crop_img.shape[1])) * 100

    return percentage_loss


def led1(x, y, image, radius):
    x1 = x
    y1 = y
    led1_called = False
    output1 = ()  # Initialize an empty tuple
    loss5 = None
    if abs(x - x1) < 3 and abs(y - y1) < 3:
        led1_called = True
        output1 += (1,)  # Add the string to the tuple
        crop_img1 = image[int(y) - (radius + 2):int(y) + (radius + 2), int(x) - (radius + 2):int(x) + (radius + 2)]
        # LOSS
        percentage_loss = calculate_percentage_loss(crop_img1)

        # print("Loss 1: {:.2f}%".format(abs(percentage_loss) / 1000))
        loss5 = abs(percentage_loss) / 1000

        crop_img1 = cv2.putText(crop_img1, "1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        crop_img1 = cv2.putText(crop_img1, "{:.2f}".format(percentage_loss), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 165, 255), 2)

        if abs(percentage_loss) / 1000 - 40 > 5:
            publish.single(MQTT_TOPIC, payload=2, hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)
            output1 += (2,)  # Add the value 2 to the tuple
            crop_img1 = cv2.putText(crop_img1, "  ON", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        elif abs(percentage_loss) / 1000 - 30 < 15:
            publish.single(MQTT_TOPIC2, payload=1, hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)
            output1 += (1,)  # Add the value 1 to the tuple
            crop_img1 = cv2.putText(crop_img1, "  OFF", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

        # Detect color and add it to the tuple
        output1 += (crop_img1,)  # Add the modified image to the tuple

    return led1_called, output1, loss5


def led2_1(x, y, image, radius):
    led2_1_called = False
    output2_1 = ()  # Initialize an empty tuple

    if abs(x - 112) < 3 and abs(y - 75) < 3:
        led2_1_called = True

        output2_1 += (1,)  # Add the string to the tuple
        crop_img1 = image[int(y) - (radius + 2):int(y) + (radius + 2), int(x) - (radius + 2):int(x) + (radius + 2)]
        nguong = tinh_nguong(crop_img1)

        # Calculate loss_value and percentage_loss
        mat_mat = crop_img1 - nguong
        loss_value = mat_mat.sum()
        percentage_loss = (loss_value / (crop_img1.shape[0] * crop_img1.shape[1])) * 100
        # print("Loss 1: {:.2f}%".format(abs(percentage_loss) / 1000))

        crop_img1 = cv2.putText(crop_img1, "1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        crop_img1 = cv2.putText(crop_img1, "{:.2f}".format(percentage_loss), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 165, 255), 2)

        if abs(percentage_loss) / 1000 - 40 > 5:
            output2_1 += (2,)  # Add the value 2 to the tuple
            crop_img1 = cv2.putText(crop_img1, "  ON", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        elif abs(percentage_loss) / 1000 - 20 < 15:
            output2_1 += (1,)  # Add the value 1 to the tuple
            crop_img1 = cv2.putText(crop_img1, "  OFF", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

            # Detect color and add it to the tuple
        output2_1 += (crop_img1,)  # Add the modified image to the tuple
        # cv2.imshow("1", crop_img1)

    return led2_1_called, output2_1


def led2_2(x, y, image, radius):
    led2_2_called = False
    output2_2 = ()  # Initialize an empty tuple

    if abs(x - 247) < 3 and abs(y - 75) < 3:
        led2_2_called = True

        output2_2 += (2,)  # Add the string to the tuple
        crop_img1 = image[int(y) - (radius + 2):int(y) + (radius + 2), int(x) - (radius + 2):int(x) + (radius + 2)]
        nguong = tinh_nguong(crop_img1)

        # Calculate loss_value and percentage_loss
        mat_mat = crop_img1 - nguong
        loss_value = mat_mat.sum()
        percentage_loss = (loss_value / (crop_img1.shape[0] * crop_img1.shape[1])) * 100
        # print("Loss 2: {:.2f}%".format(abs(percentage_loss) / 1000))

        crop_img1 = cv2.putText(crop_img1, "2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        crop_img1 = cv2.putText(crop_img1, "{:.2f}".format(percentage_loss), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 165, 255), 2)

        if abs(percentage_loss) / 1000 - 40 > 5:
            output2_2 += (2,)  # Add the value 2 to the tuple
            crop_img1 = cv2.putText(crop_img1, "  ON", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        elif abs(percentage_loss) / 1000 - 20 < 15:
            output2_2 += (1,)  # Add the value 1 to the tuple
            crop_img1 = cv2.putText(crop_img1, "  OFF", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

            # Detect color and add it to the tuple
        output2_2 += (crop_img1,)  # Add the modified image to the tuple
        # cv2.imshow("1", crop_img1)

    return led2_2_called, output2_2


def led3_1(x, y, image, radius):
    led3_1_called = False
    output3_1 = ()  # Initialize an empty tuple

    if abs(x - 120) < 3 and abs(y - 239) < 3:
        led3_1_called = True

        output3_1 += (1,)  # Add the string to the tuple
        crop_img1 = image[int(y) - (radius + 2):int(y) + (radius + 2), int(x) - (radius + 2):int(x) + (radius + 2)]
        nguong = tinh_nguong(crop_img1)

        # Calculate loss_value and percentage_loss
        mat_mat = crop_img1 - nguong
        loss_value = mat_mat.sum()
        percentage_loss = (loss_value / (crop_img1.shape[0] * crop_img1.shape[1])) * 100
        # print("Loss 1: {:.2f}%".format(abs(percentage_loss) / 1000))

        crop_img1 = cv2.putText(crop_img1, "1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        crop_img1 = cv2.putText(crop_img1, "{:.2f}".format(percentage_loss), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 165, 255), 2)

        if abs(percentage_loss) / 1000 - 10 > 5:
            output3_1 += (2,)  # Add the value 2 to the tuple
            crop_img1 = cv2.putText(crop_img1, "  ON", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        elif abs(percentage_loss) / 1000 - 20 < 15:
            output3_1 += (1,)  # Add the value 1 to the tuple
            crop_img1 = cv2.putText(crop_img1, "  OFF", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

            # Detect color and add it to the tuple
        output3_1 += (crop_img1,)  # Add the modified image to the tuple
        # cv2.imshow("1", crop_img1)

    return led3_1_called, output3_1


def led3_2(x, y, image, radius):
    led3_2_called = False
    output3_2 = ()  # Initialize an empty tuple

    if abs(x - 321) < 3 and abs(y - 233) < 3:
        led3_2_called = True

        output3_2 += (2,)  # Add the string to the tuple
        crop_img1 = image[int(y) - (radius + 2):int(y) + (radius + 2), int(x) - (radius + 2):int(x) + (radius + 2)]
        nguong = tinh_nguong(crop_img1)

        # Calculate loss_value and percentage_loss
        mat_mat = crop_img1 - nguong
        loss_value = mat_mat.sum()
        percentage_loss = (loss_value / (crop_img1.shape[0] * crop_img1.shape[1])) * 100
        # print("Loss 2: {:.2f}%".format(abs(percentage_loss) / 1000))

        crop_img1 = cv2.putText(crop_img1, "2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        crop_img1 = cv2.putText(crop_img1, "{:.2f}".format(percentage_loss), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 165, 255), 2)

        if abs(percentage_loss) / 1000 - 10 > 5:
            output3_2 += (2,)  # Add the value 2 to the tuple
            crop_img1 = cv2.putText(crop_img1, "  ON", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        elif abs(percentage_loss) / 1000 - 20 < 15:
            output3_2 += (1,)  # Add the value 1 to the tuple
            crop_img1 = cv2.putText(crop_img1, "  OFF", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

            # Detect color and add it to the tuple
        output3_2 += (crop_img1,)  # Add the modified image to the tuple
        # cv2.imshow("1", crop_img1)

    return led3_2_called, output3_2


def led3_3(x, y, image, radius):
    led3_3_called = False
    output3_3 = ()  # Initialize an empty tuple

    if abs(x - 522) < 3 and abs(y - 228) < 3:
        led3_3_called = True

        output3_3 += (3,)  # Add the string to the tuple
        crop_img1 = image[int(y) - (radius + 2):int(y) + (radius + 2), int(x) - (radius + 2):int(x) + (radius + 2)]
        nguong = tinh_nguong(crop_img1)

        # Calculate loss_value and percentage_loss
        mat_mat = crop_img1 - nguong
        loss_value = mat_mat.sum()
        percentage_loss = (loss_value / (crop_img1.shape[0] * crop_img1.shape[1])) * 100
        # print("Loss 3: {:.2f}%".format(abs(percentage_loss) / 1000))

        crop_img1 = cv2.putText(crop_img1, "3", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        crop_img1 = cv2.putText(crop_img1, "{:.2f}".format(percentage_loss), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 165, 255), 2)

        if abs(percentage_loss) / 1000 - 10 > 5:
            output3_3 += (2,)  # Add the value 2 to the tuple
            crop_img1 = cv2.putText(crop_img1, "  ON", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        elif abs(percentage_loss) / 1000 - 20 < 15:
            output3_3 += (1,)  # Add the value 1 to the tuple
            crop_img1 = cv2.putText(crop_img1, "  OFF", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

            # Detect color and add it to the tuple
        output3_3 += (crop_img1,)  # Add the modified image to the tuple
        # cv2.imshow("1", crop_img1)

    return led3_3_called, output3_3


def led4_1(x, y, image, radius):
    led4_1_called = False
    output = ()  # Initialize an empty tuple

    if abs(x - 188) < 3 and abs(y - 131) < 3:
        led4_1_called = True

        output += (1,)  # Add the string to the tuple
        crop_img1 = image[int(y) - (radius + 2):int(y) + (radius + 2), int(x) - (radius + 2):int(x) + (radius + 2)]
        nguong = tinh_nguong(crop_img1)

        # Calculate loss_value and percentage_loss
        mat_mat = crop_img1 - nguong
        loss_value = mat_mat.sum()
        percentage_loss = (loss_value / (crop_img1.shape[0] * crop_img1.shape[1])) * 100

        crop_img1 = cv2.putText(crop_img1, "1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        crop_img1 = cv2.putText(crop_img1, "{:.2f}".format(percentage_loss), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                                (0, 165, 255), 2)

        if abs(percentage_loss) / 1000 - 20 < 10:
            output += (2,)  # Add the value 2 to the tuple
            crop_img1 = cv2.putText(crop_img1, "  ON", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        elif abs(percentage_loss) / 1000 - 30 > 5:
            output += (1,)  # Add the value 1 to the tuple
            crop_img1 = cv2.putText(crop_img1, "  OFF", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

            # Detect color and add it to the tuple
        output += (crop_img1,)  # Add the modified image to the tuple
        # cv2.imshow("1", crop_img1)

    return led4_1_called, output


def led4_2(x, y, image, radius):
    led4_2_called = False  # Thêm biến cờ để theo dõi hàm led3() đã được gọi hay chưa
    output2 = ()  # Initialize an empty tuple
    if abs(x - 457) < 3 and abs(y - 133) < 3:
        led4_2_called = True
        output2 += (2,)  # Add the string to the tuple
        crop_img2 = image[int(y) - (radius + 2):int(y) + (radius + 2), int(x) - (radius + 2):int(x) + (radius +
                                                                                                       2)]
        nguong = tinh_nguong(crop_img2)

        # cv2.imshow("Crop Image 2", crop_img2)

        # print("Ngưỡng 2: ", nguong)
        mat_mat = crop_img2 - nguong
        loss_value = mat_mat.sum()  # Tính tổng giá trị mất mát
        percentage_loss = (loss_value / (crop_img2.shape[0] * crop_img2.shape[1])) * 100
        # print("Loss 2: {:.2f}%".format(abs(percentage_loss) / 1000))
        cv2.putText(crop_img2, "2", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        cv2.putText(crop_img2, "{:.2f}".format(percentage_loss), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 165, 255), 2)

        # cv2.imshow("LOSS", mat_mat)
        if abs(percentage_loss) / 1000 - 20 < 10:
            output2 += (2,)  # Add the value 2 to the tuple
            cv2.putText(crop_img2, "  ON", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

        elif abs(percentage_loss) / 1000 - 30 > 5:
            output2 += (1,)  # Add the value 2 to the tuple
            cv2.putText(crop_img2, "  OFF", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

        output2 += (crop_img2,)  # Add the modified image to the tuple

    return led4_2_called, output2


def led4_3(x, y, image, radius):
    led4_3_called = False  # Thêm biến cờ để theo dõi hàm led3() đã được gọi hay chưa
    output3 = ()  # Initialize an empty tuple

    if abs(x - 184) < 3 and abs(y - 334) < 3:
        led4_3_called = True  # Đánh dấu rằng hàm led3() đã được gọi

        output3 += (3,)  # Add the string to the tuple
        crop_img3 = image[int(y) - (radius + 2):int(y) + (radius + 2), int(x) - (radius + 2):int(x) + (radius + 2)]
        nguong = tinh_nguong(crop_img3)
        # print("Ngưỡng 3: ", nguong)

        mat_mat = crop_img3 - nguong
        loss_value = mat_mat.sum()
        percentage_loss = (loss_value / (crop_img3.shape[0] * crop_img3.shape[1])) * 100
        # print("Loss 3: {:.2f}%".format(abs(percentage_loss) / 1000))
        cv2.putText(crop_img3, "3", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        cv2.putText(crop_img3, "{:.2f}".format(percentage_loss), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255),
                    2)

        if abs(percentage_loss) / 1000 - 25 < 2:
            output3 += (2,)  # Add the value 2 to the tuple
            cv2.putText(crop_img3, "  ON", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        elif abs(percentage_loss) / 1000 - 25 > 2:
            output3 += (1,)  # Add the value 1 to the tuple
            cv2.putText(crop_img3, "  OFF", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

        output3 += (crop_img3,)  # Add the modified image to the tuple

    return led4_3_called, output3


def led4_4(x, y, image, radius):
    led4_4_called = False  # Thêm biến cờ để theo dõi hàm led3() đã được gọi hay chưa
    output4 = ()  # Initialize an empty tuple
    if abs(x - 456) < 3 and abs(y - 338) < 3:
        led4_4_called = True
        output4 += (4,)  # Add the string to the tuple
        crop_img4 = image[int(y) - (radius + 2):int(y) + (radius + 2), int(x) - (radius + 2):int(x) + (radius + 2)]
        # cv2.imshow("Crop Image 4", crop_img4)
        nguong = tinh_nguong(crop_img4)
        # print("Ngưỡng 4:", nguong)

        mat_mat = crop_img4 - nguong
        loss_value = mat_mat.sum()  # Tính tổng giá trị mất mát
        percentage_loss = (loss_value / (crop_img4.shape[0] * crop_img4.shape[1])) * 100
        # print("Loss 4: {:.2f}%".format(abs(percentage_loss) / 1000))

        # cv2.imshow("LOSS", mat_mat)
        cv2.putText(crop_img4, "4", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)
        cv2.putText(crop_img4, "{:.2f}".format(percentage_loss), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (0, 165, 255), 2)

        # cv2.imshow("LOSS", mat_mat)
        if abs(percentage_loss) / 1000 - 20 < 10:
            output4 += (2,)  # Add the value 2 to the tuple
            cv2.putText(crop_img4, "   ON", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

        elif abs(percentage_loss) / 1000 - 30 > 5:
            output4 += (1,)  # Add the value 2 to the tuple
            cv2.putText(crop_img4, "   OFF", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2)

        output4 += (crop_img4,)  # Add the modified image to the tuple

    return led4_4_called, output4


active_on = ""
active_off = ""
shut_down = ""

latest_status = ""


def on_connect(client, userdata, flags, rc):
    print('Đã kết nối với mã kết quả: ' + str(rc))
    client.subscribe(MQTT_TOPIC5)
    client.subscribe(MQTT_TOPIC_CALL)


def sw01_get_status(image):
    global active_on
    global active_off
    global shut_down

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    dem_led = 0
    check_led_on = 0

    led_results = [f"{1}"]
    ketqua = None
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
        else:
            shape_name = "Hinh Tron"
            dem_led = dem_led + 1

        x, y = approx[0][0]
        # cv2.putText(image, shape_name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if shape_name == "Hinh Tron":
            (x, y), radius = cv2.minEnclosingCircle(approx)
            center = (int(x), int(y))
            radius = int(radius)

            # Tô đỏ hình tròn
            # cv2.circle(image, center, radius, (0, 0, 255), 2)

            # Hiển thị tọa độ
            # cv2.putText(image, f"Toa Do: ({x:.2f}, {y:.2f})", (int(x), int(y) + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
            #             (0, 0, 255), 2)
            print(f"Toa Do: ({x:.2f}, {y:.2f})")

            led1_called, output1, loss5 = led1(x, y, image, radius)
            print(loss5)

            if led1_called:

                check_led_on += 1
                status = output1[0]  # "Công tắc 1"

                # payload 1
                value = output1[1]  # 1 or 2

                if value == 2:
                    ketqua = 2
                    print("ok on")
                elif value == 1:
                    ketqua = 1
                    print("ok off")
                led_results.append(f"{int(status)}:{int(value)}")

    if check_led_on == 0:
        # payload 1
        led_results.append(f"{1}:{0}")
        ketqua = 0
        print("off all")
        publish.single(MQTT_TOPIC3, payload=0, hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)

    # print("Số lượng:", dem_led)
    led_results.append(f"{int(dem_led)}")

    print(" ".join(led_results))
    print("final", ketqua)
    if ketqua == 2:
        active_on = "OK"
    else:
        active_on = "NONE"
    if ketqua == 1:
        active_off = "OK"
    else:
        active_off = "NONE"
    if ketqua == 0:
        shut_down = "OK"
    else:
        shut_down = "NONE"

    text_sum = json.dumps({
        "LED_ON": active_on,
        "LED_OFF": active_off,
        "OFF": shut_down
    })
    publish.single(MQTT_TOPIC5, payload=text_sum, hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)
    return text_sum



client = mqtt.Client()
client.on_connect = on_connect

client.connect('localhost', 1883, 60)

# Start the MQTT client loop
client.loop_start()


def sw02_get_status(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    dem_led = 0
    check_led_on1 = 0
    check_led_on2 = 0

    led_results = [f"{2}"]

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        sides = len(approx)
        cv2.drawContours(image, [approx], 0, (0, 255, 0), 2)

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
        else:
            shape_name = "Hinh Tron"
            dem_led = dem_led + 1

        x, y = approx[0][0]
        cv2.putText(image, shape_name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if shape_name == "Hinh Tron":
            (x, y), radius = cv2.minEnclosingCircle(approx)
            center = (int(x), int(y))
            radius = int(radius)

            # Tô đỏ hình tròn
            cv2.circle(image, center, radius, (0, 0, 255), 2)

            # Hiển thị tọa độ
            cv2.putText(image, f"Toa Do: ({x:.2f}, {y:.2f})", (int(x), int(y) + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), 2)
            # print(f"Toa Do: ({x}, {y})")

            led2_1_called, output2_1 = led2_1(x, y, image, radius)
            led2_2_called, output2_2 = led2_2(x, y, image, radius)

            if led2_1_called:
                check_led_on1 += 1
                status = output2_1[0]  # "Công tắc 1"
                value = output2_1[1]  # 1 or 2
                led_results.append(f"{int(status)}:{int(value)}")
            if led2_2_called:
                check_led_on2 += 1
                status = output2_2[0]  # "Công tắc 1"
                value = output2_2[1]  # 1 or 2
                led_results.append(f"{int(status)}:{int(value)}")

    if check_led_on1 == 0:
        led_results.append(f"{1}:{0}")
    if check_led_on2 == 0:
        led_results.append(f"{2}:{0}")

    # print("Số lượng:", dem_led)
    led_results.append(f"{int(dem_led)}")
    print(" ".join(led_results))


def sw03_get_status(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    dem_led = 0
    check_led_on1 = 0
    check_led_on2 = 0
    check_led_on3 = 0

    led_results = [f"{3}"]

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        sides = len(approx)
        cv2.drawContours(image, [approx], 0, (0, 255, 0), 2)

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
        else:
            shape_name = "Hinh Tron"
            dem_led = dem_led + 1

        x, y = approx[0][0]
        cv2.putText(image, shape_name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if shape_name == "Hinh Tron":
            (x, y), radius = cv2.minEnclosingCircle(approx)
            center = (int(x), int(y))
            radius = int(radius)

            # Tô đỏ hình tròn
            cv2.circle(image, center, radius, (0, 0, 255), 2)

            # Hiển thị tọa độ
            cv2.putText(image, f"Toa Do: ({x:.2f}, {y:.2f})", (int(x), int(y) + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), 2)
            # print(f"Toa Do: ({x}, {y})")

            led3_1_called, output3_1 = led3_1(x, y, image, radius)
            led3_2_called, output3_2 = led3_2(x, y, image, radius)
            led3_3_called, output3_3 = led3_3(x, y, image, radius)

            if led3_1_called:
                check_led_on1 += 1
                status = output3_1[0]  # "Công tắc 1"
                value = output3_1[1]  # 1 or 2
                led_results.append(f"{int(status)}:{int(value)}")
            if led3_2_called:
                check_led_on2 += 1
                status = output3_2[0]  # "Công tắc 1"
                value = output3_2[1]  # 1 or 2
                led_results.append(f"{int(status)}:{int(value)}")
            if led3_3_called:
                check_led_on3 += 1
                status = output3_3[0]  # "Công tắc 1"
                value = output3_3[1]  # 1 or 2
                led_results.append(f"{int(status)}:{int(value)}")

    if check_led_on1 == 0:
        led_results.append(f"{1}:{0}")
    if check_led_on2 == 0:
        led_results.append(f"{2}:{0}")
    if check_led_on3 == 0:
        led_results.append(f"{3}:{0}")

    # print("Số lượng:", dem_led)
    led_results.append(f"{int(dem_led)}")
    print(" ".join(led_results))


def sw04_get_status(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    dem_led = 0
    check_led_on4_1 = 0
    check_led_on4_2 = 0
    check_led_on4_3 = 0
    check_led_on4_4 = 0

    led_results = [f"{4}"]

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
        sides = len(approx)
        cv2.drawContours(image, [approx], 0, (0, 255, 0), 2)

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
        else:
            shape_name = "Hinh Tron"
            dem_led = dem_led + 1

        x, y = approx[0][0]
        cv2.putText(image, shape_name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        if shape_name == "Hinh Tron":
            (x, y), radius = cv2.minEnclosingCircle(approx)
            center = (int(x), int(y))
            radius = int(radius)

            # Tô đỏ hình tròn
            cv2.circle(image, center, radius, (0, 0, 255), 2)

            # Hiển thị tọa độ
            cv2.putText(image, f"Toa Do: ({x:.2f}, {y:.2f})", (int(x), int(y) + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 0, 255), 2)
            print(f"Toa Do: ({x}, {y})")

            led4_1_called, output = led4_1(x, y, image, radius)
            led4_2_called, output2 = led4_2(x, y, image, radius)
            led4_3_called, output3 = led4_3(x, y, image, radius)
            led4_4_called, output4 = led4_4(x, y, image, radius)

            if led4_1_called:
                check_led_on4_1 += 1
                status = output[0]  # "Công tắc 1"
                value = output[1]  # 1 or 2
                led_results.append(f"{int(status)}:{int(value)}")

            if led4_2_called:
                check_led_on4_2 += 1
                status = output2[0]
                value = output2[1]  # 1 or 2
                led_results.append(f"{int(status)}:{int(value)}")

            if led4_3_called:
                check_led_on4_3 += 1
                status = output3[0]
                value = output3[1]  # 1 or 2
                led_results.append(f"{int(status)}:{int(value)}")

            if led4_4_called:
                check_led_on4_4 += 1
                status = output4[0]
                value = output4[1]  # 1 or 2
                led_results.append(f"{int(status)}:{int(value)}")

    if check_led_on4_1 == 0:
        led_results.append(f"{1}:{0}")
    if check_led_on4_2 == 0:
        led_results.append(f"{2}:{0}")
    if check_led_on4_3 == 0:
        led_results.append(f"{3}:{0}")
    if check_led_on4_4 == 0:
        led_results.append(f"{4}:{0}")

    # print("Số lượng:", dem_led)
    led_results.append(f"{int(dem_led)}")
    print(" ".join(led_results))


sum_blink = ""


def blink_led1(anh):
    global threshold_time_total, sum_blink
    global threshold_count
    global previous_threshold_value
    global dem_duong
    global dem_am
    global total_threshold_diff
    global previous_total_threshold_diff
    global previous_total_threshold_diff_time
    global blink
    global frame_count
    percentage_loss = abs(calculate_percentage_loss(anh)) / 1000
    # Tính giá trị ngưỡng
    start_threshold_time = time.time()
    end_threshold_time = time.time()
    threshold_time_ms = (end_threshold_time - start_threshold_time) * 1000
    # print("Loss 1: {}".format(abs(percentage_loss) / 1000))
    # print("Thời gian tính ngưỡng (ms): ", threshold_time_ms)
    print("loss test", percentage_loss * 2)
    threshold_time_total += threshold_time_ms

    if percentage_loss > 45:
        threshold_count += 1

    # Tính tổng số lần mà giá trị ngưỡng hiện tại trừ giá trị ngưỡng trước đó lớn hơn 50
    if previous_threshold_value is not None:
        threshold_diff = percentage_loss - previous_threshold_value
        if abs(threshold_diff) <= 7:
            print("+")
            dem_duong = dem_duong + 1
            total_threshold_diff += 1
            if total_threshold_diff - previous_total_threshold_diff == 1:
                if previous_total_threshold_diff_time is not None:
                    current_time = time.time()
                    time_diff = (current_time - previous_total_threshold_diff_time)
                    print("Khoảng thời gian (s) nháy {} lần và {} lần:".format(total_threshold_diff - 1,
                                                                               total_threshold_diff), time_diff)

                previous_total_threshold_diff_time = time.time()
        else:
            print("-")
            dem_am = dem_am + 1
    previous_threshold_value = percentage_loss
    previous_total_threshold_diff = total_threshold_diff
    print("LED Đã Nháy {} Lần !".format(total_threshold_diff))
    print("dem duong", dem_duong)
    cv2.putText(
        anh,
        f"                TIME OUT:{dem_duong / 23:.2f}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )
    if dem_duong > 200:
        print("dem am", dem_am)

        if dem_am != 0:
            blink = blink + 1
            sum_blink = math.ceil((dem_am - 2) / 2)
            publish.single(MQTT_TOPIC4, payload=sum_blink, hostname=MQTT_SERVER, port=MQTT_PORT, qos=1)
        dem_duong = 0
        dem_am = 0
        # blink = 0
    # dem_am 8 => 10
    # Tính FPS và hiển thị lên frame
    frame_count += 1
    elapsed_time = time.time() - start_time
    fps = frame_count / elapsed_time
    cv2.putText(
        anh,
        f"FPS: {fps:.2f}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    current_frame_time = time.time()
    time_diff = current_frame_time - start_time
    print("time = {:.2f}".format(time_diff))
    cv2.putText(
        anh,
        f"Time: {time_diff:.2f}s",
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )
    if sum_blink == 0:
        blink_total = "NONE"
    else:
        blink_total = sum_blink

    blink_sum = json.dumps({
        "TOTAL": blink_total
    })
    return blink_sum
