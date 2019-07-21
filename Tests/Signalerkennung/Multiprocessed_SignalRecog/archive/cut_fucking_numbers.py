yfrom pytesseract import image_to_string
import numpy as np
import cv2

import warnings
warnings.filterwarnings('ignore')
import glob



#img = cv2.imread('C:/data/pi/new/pictures/fahrend_klein_2019-05-10 09_27_42.782458.jpg')
#img = cv2.imread('C:/data/pi/new/pictures/fahrend_klein_2019-05-10 09_27_42.242215.jpg')
img = cv2.imread('C:/Users/ursfe/HSLU/PREN2/pictures/320240_20190519_165947_984838.jpg')

L = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])

#def detect(image):
#        scaled_image = cv2.resize(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),(28,28))
#        scaled_image = scaled_image.reshape(1, 28, 28, 1)
#        pred = model.predict(scaled_image)
#        predicted_digit = pred[0].tolist().index(max(pred[0].tolist()))
#        return predicted_digit

count_number = 0
template_check = [] 

#for filepath in glob.iglob('C:/Users/ursfe/HSLU/PREN2/contours/*.jpg'):
#    count_number = count_number + 1
#    img = cv2.imread(filepath)
#    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#    binary = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)[1]
#    binary = cv2.resize(binary,(50,50))
#    template_check.append(binary) 
#    cv2.imshow('img',binary)
#    cv2.waitKey(500)

def compare_template(picture):
    picture = cv2.resize(picture,(50,50))
    res_max = 100
    res_act = 100
    res_number = -1
    for i in range(0,9):
        res = cv2.matchTemplate(picture,template_check[i],cv2.TM_SQDIFF_NORMED) 
        if(res < res_max):
            res_number = i + 1
            res_act = res
            res_max = res
    return res_number
       
def tesseract(image):
    return image_to_string(image, lang='eng', config='--psm 6')
    
counter = 0
############
for filepath in glob.iglob('C:/data/pi/new/pics_new/*.jpg'):
#for filepath in glob.iglob('C:/data/pi/new/pics_new/320240_20190521_222119_999708.jpg'):
    img = cv2.imread(filepath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    filtered = cv2.filter2D(gray, -1, L)
    cont = img.copy()
    canny = cv2.Canny(gray,30,250)
    
    # nur für Urs
    test = cv2.threshold(filtered, 30, 255, cv2.THRESH_BINARY)[1]
    
    im2, contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    new_contour = []
    counter += 1
    hm = 50
    get_number = 0

    for i in range(0,len(contours)):
        epsilon = 0.1 * cv2.arcLength(contours[i], True)
        approx = cv2.approxPolyDP(contours[i], epsilon, closed=True)

        if (abs(cv2.contourArea(contours[i])) > 0):
        #if(abs(cv2.contourArea(contours[i])) > 0 and hierarchy[0][i][0] > -1):
            
            #xm, ym, wm, hm = cv2.boundingRect(contours[hierarchy[0][i][0]])
            if((hm) > 40):
                x,y,w,h = cv2.boundingRect(contours[i])
                rel = h / w
                addh = int(h / 8)
                addw = int(w / 8)
                if(rel > 1.5 and h > 20 and w > 10 and w < 40 and h < 55 and y > 5 and (y + h) < 235 and x < 220):
                #if(rel > 1.3):
                    #cv2.polylines(cont, [contours[i]], False, (0,255,0), 2)
                    number = cv2.threshold(gray[y - addh:y + h + addh,x - addw:x + w + addw], 30, 255, cv2.THRESH_BINARY)[1]
                    try:
                        if number[0][0].all() == 0:
                            number = cv2.bitwise_not(number)
                        
                        nonzeroes = np.count_nonzero(number)/np.prod(number.shape)
                        if number[0][0].all() != 0 and number[:][0].all() and nonzeroes > 0.65 and nonzeroes < 0.88:

                           cv2.rectangle(cont, (x - addw, y - addh), (x + w + addw, y + h + addh), (0, 0, 255), 1)
                           get_number = tesseract(number)
                           
                           cv2.imshow('number',cv2.resize(number,None,fx=5,fy=5))    
                           cv2.putText(cont, "h={}  w={} c={}".format(h, w, cv2.isContourConvex(contours[i])),
                                        (x + w + addw + 5, y), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
                           cv2.putText(cont, "r={:.2f} a={} n={}".format(rel, abs(cv2.contourArea(contours[i])), i),
                                        (x + w + addw + 5, y + 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
                           cv2.putText(cont, "x={} y={}".format(x, y),
                                        (x + w + addw + 5, y + 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255), 1)
                           cv2.putText(cont, "nuymat(get_number, len(approx)),
                                        (x + w + addw + 5, y + 45), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1)
                           print(str(get_number) + " " + str(np.count_nonzero(number)/np.prod(number.shape)) + " " + str(np.count_nonzero(number)) + " " + str(np.prod(number.shape)))
                               
                    except:
                        count = 1 

    cv2.imshow('canny',canny)
    cv2.imshow('cont',cont)
    cv2.putText(filtered, "number={}".format(counter),
                (10, 10), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1)
    cv2.putText(filtered, "{}".format(filepath[30:None]),
                (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0), 1)
    cv2.imshow('filtered',filtered)
#    cv2.destroyAllWindows()
    try:
        if int(get_number) > 0:
            cv2.waitKey(1000)  
    except:
        print("not a number")    
    
