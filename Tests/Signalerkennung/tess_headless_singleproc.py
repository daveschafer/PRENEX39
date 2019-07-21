from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import datetime
from pytesseract import image_to_string
import pytesseract
import re

import numpy as np
#from keras.models import load_model
import warnings

import sys
sys.path.append('/usr/local/python/cv2/python-3.5/')
import cv2


# Multiprocessing
import os

warnings.filterwarnings('ignore')
import glob

template_check = []
#model = load_model("traineddata/numbers.h5")


def tesseract(image):
    return image_to_string(image, lang='digits', config='--psm 6')


# model
def detect(image):
    image = cv2.resize(image, (28, 28))
    vectorized_image = image.reshape(1, 28, 28, 1)
    predictions = model.predict(vectorized_image)
    predicted_digit = np.argmax(predictions)
    return predicted_digit


def init_template_matching():
    print("init some templates")
    for filepath in sorted(glob.iglob('templates/*.png')):
        img = cv2.imread(filepath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        binary = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)[1]
        template_check.append(binary)


def compare_template(picture):
    res_max = 100
    res_number = -1
    picture = cv2.resize(picture, (28, 28))

    for i in range(0, 10):
        # print(i)
        res = cv2.matchTemplate(
            picture, template_check[i], cv2.TM_SQDIFF_NORMED)
        #print("i:{} res:{} res_max:{}".format(i, res, res_max))

        if(res < res_max):
            res_number = i
            res_max = res
    return (res_number, res)



# MAIN
if __name__ == '__main__':
    print("Main gestartet :)")
    print('Running in process: {}'.format(os.getpid()))

    camera = PiCamera()
    camera.resolution = (320, 240)
    camera.framerate = 40
    rawCapture = PiRGBArray(camera, size=(320, 240))
    camera.shutter_speed = 50
    camera.iso = 1600
    camera.rotation = 180

    #do some test images
    camera.capture("testimg.jpg")

    #init templates
    #init_template_matching()

    # time to init
    time.sleep(1)

    counter = 0


    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        # NEVER pass the frame, always pass the converted img
        #img = frame.array[:120][:][::]
        img = frame.array[:120,:,:]

        # gray and canny
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 50, 230)

        # find contours
        contours, hierarchy = cv2.findContours(
            canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for i in range(0, len(contours)):
            x, y, w, h = cv2.boundingRect(contours[i])

            rel = h / w
            # adding space to contours
            addh = int(h / 12)
            addw = int(w / 8)
            if addw < 1:
                addw = 1

            # coordinates for bounding rectangle
            top_border = y - addh
            bottom_border = y + h + addh
            left_border = x - addw
            right_border = x + w + addw

            # calculations for timo's model
            addh_model = int(h / 5)
            addw_model = int(w / 2)
            top_border_model = y - addh_model
            bottom_border_model = y + h + addh_model
            left_border_model = x - addw_model
            right_border_model = x + w + addw_model

            image = img.copy()
            cv2.drawContours(image, contours[i], -1, (0,255,255), 2)

            # skip contour if too smallor too big
            if (rel < 1.45 or rel > 4 or w <= 4 or w >= 50 or h <= 15 or h >= 60 or top_border < 0 or left_border < 0 or bottom_border > 240):
            #    # print data of contour
            #    print("\n\nh={}  w={} r={} c={} ".format(
            #        h, w, rel, cv2.isContourConvex(contours[i])))
            #    print("x={}  y={} xw={} yw={} s={} ".format(
            #        left_border, top_border, right_border, bottom_border, len(contours[i])))
                continue    

            # cut_number and make it binary
            number = cv2.threshold(
                gray[top_border:bottom_border, left_border:right_border], 30, 255, cv2.THRESH_BINARY)[1]


            # calculate right and bottom row of array
            bottom_row, right_col = number.shape
            bottom_row -= 1
            right_col -= 1

            # invert if signal is black
            if number[bottom_row, :].all() == 0:
                number = cv2.bitwise_not(number)

            # calculate relation of black and white
            nonzeroes = np.count_nonzero(number) / np.prod(number.shape)

            # check if bottom row and right col complete white
            if number[:, right_col].all() != 0 and number[bottom_row, :].all() != 0 and nonzeroes > 0.6 and nonzeroes < 0.9:
                # Template
                #get_number_temp_match, res = compare_template(number)
                get_number_temp_match = tesseract(number)


                try:
                    number_check = int(get_number_temp_match) #check for no number
                    #print("[Recognized][Proc-%s]: Got some Number %s - %s"%(counter,str(get_number_temp_match),res))
                    print("[Recognized][Proc-%s]: Got some Number %s"%(counter,str(get_number_temp_match)))

                except:
                    pass
        

        # Truncate after frame processing
        rawCapture.truncate(0)
