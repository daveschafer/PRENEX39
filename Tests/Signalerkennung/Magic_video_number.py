import math
import numpy as np
import sys
sys.path.append('/usr/local/python/cv2/python-3.5/')
import cv2
import matplotlib as mpl
from matplotlib.pyplot import *
import matplotlib.pyplot as plt
import pytesseract

#from pytesseract import image_to_string

vidcap = cv2.VideoCapture('1556872376191_video.mp4')

count = 0
number = 0
while True:
    success,img = vidcap.read()

    if success == True:
       L = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
       rcParams['figure.dpi']= 200
       for i in range (0,1):
        start = time.time()
        gray = cv2.cvtColor(img[:][:][::], cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray,120,250)
        contours, hierarchy = cv2.findContours(cv2.filter2D(canny, -1, L), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        counter = 0
        new_contour = []
        for i in range(0,len(contours)):
            epsilon = 0.1*cv2.arcLength(contours[i],True)
            approx = cv2.approxPolyDP(contours[i], epsilon, closed=True)
            if(abs(cv2.contourArea(contours[i])) > 10 and len(approx) == 2 and not(cv2.isContourConvex(approx))):
                new_contour.append(contours[i])
                x,y,w,h = cv2.boundingRect(contours[i])
                rel = h / w
                addh = int(h / 8)
                addw = int(w / 4)
                print()
                if(rel > 1.5 and h > 20 and h < 50 and w > 20 and w < 50 and y > 0 and x > 0):
                    cont = img.copy()
                    #cv2.rectangle(cont, (x - addh, y - addw), (x + w + addw, y + h + addh), (0, 255, 0), 1)
                    #cv2.imshow("cont", cont)
                    #cv2.waitKey(0)
                    cv2.fillPoly(cont, [contours[i]], (255,255,255))
                    cropped =cont[y - addw:y + h + addh,x - addh:x + w + addw]
                    image_string = pytesseract.image_to_string(cv2.bitwise_not(cropped), lang='eng', config='-c tessedit_char_whitelist=0123456789 --oem 0 --psm 10')
                    print(image_string)
                    #imshow(cv2.bitwise_not(cont[y - addh:y + h + addh,x - addw:x + w + addw]))
                    #cv2.imshow("bitwise", cv2.bitwise_not(cont[y - addh:y + h + addh,x - addw:x + w + addw]))
                    #cv2.waitKey(0)
                    cv2.imwrite(r'new/numbers/file_'+str(start)+'_'+image_string+'.jpg', cropped)
                    #cv2.imwrite(r'new/numbers/'+image_string+'/file_'+str(counter)+'_'+image_string+'.jpg', cropped)
                    counter = counter + 1



    finish = time.time()
    #imshow(cont)
vidcap.release()
cv2.destroyAllWindows()
finish = time.time()
#print('%.5ffps' % ((finish - start)))

