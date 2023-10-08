# import required libraries
import cv2

# read the input image as a gray image
img = cv2.imread('LED_OFF.jpg',0)
img2 = cv2.imread('LED_ON.jpg', 0)

# Apply Otsu's thresholding
_,th = cv2.threshold(img,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
_,th2 = cv2.threshold(img2,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# display the output image
cv2.imshow("Otsu's Thresholding", th)
cv2.imshow("Otsu's Thresholding 2", th2)

cv2.waitKey(0)
cv2.destroyAllWindows()