import math
import numpy as np

import sys
sys.path.append('/usr/local/python/cv2/python-3.5/')
import cv2

import imutils
from imutils.perspective import four_point_transform
from imutils import contours
from PIL import Image, ImageEnhance, ImageFilter
#from skimage.measure import compare_ssim as ssim
import PIL.ImageOps
import time
import datetime
import pytesseract
from picamera.array import PiRGBArray
from picamera import PiCamera
CANNY = 250

camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 40
rawCapture = PiRGBArray(camera, size=(320, 240))
camera.shutter_speed = 50
camera.iso = 1600

time.sleep(1)
# capture frames from the camera
VIDEO_BASE_FOLDER = '/home/pi/Videos/'
VIDEO_LENGTH = 60*1000
# global definitions
current_time_ms = lambda: int(round(time.time() * 1000))
# use this to define your file name builder, I just used the Unix time
def get_video_filename(now):
    return VIDEO_BASE_FOLDER+str(now)+'_video.h264'
# the timestamp when the video write started
video_time  = 0
# main logic
def see():
    # initialize the camera and grab a reference
    clock = current_time_ms()
    video_time = clock
    # start recording using piCamera API
    camera.start_recording(get_video_filename(clock))
    # grab one frame at the time from the stream
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        # grab the raw NumPy array representing the image
        image = frame.array
        # establish a time for the rest of the logic
        now = current_time_ms()

        
        # all we do is show the frame ...
        cv2.imshow('frame',image)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
# clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        cv2.destroyAllWindows()

see()
