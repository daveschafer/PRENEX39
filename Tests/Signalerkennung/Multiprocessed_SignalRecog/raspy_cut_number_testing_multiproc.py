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

#Multiprocessing
#process vs pool
#https://www.ellicium.com/python-multiprocessing-pool-process/
import multiprocessing
from multiprocessing import Pool
import os

warnings.filterwarnings('ignore')

#############################################
# Disclaimer                                #
#                                           #
# This really uses up all your Pis memory   #
# Please enhance the swap file before this  #
# (500MB at least)                          #
#############################################


##@urs, was ist das? noch benötigt?

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

def tesseract(image):
    #return image_to_string(image, lang='eng', config='--psm 6')
    #Alternative mit Digits traineddata file (NUR nummern) --> Much faster
    return image_to_string(image, lang='digits', config='--psm 6')


#############################

@DeprecationWarning
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


    #####################
    ## MultiProcessing ##
    #####################

    #prepare pool:
    pool = Pool(processes=4)
    #prepare return list (not needed?)
    #results = list(range(4))

    counter = 0 
    print("Starting singal() capture multiproc mode")
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # Capture frame-by-frame

        #NEVER pass the frame, always pass the converted img
        img = frame.array[:120][:][::]

        pool.apply_async(process_frame_worker, (img ,counter,))
        counter+=1
        time.sleep(0.25)

        #Das sollte trotzdem in der Schleife bleiben
        rawCapture.truncate(0)

        #waitkey is needed only for imshow (GUI), else picture wont display with imshow
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break

#######################################


def process_frame_worker(img=0, counter=0):
    #print("[Proc-%s] started"% counter)
    #print('Running in process: {}'.format(os.getpid()))
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cont = img.copy()
    canny = cv2.Canny(gray, 30, 250)
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    new_contour = []
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

    try:
        if int(get_number) > 0: 
            #sound.play(str(int(get_number)))
            print('Running in process: {}'.format(os.getpid()))

            print("[Recognized][Proc-%s]: Got some Number %s"%(counter,str(get_number)))
            print("[Time]: %s"%datetime.datetime.now().time())
            #savestring = "/home/pi/testing/pics/recog_%s_co%s.jpg"%(get_number,counter)
            #cv2.imwrite(savestring, number)
            ##ToDo: Irgend ein Interrupt, sobald eine Nummer "sicher" erkannt wurde, sollte man aus dem Multiprocess loop ausbrechen
    except:
        print("[No][Proc-%s] not a number"%counter)
        print("[Time]: %s"%datetime.datetime.now().time())
        #savestring2 = "/home/pi/testing/pics/no_numb_co%s.jpg"%(counter)
        #cv2.imwrite(savestring2, number)
    
    #you have to return, else the process does never end
    #print("[Proc-%s] ended", counter)

    return

#########################

#wichtig: Multiprocessing sollten in einem main modul gestartet werden, ansonsten
#wissen die subprocceses nicht wo ansiedeln
if __name__ == '__main__':
    print("Main gestartet :)")
    print('Running in process: {}'.format(os.getpid()))

    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 40
    rawCapture = PiRGBArray(camera, size=(320, 240))
    camera.shutter_speed = 200
    camera.iso = 100
    camera.rotation = 180

    #time to init
    time.sleep(1)

    print("taking test image:")
    camera.capture("testimg.jpg")


    #####################
    ## MultiProcessing ##
    #####################

    #prepare pool:
    pool = Pool(processes=4)
    #prepare return list (not needed?)
    #results = list(range(4))

    counter = 0 

    print("[Ludicrous Mode] : Starting Image Recognition")
    # Capture frame-by-frame
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        #NEVER pass the frame, always pass the converted img
        img = frame.array[:120][:][::]

        pool.apply_async(process_frame_worker, (img ,counter,))

        counter = counter + 1

        #Wenn wirklich jedes Frame verarbeitet wird, wird es etwas CPU lastig.
        # Variante 1: nach x-Mal Signal erkannt -> Exit des Loops
        # Variante 2: Timeout einbauen damit wir die CPU nicht überlasten
        time.sleep(0.01)

        #wichtig, immer schön truncaten
        rawCapture.truncate(0)
      
    
    print("for loop ended, how?")
 

#signal()

# multiprocessing and capture_continous --> never pass the frame, this is like accessing
# the camera itself, what is blocked by the camera firmware 
# https://stackoverflow.com/questions/53561122/raspi-camera-module-not-working-in-separate-process
