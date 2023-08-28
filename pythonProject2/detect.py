import cv2
import numpy as np

def calculate_color_percentage(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    color_ranges = {
        'red': ([0, 70, 50], [10, 255, 255]),
        'yellow': ([25, 70, 50], [35, 255, 255]),
        'green': ([35, 70, 50], [85, 255, 255]),
        'blue': ([90, 70, 50], [130, 255, 255]),
    }

    color_percentages = {}
    total_pixels = hsv_image.shape[0] * hsv_image.shape[1]

    for color, (lower, upper) in color_ranges.items():
        mask = cv2.inRange(hsv_image, np.array(lower), np.array(upper))
        pixel_count = np.count_nonzero(mask)

        percentage = (pixel_count / total_pixels) * 100
        color_percentages[color] = percentage

    return color_percentages

def main():
    image = cv2.imread("Xanh_tron.jpg")

    color_percentages = calculate_color_percentage(image)

    for color, percentage in color_percentages.items():
        print(f"{color}: {percentage:.2f}%")  # Display percentages with two decimal places

if __name__ == "__main__":
    main()