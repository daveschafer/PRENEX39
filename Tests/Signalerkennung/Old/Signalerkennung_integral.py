"""
import math
import numpy as np


import skimage
import skimage.data
import skimage.io
import skimage.future
import skimage.segmentation
import sklearn.cluster
"""

import sys

sys.path.append('/usr/local/python/cv2/python-3.5/')

import cv2

image = cv2.imread("rectangle.jpg")
cv2.imshow("Image",image)
sub = image[200:500, 200:1500]
sub_gray = cv2.cvtColor(sub, cv2.COLOR_RGB2GRAY)

cv2.imshow("gray",sub_gray)
integral_image = cv2.integral(sub_gray)
#plt.imshow(integral_image)


# sum = C + A - B - D\n",
# see https://en.wikipedia.org/wiki/Haar-like_feature\n",
def haar_feature(integral_image, height, width, row, col):
    c = integral_image[row+height, col+width]
    a = integral_image[row, col]
    b = integral_image[row, col+width]
    d = integral_image[row+height, col]
    return c + a - b - d

def find_rect(integral_image, height, width):
    max_value = 0
    max_position = (0,0)
    for row in range(integral_image.shape[0] - height - 1):
        for col in range(integral_image.shape[1] - width - 1):
            value = haar_feature(integral_image, height, width, row, col)
            if value > max_value:
                max_value = value
                max_position = (row, col)
    return max_position

height = 150
width = 150
pos = find_rect(integral_image, height, width)

# display result\n",
displayed_image = cv2.cvtColor(sub_gray, cv2.COLOR_GRAY2RGB)
# OpenCV wants the position in x and y, which is different as row, col\n",
pos_xy = (pos[1], pos[0])
pos2_xy = (pos[1]+width, pos[0]+height)
cv2.rectangle(displayed_image, pos_xy, pos2_xy, (255, 0,0), 5)
#plt.rcParams['figure.figsize'] = [10, 20]
cv2.imshow("displ", displayed_image)

print("runned")
# try to find in the full image, but there will be too much white areas\n",
full_integral_image = cv2.integral(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY))
height = 150
width = 150
pos = find_rect(full_integral_image, height, width)
# display result\n",
displayed_image = image.copy()
# OpenCV wants the position in x and y, which is different as row, col\n",
pos_xy = (pos[1], pos[0])
pos2_xy = (pos[1]+width, pos[0]+height)
cv2.rectangle(displayed_image, pos_xy, pos2_xy, (255, 0,0), 5)
#plt.rcParams['figure.figsize'] = [10, 20]
cv2.imshow("image", displayed_image)

