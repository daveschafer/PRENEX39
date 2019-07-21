from picamera.array import PiRGBArray
from picamera import PiCamera
import math
import numpy as np

import sys
sys.path.append('/usr/local/python/cv2/python-3.5/')

import cv2
import time
import subprocess
from PIL import Image
import pytesseract
import re
import numpy as np
import matplotlib.pyplot as plt

#camera = PiCamera()
#camera.resolution = (320, 180)
#camera.framerate = 30
#rawCapture = PiRGBArray(camera, size=(320, 180))
#shutterspeed = (int)(input("shutterspeed: "))
#camera.shutter_speed = shutterspeed
#camera.iso = 1600

#empfohlene auflösung 320 x 180
img = cv2.imread('picture_32.jpg')
print(img.shape)
L = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
plt.rcParams['figure.dpi']= 200

gray = cv2.cvtColor(img[:][0:100][::], cv2.COLOR_BGR2GRAY)

contours, hierarchy = cv2.findContours(cv2.filter2D(cv2.Canny(gray,120,250), -1, L), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
counter = 0
new_contour = []
print(len(contours))

for i in range(0,len(contours)):
    epsilon = 0.1*cv2.arcLength(contours[i],True)
    approx = cv2.approxPolyDP(contours[i], epsilon, closed=True)
    if(abs(cv2.contourArea(contours[i])) > 2 and len(approx) == 2 and not(cv2.isContourConvex(approx))):
        new_contour.append(contours[i])
        x,y,w,h = cv2.boundingRect(contours[i])
        if(w > 15 and (y + h) > 98 and h > 30):
            cv2.rectangle(img, (x, y + 1), (x + w, y + w), (0, 255, 0), 2)
            cv2.imshow('img',img)
            counter = counter + 1
            u = (int)(h / 9)
            r = (int)(2 * u)
            cropped = img[y + u: y + h - r, x + u: x + w - r]
            cv2.imshow('cropped',cropped)
            image_string = pytesseract.image_to_string(
                        cropped, config='-c tessedit_char_whitelist=0123456789 --oem 0 --psm 10')
            print("string: " +image_string)

#cv2.imshow(img[:][:100][::])   
print(counter)