import cv2
import numpy as np
from matplotlib import pyplot as plt

# reading the input image
img = cv2.imread('anh1_0.jpg')
img2 = cv2.imread('anh1_on_0.jpg')

# computing the histogram of the blue channel of the image
hist1 = cv2.calcHist([img], [0], None, [256], [0, 256])
hist2 = cv2.calcHist([img], [0], None, [256], [0, 256])

# plot the above computed histogram
plt.plot(hist1, color='b')
plt.plot(hist2, color='g')
plt.title('Image Histogram For Blue Channel GFG')
plt.show()
