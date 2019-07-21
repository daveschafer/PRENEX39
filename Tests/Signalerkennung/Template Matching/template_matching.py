from picamera.array import PiRGBArray
from picamera import PiCamera
import math
import sound
import numpy as np
import datetime
import sys
sys.path.append('/usr/local/python/cv2/python-3.5/')

import cv2
import time
import subprocess
from PIL import Image
import pytesseract
import re
import glob

#Import Threading classes
import threading
import multiprocessing

L = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])

# stop programm
print("press q to exit")

count_number = 0
template_check = []
list = []

def compare_template(picture):
    res_max = 100
    res_act = 100
    res_number = -1
    picture = cv2.resize(picture, (50, 50))
    for i in range(0, 9):
        res = cv2.matchTemplate(picture, template_check[i], cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        print(min_val)
        if (min_val < res_max):
            res_number = i + 1
            res_act = min_val
            res_max = min_val
    return res_number


for filepath in glob.iglob('templates/*.jpg'):
    count_number = count_number + 1
    img = cv2.imread(filepath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    binary = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)[1]
    binary = cv2.resize(binary, (50, 50))
    template_check.append(binary)
    


def multi_signal_worker(procnumber, image, return_dict):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)[:][:]
    cont = image.copy()
    canny = cv2.Canny(gray,60,180)
    number = image.copy()
    contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    counter = 0
    new_contour = []
    ret = True
    if ret==True:
    # Capture frame-by-frame
        for i in range(0,len(contours)):
                    print(hierarchy[0][i])
                    if(abs(cv2.contourArea(contours[i])) > 0 and hierarchy[0][i][0] > -1):
                        xm, ym, wm, hm = cv2.boundingRect(contours[hierarchy[0][i][0]])
                        if((hm) > 40):
                            x,y,w,h = cv2.boundingRect(contours[i])
                            rel = h / w
                            addh = int(h / 8)
                            addw = int(w / 8)
                            print(hierarchy[0][i])
                            if(rel > 1.5 and h > 20 and w > 6 and h < 80):
                                number = cv2.threshold(gray[y - addh:y + h + addh,x - addw:x + w + addw], 30, 255, cv2.THRESH_BINARY)[1]
                                get_number = compare_template(number)
                                
                                try:  
                                    if number[0][0].all() == 0:
                                        number = cv2.bitwise_not(number)
                                    if number[0][0].all() != 0:
                                        cv2.rectangle(cont, (x - addw, y - addh), (x + w + addw, y + h + addh), (0, 0, 255), 1)
                    
                                        cv2.putText(cont, "h={}  w={} c={}".format(h, w, cv2.isContourConvex(contours[i])),
                                            (x + w + addw + 5, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
                                        cv2.putText(cont, "r={:.2f} a={} n={}".format(rel, abs(cv2.contourArea(contours[i])), i),
                                            (x + w + addw + 5, y + 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
                                        cv2.putText(cont, "x={} y={}".format(x, y),
                                            (x + w + addw + 5, y + 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
                                        cv2.putText(cont, "number={}".format(get_number),
                                            (x + w + addw + 5, y + 45), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1)
 
                                        if any(get_number in s for s in list):
                                            cv2.imshow('number',get_number)
                                        else:
                                            list.append([get_number])
                                except:
                                    count = 1 
        cv2.imshow('canny',canny)
        cv2.imshow('cont',cont)
        cv2.imshow('number',number)


def signal():
    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 40
    camera.shutter_speed = 50
    camera.iso = 1600
    camera.rotation = 180
    rawCapture = PiRGBArray(camera, size=(320, 240))

    time.sleep(1)

    #multiprocesso
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []


    ret = True
    counter = 0
    proc_ind = 1
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        #Capture frame-by-frame
        image = frame.array

        for i in range(3):
            ###Asynchrone Arbeitsverteilung###
            p = multiprocessing.Process(target=multi_signal_worker, args=(proc_ind,image, return_dict))
            jobs.append(p)
            p.start()

        for proc in jobs:
            #Synchronisieren#
            proc.join()

        print("Numbers:")
        print(return_dict.values())


        proc_ind = proc_ind+1
        rawCapture.truncate(0)
        if cv2.waitKey(27) & 0xFF == ord('q') :
            break

    # When everything done, release the capture


#wichtig: Multiprocessing muss in einem main modul gestartet werden, ansonsten
#wissen die subprocceses nicht wo ansiedeln
if __name__ == '__main__':
    print("="*40)
    print("Multi Core Solution\n")
    signal()
