{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "press q to exit\n",
      "8\n",
      "8\n",
      "8\n",
      "8\n"
     ]
    }
   ],
   "source": [
    "import math\n",
    "import numpy as np\n",
    "import cv2\n",
    "import time\n",
    "import subprocess\n",
    "from PIL import Image\n",
    "import pytesseract\n",
    "import re\n",
    "\n",
    "pattern = re.compile(\"^(\\d)$\")\n",
    "#dictionary of all contours\n",
    "contours = {}\n",
    "#array of edges of polygon\n",
    "approx = []\n",
    "#scale of the text\n",
    "scale = 2\n",
    "#camera\n",
    "cap = cv2.VideoCapture(0)\n",
    "cap.set(cv2.CAP_PROP_FPS, 40)\n",
    "cap.set(cv2.CAP_PROP_FRAME_WIDTH,320)\n",
    "cap.set(cv2.CAP_PROP_FRAME_HEIGHT,240)\n",
    "cap.set(cv2.CAP_PROP_EXPOSURE, 0.05); \n",
    "\n",
    "\n",
    "#stop programm\n",
    "print(\"press q to exit\")\n",
    "\n",
    "#calculate angle\n",
    "def angle(pt1,pt2,pt0):\n",
    "    dx1 = pt1[0][0] - pt0[0][0]\n",
    "    dy1 = pt1[0][1] - pt0[0][1]\n",
    "    dx2 = pt2[0][0] - pt0[0][0]\n",
    "    dy2 = pt2[0][1] - pt0[0][1]\n",
    "    return float((dx1*dx2 + dy1*dy2))/math.sqrt(float((dx1*dx1 + dy1*dy1))*(dx2*dx2 + dy2*dy2) + 1e-10)\n",
    "\n",
    "while(cap.isOpened()):\n",
    "    #Capture frame-by-frame\n",
    "    ret, frame = cap.read()\n",
    "    if ret==True:\n",
    "        #grayscale\n",
    "        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)\n",
    "        #Canny\n",
    "        canny = cv2.Canny(frame,80,240,3)\n",
    "\n",
    "        #contours\n",
    "        canny2, contours, hierarchy = cv2.findContours(canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)\n",
    "        for i in range(0,len(contours)):\n",
    "            #approximate the contour with accuracy proportional to\n",
    "            #the contour perimeter\n",
    "            approx = cv2.approxPolyDP(contours[i],cv2.arcLength(contours[i],True)*0.02,True)\n",
    "\n",
    "            #Skip small or non-convex objects\n",
    "            if(abs(cv2.contourArea(contours[i]))<100 or not(cv2.isContourConvex(approx))):\n",
    "                continue\n",
    "\n",
    "            #ractangle\n",
    "            if(len(approx) == 4):\n",
    "                x,y,w,h = cv2.boundingRect(contours[i])\n",
    "                #cv2.putText(frame,'RECT',(x,y),cv2.FONT_HERSHEY_SIMPLEX,scale,(255,255,255),2,cv2.LINE_AA)\n",
    "                cropped = frame[y: y + h, x: x + w]\n",
    "                current = str( time.time() )\n",
    "                image_string = pytesseract.image_to_string(cropped, config='--psm 10 --oem 3')\n",
    "                if pattern.match(image_string):\n",
    "                    print(image_string)\n",
    "                # cv2.imwrite( 'bilder/cropped_img_' + current + '_.jpg', cropped )\n",
    "                # print(\"cropped_img wrote\")\n",
    "\n",
    "        #Display the resulting frame\n",
    "        #out.write(frame)\n",
    "        cv2.imshow('frame',frame)\n",
    "        cv2.imshow('canny',canny)\n",
    "        if cv2.waitKey(27) & 0xFF == ord('q') :\n",
    "            break\n",
    "\n",
    "#When everything done, release the capture\n",
    "cap.release()\n",
    "cv2.destroyAllWindows()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [],
   "source": [
    "pytesseract.pytesseract.tesseract_cmd = r\"C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'8'"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "from PIL import Image\n",
    "import pytesseract\n",
    "im = Image.open(\"bilder/cropped_img_1542273832.14374_.jpg\")\n",
    "pytesseract.image_to_string(im, config='--psm 10 --oem 3')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
