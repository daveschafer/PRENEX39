from picamera.array import PiRGBArray
from picamera import PiCamera
import math
import numpy as np
import sys
sys.path.append('/usr/local/python/cv2/python-3.5/')
import cv2
import matplotlib as mpl
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
import pytesseract
#pytesseract.pytesseract.tesseract_cmd = '/usr/share/tesseract-ocr/tesseract.exe'
import time


camera = PiCamera()
camera.resolution = (320, 192)
camera.framerate = 40
rawCapture = PiRGBArray(camera, size=(320, 192))
#shutterspeed = (int)(input("shutterspeed: "))
camera.shutter_speed = 400
#camera.shutter_speed = shutterspeed
camera.iso = 800

time.sleep(1)

number = 0
count = 0

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #Capture frame-by-frame
    img = frame.array

    #print(img.shape)
    L = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
    rcParams['figure.dpi']= 200
    #img = img[50: 150, 0:400] #infosignal
    #img = img[200:500, 0:300] #Haltesignal
    import glob
    number = 0
    image = img.copy()

    gray = cv2.cvtColor(img[:][:][::], cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray,120,250)
    contours, hierarchy = cv2.findContours(cv2.filter2D(canny, -1, L), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    counter = 0
    new_contour = []
    for i in range(0,len(contours)):

        if(abs(cv2.contourArea(contours[i])) > 2):
            new_contour.append(contours[i])
            x,y,w,h = cv2.boundingRect(contours[i])
            rel = h / w
            addh = int(h / 4)
            addw = int(w / 2)
            if(rel > 1.5 and h > 20 and h < 50 and w > 20 and w < 50):
                cv2.rectangle(img, (x - addh, y - addw), (x + w + addw, y + h + addh), (0, 255, 0), 1)

                cropped = img[y - addw:y + h + addh,x - addh:x + w + addw]
                _retval, bin = cv2.threshold(cropped, 30, 255, cv2.THRESH_BINARY)

                #image_string = pytesseract.image_to_string(
                #        cropped, lang='eng', config='-c tessedit_char_whitelist=0123456789 --oem 0 --psm 10')
                #print(image_string)

                counter = counter + 1
                number = number + 1 
                current = str(time.time())
                cv2.imwrite(r'../new/numbers/file_' + str(number) +'_'+str(current)+ '.jpg', img)
                print("saved image")
    rawCapture.truncate(0)
#imshow(cont)

finish = time.time()
#print('%.5ffps' % ((finish - start)))

