from picamera.array import PiRGBArray
from picamera import PiCamera
import math
#import sound
import numpy as np
import datetime
import sys
import datetime

sys.path.append('/usr/local/python/cv2/python-3.5/')

import cv2
import time
import subprocess
from PIL import Image
import pytesseract
import re
from pytesseract import image_to_string

import warnings

warnings.filterwarnings('ignore')

show_pictures = sys.argv[1]
print(show_pictures)


def tesseract(image):
    return image_to_string(image, lang='eng', config='--psm 6')
    #Alternative mit Digits traineddata file (NUR nummern):
    #return image_to_string(image, lang='digits', config='--psm 6')



pattern = re.compile("^(\d)$")
# dictionary of all contour
contours = {}
# array of edges of polygon
approx = []
# scale of the text
scale = 2
# camera
# cap = cv2.VideoCapture(0)
# camera = PiCamera()

# stop programm
print("press q to exit")


def signal():
    
    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 40
    rawCapture = PiRGBArray(camera, size=(320, 240))
    camera.shutter_speed = 200
    camera.iso = 100
    camera.rotation = 180

    time.sleep(1)

    print("taking test image:")
    camera.capture("testimg.jpg")

    ret = True
    counter = 0
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # Capture frame-by-frame

        img = frame.array[:120][:][::]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cont = img.copy()
        canny = cv2.Canny(gray, 30, 250)

        contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        new_contour = []
        counter += 1
        hm = 50
        get_number = 0

        for i in range(0, len(contours)):
            epsilon = 0.1 * cv2.arcLength(contours[i], True)
            approx = cv2.approxPolyDP(contours[i], epsilon, closed=True)

            if (abs(cv2.contourArea(contours[i])) > 0):
                # if(abs(cv2.contourArea(contours[i])) > 0 and hierarchy[0][i][0] > -1):

                # xm, ym, wm, hm = cv2.boundingRect(contours[hierarchy[0][i][0]])
                if ((hm) > 40):
                    x, y, w, h = cv2.boundingRect(contours[i])
                    rel = h / w
                    addh = int(h / 8)
                    addw = int(w / 8)
                    if (rel > 1.5 and h > 20 and w > 10 and w < 40 and h < 55 and y > 5 and (y + h) < 235 and x < 220):
                        # if(rel > 1.3):
                        # cv2.polylines(cont, [contours[i]], False, (0,255,0), 2)
                        number = \
                            cv2.threshold(gray[y - addh:y + h + addh, x - addw:x + w + addw], 30, 255,
                                          cv2.THRESH_BINARY)[1]
                        try:
                            if number[0][0].all() == 0:
                                number = cv2.bitwise_not(number)

                            nonzeroes = np.count_nonzero(number) / np.prod(number.shape)
                            if number[0][0].all() != 0 and number[:][0].all() and nonzeroes > 0.65 and nonzeroes < 0.88:
                                get_number = tesseract(number)

                                if (show_pictures == "yes"):
                                    cv2.rectangle(cont, (x - addw, y - addh), (x + w + addw, y + h + addh), (0, 0, 255),
                                                  1)

                                    #cv2.imshow('number', cv2.resize(number, None, fx=5, fy=5))
                                    cv2.putText(cont, "h={}  w={} c={}".format(h, w, cv2.isContourConvex(contours[i])),
                                                (x + w + addw + 5, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
                                    cv2.putText(cont,
                                                "r={:.2f} a={} n={}".format(rel, abs(cv2.contourArea(contours[i])), i),
                                                (x + w + addw + 5, y + 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
                                    cv2.putText(cont, "x={} y={}".format(x, y),
                                                (x + w + addw + 5, y + 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
                                    cv2.putText(cont, "number={} l={}".format(get_number, len(approx)),
                                                (x + w + addw + 5, y + 45), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1)
                                    print(str(get_number) + " " + str(
                                        np.count_nonzero(number) / np.prod(number.shape)) + " " + str(
                                        np.count_nonzero(number)) + " " + str(np.prod(number.shape)))

                        except:
                            count = 1
        if (show_pictures == "yes"):
            #cv2.imshow('canny', canny)
            #cv2.imshow('cont', cont)
            print("")
        #    cv2.destroyAllWindows()

        try:
            if int(get_number) > 0:
                #sound.play(str(int(get_number)))
                print("[Recognized]: Got some Number %s"%str(get_number))
                print("[Time]: %s"%datetime.datetime.now().time())
                savestring = "/home/pi/testing/pics/recog_%s_co%s.jpg"%(get_number,counter)
                cv2.imwrite(savestring, number)
        except:
            print("[No] not a number")
            savestring2 = "/home/pi/testing/pics/no_numb_co%s.jpg"%(counter)
            print("[Time]: %s"%datetime.datetime.now().time())
            cv2.imwrite(savestring2, number)


        rawCapture.truncate(0)
        #waitkey is needed only for imshow (GUI), else picture wont display with imshow
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break


signal()
