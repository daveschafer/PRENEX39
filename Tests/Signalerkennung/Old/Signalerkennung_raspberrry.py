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

camera = PiCamera()
camera.resolution = (320, 192)
camera.framerate = 64
rawCapture = PiRGBArray(camera, size=(320, 192))
camera.shutter_speed = 10000
camera.iso = 1600

time.sleep(1)

pattern = re.compile("^(\d)$")
#dictionary of all contour
contours = {}
#array of edges of polygon
approx = []
#scale of the text
scale = 2


#stop programm
print("press q to exit")

#calculate angle


def angle(pt1, pt2, pt0):
    dx1 = pt1[0][0] - pt0[0][0]
    dy1 = pt1[0][1] - pt0[0][1]
    dx2 = pt2[0][0] - pt0[0][0]
    dy2 = pt2[0][1] - pt0[0][1]
    return float((dx1*dx2 + dy1*dy2))/math.sqrt(float((dx1*dx1 + dy1*dy1))*(dx2*dx2 + dy2*dy2) + 1e-10)


ret = True
counter = 0
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #Capture frame-by-frame
    image = frame.array
    if ret == True:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img = cv2.GaussianBlur(gray, (5, 5), 0)
        squares = []
        cv2.imshow('rectangle', image)
        for gray in cv2.split(img):
            for thrs in range(0, 255, 26):
                if thrs == 0:
                    bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                    edges = cv2.Canny(gray, 10, 250)
                    cv2.imshow('edges', edges)
                    bin = cv2.dilate(bin, None)
                else:
                    _retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
                bin, contours = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    cnt_len = cv2.arcLength(cnt, True)
                    cnt = cv2.approxPolyDP(cnt, 0.02 * cnt_len, True)
                    if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                        IS_FOUND = 1
                        cnt = cnt.reshape(-1, 2)
                        max_cos = np.max([angle(cnt[i], cnt[(i + 1) % 4], cnt[(i + 2) % 4]) for i in range(4)])
                        cv2.imshow('cropped', max_cos)
                        if max_cos < 0.1:
                            image_string = pytesseract.image_to_string(
                                max_cos, config='-c tessedit_char_whitelist=0123456789 --oem 0 --psm 10')
                            print(image_string)

        #Display the resulting frame
        #out.write(frame)
        rawCapture.truncate(0)
        if cv2.waitKey(27) & 0xFF == ord('q'):
            break

#When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

