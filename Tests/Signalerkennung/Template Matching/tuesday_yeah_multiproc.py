from picamera.array import PiRGBArray
from picamera import PiCamera
import math
import sound
import numpy as np
import datetime
import sound
from multiprocessing import Pool
import multiprocessing
from multiprocessing import Queue

from pytesseract import image_to_string
import numpy as np
from pathlib import Path
import warnings
import time
import subprocess
from PIL import Image
import pytesseract
import re

#Import Threading classes
import threading
import multiprocessing

import sys
sys.path.append('/usr/local/python/cv2/python-3.5/')

import cv2


warnings.filterwarnings('ignore')

L = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])


pattern = re.compile("^(\d)$")
#dictionary of all contour
contours = {}
#array of edges of polygon
approx = []


#stop programm
print("press q to exit")

#auswertung zahl zu string
def tess(image):
#while not info_signal_queue.empty():
#        getimage = signalerkennung.info_signal_queue.get()
        image_string = pytesseract.image_to_string(image, config='--oem 0 --psm 5')
        detected_number = re.search('\d+',image_string)[0]
        print(detected_number)
        sound.play(str(detected_number))
        return detected_number


#AUfnahme und zuschneiden
def signal(procnumber=0, return_dict="null"):
     
    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 40
    camera.shutter_speed = 50
    camera.iso = 800
    camera.rotation =  180
    rawCapture = PiRGBArray(camera, size=(320, 240))
    
    time.sleep(1)

    ret = True
    counter = 0

    startframes = time.time()

    for i in range(1000):
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            #Capture frame-by-frame

            counter = counter + 1
            if counter % 40 == 0:
                stopframes = time.time()
                print('Captured images at %.3ffps' % (counter / (stopframes - startframes)))

            #start = time.time()
            image = frame.array[:120][:][::]
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            #gray = image.copy()
            cont = gray.copy()

            if ret==True:
    #            start = time.time()
                canny = cv2.Canny(gray,120,250)
                contours, hierarchy = cv2.findContours(cv2.filter2D(canny, -1, L), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for i in range(0,len(contours)):
                    if(abs(cv2.contourArea(contours[i])) > 0):
                        x,y,w,h = cv2.boundingRect(contours[i])
                        rel = h / w
                        addh = int(h / 8)
                        addw = int(w / 8)
                        #if(rel > 1.5 and h > 35 and h < 41 and rel < 3 and x < 200 and y < 40):
                        if(rel > 1.5 and h > 30 and h < 45 and rel < 3 and x < 200 and (y < 40 or y > 130)):
    #                    if(h > 20):
    #                       cont = image.copy()
                            #cv2.polylines(cont, [contours[i]], False, (0,255,0), 2)
                            number = cv2.threshold(cont[y - addh:y + h + addh,x - addw:x + w + addw], 30, 255, cv2.THRESH_BINARY)[1]
                            try:
                                if number[0][0][:].all() == 0:
                                    number = cv2.bitwise_not(number)
                                if number[0][0][:].all() != 0:
                                    cont[y - addh:y + h + addh,x - addw:x + w + addw,::] = number
                            
    #                                filetimestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')

                                    
                                    detected_number = tess(number)
                                    return_dict[procnumber]= detected_number
    #                                cv2.rectangle(cont, (x - addw, y - addh), (x + w + addw, y + h + addh), (0, 0, 255), 1)

                                    #cv2.imwrite('output/320240_' + filetimestamp + "_" + str(detected_number) + '.jpg', number)
                                    #cv2.imwrite('output/320240_' + filetimestamp + "_" + str(detected_number) + '_raw.jpg', gray)
                                    #cv2.imwrite('output/320240_' + filetimestamp + "_" + str(detected_number) + '_cropped.jpg', gray[y - addh:y + h + addh,x - addw:x + w + addw])
                                    #print("Number detected: " + str(detected_number))

    #                                cv2.putText(cont, "h={}  w={}".format(h, w),
    #                                    (x + w + addw + 5, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
    #                                cv2.putText(cont, "r={:.2f}".format(rel),
    #                                    (x + w + addw + 5, y + 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
    #                                cv2.putText(cont, "x={} y={} a={}".format(x, y, abs(cv2.contourArea(contours[i]))),
    #                                    (x + w + addw + 5, y + 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
    #                                cv2.putText(cont, "number={}".format(detected_number),
    #                                    (x + w + addw + 5, y + 45), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1)
                                    #cv2.imwrite('output/320240_' + filetimestamp + "_" + str(detected_number) + '_labeled.jpg', cont)
                                    break
                            except:
                                huhu = 1
                                #print(number)
                #cv2.imshow('test', cont)   
                #cv2.imshow('number', number)   
                #cv2.imshow('gray', gray)   
                #cv2.imshow('canny', canny)   

                #finish = time.time()
                #print('Captured images at %.3ffps' % (1 / (finish - start)))
            
            rawCapture.truncate(0)
            return detected_number



if __name__ == '__main__':
    print("="*40)
    print("Single Core Solution\n")

    ## Zeitmessung ##
    start_time = time.time()
    count = 100
    det_number = signal(99)
    print("[Single]Detected Number: ", det_number)


    ## Zeitmessung Stop##
    end_time = time.time()

    print("Duration: %s"% (end_time - start_time))
    print("Runs: %s"%count)
    print("'fps': %s"% (count / (end_time - start_time)))

    time.sleep(1)

    print("="*40)
    print("Multi Core Solution\n")

    ## Zeitmessung ##
    start_time2 = time.time()

 

    ##pass variables via shared variables when working with multiproc
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    for i in range(3):
        ###Asynchrone Arbeitsverteilung###
        p = multiprocessing.Process(target=signal, args=(3,i, return_dict))
        jobs.append(p)
        p.start()

    for proc in jobs:
        #Synchronisieren#
        proc.join()

    print("[Multi]Detected Numbers: ", return_dict.values())

    ## Zeitmessung Stop ##
    end_time2 = time.time()

    print("Duration: %s"% (end_time2 - start_time2))
    print("Runs: %s"%1000)
    print("'fps': %s"% (1000 / (end_time2 - start_time2)))

    print("="*40)

    print("Geschwindigkeitsboost um Faktor: %s"% ( (end_time - start_time) /((end_time2 - start_time2) /100)))