import cv2
import os
import matplotlib.pyplot as plt

os.environ['QT_QPA_PLATFORM'] = 'wayland'

# Read the images
img = cv2.imread('anh1_0.jpg')
img2 = cv2.imread('anh1_on_0.jpg')
img3 = cv2.imread('anh4_off_34.jpg')

# Convert the images to grayscale
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
gray_img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)

# Calculate the histograms
hist_img = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
hist_img2 = cv2.calcHist([gray_img2], [0], None, [256], [0, 256])
hist_img3 = cv2.calcHist([gray_img3], [0], None, [256], [0, 256])

# Plot the images and histograms
plt.figure(figsize=(10, 10))

plt.subplot(3, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('OFF')
plt.axis('off')

plt.subplot(3, 2, 2)
plt.imshow(cv2.cvtColor(img2, cv2.COLOR_BGR2RGB))
plt.title('ON/ON')
plt.axis('off')

plt.subplot(3, 2, 3)
plt.imshow(cv2.cvtColor(img3, cv2.COLOR_BGR2RGB))
plt.title('ON/OFF')
plt.axis('off')

plt.subplot(3, 2, 4)
plt.plot(hist_img, color='black')
plt.title('OFF')
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')

plt.subplot(3, 2, 5)
plt.plot(hist_img2, color='black')
plt.title('ON/ON')
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')

plt.subplot(3, 2, 6)
plt.plot(hist_img3, color='black')
plt.title('ON/OFF')
plt.xlabel('Pixel Value')
plt.ylabel('Frequency')

plt.tight_layout()
plt.show()