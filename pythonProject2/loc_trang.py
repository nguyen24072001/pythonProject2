import cv2
import numpy as np

## Read
img = cv2.imread("Xanh_tron.jpg")

## convert to hsv
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

mask = cv2.inRange(hsv, (36, 25, 25), (70, 255,255))
imask = mask>0
green = np.zeros_like(img, np.uint8)
green[imask] = img[imask]

cv2.imwrite("green.jpg", green)
