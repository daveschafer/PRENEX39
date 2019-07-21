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

camera = PiCamera()
camera.resolution = (320, 192)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(320, 192))
shutterspeed = (int)(input("shutterspeed: "))
camera.shutter_speed = shutterspeed
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

def angle(pt1, pt2, pt0):
    dx1 = pt1[0][0] - pt0[0][0]
    dy1 = pt1[0][1] - pt0[0][1]
    dx2 = pt2[0][0] - pt0[0][0]
    dy2 = pt2[0][1] - pt0[0][1]
    return float((dx1*dx2 + dy1*dy2))/math.sqrt(float((dx1*dx1 + dy1*dy1))*(dx2*dx2 + dy2*dy2) + 1e-10)

ret = True
counter = 0
oldNumber = 0
list = []
found = False

fgbg = cv2.createBackgroundSubtractorMOG2()

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    #Capture frame-by-frame
    image = frame.array
    
    #Background subtraction dosn't work as excpected
    fsub = fgbg.apply(image)
    cv2.imshow('fsub',fsub)

    if ret == True:
        image = image[0: 500, 0:500]
        
        
        #cv2.imshow('cropped', image)
        #grayscale
        #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        """
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # convert it to hsv
        h, s, v = cv2.split(hsv)
        """
        """
        value = 100
        lim = 255 - value
        v[v > lim] = v
        v[v <= lim] = 255
        """
        #v+=255
        #lower_red = np.array([110, 50, 50])
        #upper_red = np.array([130, 255, 255])
        
        """
        final_hsv = cv2.merge((h, s, v))
        #bright = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        cv2.imshow('brightness', bright)
        """

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #print((str)(camera.exposure_speed))
        canny = cv2.Canny(gray, 80, 240, 3)
        #contours
        cv2.imshow('frame', image)
        cv2.imshow('canny', canny)

        contours, hierarchy = cv2.findContours(canny ,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        counterR1 = 0

        for i in range(0, len(contours)):
            #           #approximate the contour with accuracy proportional to
            #            #the contour perimeter
             img = contours[i]
             approx = cv2.approxPolyDP(
                 contours[i], cv2.arcLength(img, True)*0.02, False)

             #take some picturez
             #if(counterR1 % 20 == 0):
                #current = str(time.time())
                #cv2.imwrite('../Pictures/canny_img_' + current + str(counterR1) + '_.jpg', canny)
                #cv2.imwrite('../Pictures/rectangle_img_' + current + str(counterR1) + '_.jpg', image)

#            #Skip small or non-convex objects
             #if(abs(cv2.contourArea(img)) < 100 or not(cv2.isContourConvex(approx))):
             if(abs(cv2.contourArea(img)) < 100):
                 continue
                #ractangle
             if(len(approx) == 4 ):
                 x, y, w, h = cv2.boundingRect(img)
                 verhaeltnis = w / h

                 if (w >= 50 and w < 200 and h >= 75 and h < 200 and verhaeltnis > 0.7 and verhaeltnis < 1.3):
                    u = (int)(h / 9)
                    r = (int)(2 * u)
                    #darwing rectangle
                    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 3)
                    cv2.imshow('rectangle', image)
                    cropped = image[y + u: y + h - r, x + u: x + w - r]
                    current = str(time.time())
                    print("Time:"+current)

                    cv2.imwrite( '../Pictures/test_img_' + current + '_.jpg', image )
                    cv2.imshow('cropped', cropped)
                    _retval, bin = cv2.threshold(cropped, 127, 255, cv2.THRESH_BINARY)
                    cv2.imshow('tresh', bin)
                    #todo corina: z.B. nach 3 mal erkennen der gleichen Zahl
                    #stoppen mit der auswertung (bez. keine weiteren Bilder für x sekunden analysieren)

                    image_string = pytesseract.image_to_string(
                        cropped, config='-c tessedit_char_whitelist=0123456789 --oem 0 --psm 10')
                    print(image_string)
                    """
                    if(len(list) > 0):
                        for x in list:
                            if(list[x] == image_string):
                                list[x][x] += 1
                                found = true
                                print("imagestring " + image_string)

                        if(found == False):
                                list[x] = image_string
                                list[x][x] = 1
                                print("new imagestring " + image_string)

                        for i in list:
                            for j in list:
                                if(list[i][j] == 3):
                                    infosignalstring = list[i]
                                    print("info: " + (str)(infosignalstring))
                    """
                    #return value

    #Display the resulting frame
    #out.write(frame)
    rawCapture.truncate(0)
    if cv2.waitKey(27) & 0xFF == ord('q'):
        break

#When everything done, release the capture
#cap.release()
cv2.destroyAllWindows()
