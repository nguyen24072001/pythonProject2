import cv2

# Đọc ảnh đầu vào
image = cv2.imread("LED_ON.jpg")

# Chuyển đổi ảnh thành ảnh grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Áp dụng Gaussian blur để loại bỏ nhiễu
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Phát hiện các cạnh bằng Canny edge detection
edges = cv2.Canny(blurred, 50, 150)

# Tìm các đường biên trong ảnh bằng contour detection
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Đếm số lượng công tắc
dem_led = 0

# Duyệt qua từng contour và xác định hình dạng
for contour in contours:
    # Xác định độ phức tạp của contour
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)

    # Xác định số đỉnh của hình dạng
    sides = len(approx)

    # Vẽ hình bao quanh contour
    cv2.drawContours(image, [approx], 0, (0, 255, 0), 2)

    # Xác định tên hình dạng dựa trên số đỉnh
    shape_name = ""
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

    # Hiển thị tên hình dạng bên cạnh hình bao quanh
    x, y = approx[0][0]
    cv2.putText(image, shape_name, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    if shape_name == "hinh tron":
        # Tìm tâm và bán kính của hình tròn
        (x, y), radius = cv2.minEnclosingCircle(approx)
        center = (int(x), int(y))
        radius = int(radius)

        # Vẽ hình tròn
        cv2.circle(image, center, radius, (0, 0, 255), 2)
        cv2.putText(image, f"Toa Do: ({x}, {y})", (int(x), int(y) + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        print(f"Toa Do: ({x}, {y})")

        if 128 <= x <= 130 and 31 <= y <= 33:
            print("Công tắc 1")
        elif 75 <= x <= 76 and 32 <= y <= 34:
            print("Công tắc 2")
        elif 19 <= x <= 21 and 31 <= y <= 33:
            print("Công tắc 3")

        print("Số lượng : ", dem_led)

# Hiển thị ảnh kết quả
cv2.imshow("Shape Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
