import math
import time
import sys
sys.path.append('/usr/local/python/cv2/python-3.5/')
import cv2
import time
import subprocess
from PIL import Image
import pytesseract
import re
import numpy as np

time.sleep(1)
image = cv2.imread('blob1.jpeg')
cv2.imshow("Image",image)
sub = image[200:500, 200:1000]
cv2.imshow("sub",sub)
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

def find_rect(integral_image, height, width, dark):
    max_value = 0
    max_position = (0,0)
    for row in range(integral_image.shape[0] - height - 5):
        for col in range(integral_image.shape[1] - width - 5):
            value = haar_feature(integral_image, height, width, row, col)
            if dark:
                if value < max_value and height > 75 and width > 75 :
                    max_value = value
                    max_position = (row, col)
            else:
                if value > max_value and height > 75 and width > 75 :
                    max_value = value
                    max_position = (row, col)
    return max_position

height = 150
width = 150
pos = find_rect(integral_image, height, width, False)

# display result\n",
displayed_image = cv2.cvtColor(sub_gray, cv2.COLOR_GRAY2RGB)
current = str(time.time())
#cv2.imwrite( '../Pictures/integral_img_' + current + '_.jpg', displayed_image )
# OpenCV wants the position in x and y, which is different as row, col\n",
pos_xy = (pos[1], pos[0])
pos2_xy = (pos[1]+width, pos[0]+height)
cv2.rectangle(displayed_image, pos_xy, pos2_xy, (255, 0,0), 5)
#plt.rcParams['figure.figsize'] = [10, 20]
#x, y, w, h = cv2.boundingRect(displayed_image)
cv2.imshow("displ", displayed_image)
u = (int)(height/9)
r= (int)(2*u)

cropped = displayed_image[pos[0]: pos[0]+height, pos[1]: pos[1]+ width]

#cropped = displayed_image[y + u: y + h - r, x + u: x + w - r]
cv2.imshow("cropped", cropped)
_retval, bin = cv2.threshold(cropped, 127, 255, cv2.THRESH_BINARY)
cv2.imshow('tresh', bin)

cropped_integral_image = cv2.integral(cv2.cvtColor(cropped, cv2.COLOR_RGB2GRAY))
height = 60
width = 60
pos = find_rect(cropped_integral_image, height, width, True)
displayed_image = image.copy()
pos_xy = (pos[1], pos[0])
pos2_xy = (pos[1]+width, pos[0]+height)
cv2.rectangle(displayed_image, pos_xy, pos2_xy, (255, 0,0), 5)
cv2.imshow("image2", displayed_image)

image_string = pytesseract.image_to_string(cropped, config='-c tessedit_char_whitelist=0123456789 --oem 0 --psm 10')
if(image_string != ""):
    print(image_string)

## try to find in the full image, but there will be too much white areas\n",
#full_integral_image = cv2.integral(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY))
#height = 150
#width = 150
#pos = find_rect(full_integral_image, height, width)
## display result\n",
#displayed_image = image.copy()
## OpenCV wants the position in x and y, which is different as row, col\n",
#pos_xy = (pos[1], pos[0])
#pos2_xy = (pos[1]+width, pos[0]+height)
#current = str(time.time())
#cv2.imwrite( '../Pictures/integral_img_' + current + '_.jpg', displayed_image )
#cv2.rectangle(displayed_image, pos_xy, pos2_xy, (255, 0,0), 5)
##plt.rcParams['figure.figsize'] = [10, 20]
#cv2.imshow("image", displayed_image)
#cv2.waitKey(0)
