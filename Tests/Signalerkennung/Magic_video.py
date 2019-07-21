
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
        #print(img.shape)
        L = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
        rcParams['figure.dpi']= 200
        #img = img[50: 150, 0:400] #infosignal
        #img = img[200:500, 0:300] #Haltesignal
        import glob

    #    for i in range (0,1000):
    #        start = time.time()
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
                if(rel > 1.5 and h > 20 and h < 50 and w > 20 and w < 47 ):
                    cv2.rectangle(img, (x - addh, y - addw), (x + w + addw, y + h + addh), (0, 255, 0), 1)
                    cv2.imshow("test", img)
                    cropped = img[y - addw:y + h + addh,x - addh:x + w + addw]
                    _retval, bin = cv2.threshold(cropped, 30, 255, cv2.THRESH_BINARY)

                    image_string = pytesseract.image_to_string(
                            cropped, lang='eng', config='-c tessedit_char_whitelist=0123456789 --oem 0 --psm 10')
                    print(image_string)

                    counter = counter + 1
                    number = number + 1 
                    current = str(time.time())
                    cv2.polylines(cropped, [contours[i]], False, (255,255,255), 2)
                    #cv2.imwrite(r'/new/numbers/file_' + str(number) +'_'+str(current)+ '.jpg', img)
                    cv2.imwrite(r'new/numbers/file_'+image_string+'_' + str(number) +'.jpg', cropped)
                    print("saved image" + str(number))
                    #plt.imshow(img, cmap='gray')
                    #plt.show()
                    cv2.imshow("img", img)
                    cv2.imshow("number", cv2.bitwise_not(cropped))

                    #imshow(cv2.bitwise_not(img[y - addh:y + h + addh,x - addw:x + w + addw]))
                    counter = counter + 1

        number = number + 1
        #filename = "%05d" % number 
        #cv2.imwrite('C:/data/pi/new/numbers/' + filename + '.jpg', img)
    #imshow(cont)
vidcap.release()
cv2.destroyAllWindows()
finish = time.time()
#print('%.5ffps' % ((finish - start)))

