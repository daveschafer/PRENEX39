import math
import numpy as np
import cv2
import time
import subprocess
from PIL import Image
import pytesseract
import re

pattern = re.compile("^(\d)$")
#dictionary of all contours
contours = {}
#array of edges of polygon
approx = []
#scale of the text
scale = 2
#camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 40)
cap.set(cv2.CAP_PROP_FRAME_WIDTH,320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)
cap.set(cv2.CAP_PROP_EXPOSURE, 0.05); 


#stop programm
print("press q to exit")

#calculate angle
def angle(pt1,pt2,pt0):
    dx1 = pt1[0][0] - pt0[0][0]
    dy1 = pt1[0][1] - pt0[0][1]
    dx2 = pt2[0][0] - pt0[0][0]
    dy2 = pt2[0][1] - pt0[0][1]
    return float((dx1*dx2 + dy1*dy2))/math.sqrt(float((dx1*dx1 + dy1*dy1))*(dx2*dx2 + dy2*dy2) + 1e-10)

while(cap.isOpened()):
    #Capture frame-by-frame
    ret, frame = cap.read()
    if ret==True:
        #grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = cv2.GaussianBlur(gray, (5, 5), 0)
        #Canny
        canny = cv2.Canny(img,80,240,3)

        #contours
        _retval, bin = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
        canny2, contours, hierarchy = cv2.findContours(bin,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for i in range(0,len(contours)):
            #approximate the contour with accuracy proportional to
            #the contour perimeter
            cnt_len = cv2.arcLength(contours[i], True)
            cnt = cv2.approxPolyDP(contours[i], 0.02 * cnt_len, True)
            #approx = cv2.approxPolyDP(contours[i],cv2.arcLength(contours[i],True)*0.02,True)

            #Skip small or non-convex objects
            if(abs(cv2.contourArea(contours[i]))<100 or not(cv2.isContourConvex(approx))):
                continue

            #ractangle
            if(len(approx) == 4):
                x,y,w,h = cv2.boundingRect(contours[i])
                #cv2.putText(frame,'RECT',(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)
                cropped = frame[y: y + h, x: x + w]
                current = str( time.time() )
                image_string = pytesseract.image_to_string(cropped, config='--psm 10 --oem 3')
                if pattern.match(image_string):
                    print(image_string)
                # cv2.imwrite( 'bilder/cropped_img_' + current + '_.jpg', cropped )
                # print("cropped_img wrote")

        #Display the resulting frame
        #out.write(frame)
        cv2.imshow('frame',frame)
        cv2.imshow('canny',canny)
        if cv2.waitKey(27) & 0xFF == ord('q') :
            break

#When everything done, release the capture
cap.release()
cv2.destroyAllWindows()

#
#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"


#from PIL import Image
#import pytesseract
#im = Image.open("bilder/cropped_img_1542273832.14374_.jpg")
#pytesseract.image_to_string(im, config='--psm 10 --oem 3')
