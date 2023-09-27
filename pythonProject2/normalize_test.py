import cv2

img = cv2.imread("color_led1.jpg")
cv2.imshow("test", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
