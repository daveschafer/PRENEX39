#Debug Version Team 39

import time
from pytesseract import image_to_string
import numpy as np
from keras.models import load_model
import warnings
import os

#Use Filepath and not camera
from PIL import Image
import glob

try:
    import cv2
except ImportError:
    # we running on Ors Pi
    import sys

    sys.path.append('/usr/local/python/cv2/python-3.5/')
    import cv2

# Multiprocessing
import multiprocessing
from multiprocessing import Pool
import glob

warnings.filterwarnings('ignore')

try:
    from picamera.array import PiRGBArray
    from picamera import PiCamera
except ImportError:
    # We are not on a raspberry pi
    from unittest import mock

    PiRGBArray = mock.MagicMock()
    PiCamera = mock.MagicMock()

template_check = []
try:
    model = load_model("models/numbers.h5")
except:
    model = load_model("/home/pi/PREN/maintrain_statemachine/signalerkennung/models/numbers.h5")


# Global Variables
count_pictures = 0
count_number = 0
count_number_temp = 0
count_not_a_number = 0
template_check = []
#startsignal = cv2.imread('template_start/startsignal.png')
startsignal = cv2.imread('/home/pi/PREN/maintrain_statemachine/signalerkennung/template_start/startsignal.png')

startsignal = cv2.cvtColor(startsignal, cv2.COLOR_BGR2HSV)
start_signal_hist = cv2.calcHist([startsignal], [0, 1], None, [45, 32], [0, 180, 0, 256]) #TODO finetuning, ist auf remo abgestimmt


# tesseract
def detect_with_tesseract(image):
    return image_to_string(image, lang='digits', config='--psm 10')


# model
def detect_with_model(image):
    image = cv2.resize(image, (28, 28))
    vectorized_image = image.reshape(1, 28, 28, 1)
    predictions = model.predict(vectorized_image)
    predicted_digit = np.argmax(predictions)
    return predicted_digit


# template matching
# -> init
def init_template_matching():
    print("[INFO] init some templates")
    for filepath in sorted(glob.iglob('templates_slow_speed/*.jpeg')):
        img = cv2.imread(filepath)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        binary = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)[1]
        template_check.append(binary)


# detect with template matching
def detect_with_template_matching(number_binary):
    # blur and resize
    number_blured = cv2.blur(number_binary, (3, 3))
    number_resized = cv2.resize(number_blured, (20, 40))

    # init template matching
    number_template_matching = -1  # wrong number
    result_min = 100
    for i in range(0, 10):

        # compare number with template
        result = cv2.matchTemplate(number_resized, template_check[i], cv2.TM_SQDIFF_NORMED)
        if (result < result_min):
            number_template_matching = i
            result_min = result

    # identify as "not a number"
    if result_min > 0.1:
        number_template_matching = 0

    return number_template_matching


def init_template_start_signal():
    print("[INFO] init start signal template")
    template_start_signal = cv2.imread('teamplate_start/startsignal.png')
    template_start_signal = cv2.cvtColor(template_start_signal, cv2.COLOR_BGR2HSV)
    global start_signal_hist
    start_signal_hist = cv2.calcHist([template_start_signal], [0, 1], None, [45, 32], [0, 180, 0, 256])
    cv2.normalize(start_signal_hist, start_signal_hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)


# check which condition does not apply
def check(what, value):
    # print("[INFO] skipped due to {} - value = {}".format(what, value))
    return True


# number validator from urs - does we need that?
def check_guesel(number):
    contours, hierarchy = cv2.findContours(number, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 1:
        return False
    else:
        return True

# Detect most frequent Number matches in an array
def count_occurences(np_array, frequency_treshold=2):
    counts = np.bincount(np_array)
    if(np.max(counts) >= frequency_treshold ):
        #Get Most Frequent Number
        freq_number = np.argmax(counts)
        if (freq_number==0):
            print("0 detected")
            return 0
        print("[Info] number '%s' detected '%s' times - definitive match!"% (freq_number,frequency_treshold))
        return freq_number
    else:
        return 0 #return 0 for no match

#worker method for startsignal
def startsignal_detection(img=0):
    # Captures the live stream frame-by-frame
    # Converts images from BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Here we are defining range of bluecolor in HSV
    # This creates a mask of blue coloured
    # objects found in the frame.
    lower_blue = np.array([110, 180, 0])
    upper_blue = np.array([130, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # The bitwise and of the frame and mask is done so
    # that only the blue coloured objects are highlighted
    # and stored in res
    res = cv2.bitwise_and(img, img, mask=mask)

    # jump if mask does not match
    if np.count_nonzero(mask) < 500:
        pass

    signal_detected = False

    for i in range(0, 70, 8):
        if signal_detected:
            break
        for j in range(0, 120, 12):
            if mask[i, j] == 0:
                continue
            sub_image = hsv[i:i + 40, j:j + 40]
            hist_image = cv2.calcHist([sub_image], [0, 1], None, [45, 32], [0, 180, 0, 256])
            cv2.normalize(hist_image, hist_image, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
            global start_signal_hist
            dist_bhatt = cv2.compareHist(start_signal_hist, hist_image, cv2.HISTCMP_BHATTACHARYYA)

            if dist_bhatt < 1:
                # print("[INFO] " + str(i) + " " + str(j) + " " + str(dist_bhatt) + " " + str(mask[j, i]) + " " + str(mask[i, j]))
                # threshold for histogram compare
                if (dist_bhatt < 0.95): #TODO, abgestimmt auf REMO
                    signal_detected = True
                    print("[INFO] START-SIGNAL FOUND ")
                    return signal_detected
                    break


# Worker method for info and haltesignal
def process_frame_worker(img=0, counter=0, modeselector="model"):
    """[Processes Frames (Cutting, Detecting Contours, Recognizing Image)]
    
    Keyword Arguments:
        img {int} -- Img from Camera or Filesystem (default: {0})
        counter {int} -- Counter, Identifies Frame/Img (default: {0})
        modeselector {str} -- Modes for Img Recognition: 'model','template','tesseract' (default: {"model"})
    """
    # gray and canny
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 50, 230)
    # find contours
    contours, hierarchy = cv2.findContours(
        canny, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    for i in range(0, len(contours)):
        # find position and size of contour
        x, y, w, h = cv2.boundingRect(contours[i])

        # remove too small and too big
        if w <= 6 or w >= 80:
            if check("width", w):
                continue
        if h <= 20 or h >= 80:
            if check("height", h):
                continue

        # calculate relation between height and width
        rel = h / w

        # skip contour if too small too big (relation)
        if rel < 1.3 or rel > 4:
            if check("rel", rel):
                continue

        # adding space to contours
        addh = int(h / 16)
        addw = int(w / 6)
        if addw < 1:
            addw = 1

        # coordinates for bounding rectangle
        top_border = y - addh
        bottom_border = y + h + addh
        left_border = x - addw
        right_border = x + w + addw

        if top_border < 0:
            if check("top_border", top_border):
                continue
        if left_border < 0:
            if check("left_border", left_border):
                continue
        if bottom_border > 240:
            if check("bottom border", bottom_border):
                continue
        if np.amax(gray[top_border:bottom_border, left_border:right_border]) > 150:
            if check("max", np.amax(gray[top_border:bottom_border, left_border:right_border])):
                continue
        #cv2.imshow('gray', gray)
        # cut_number and make it binary
        number = cv2.threshold(gray[top_border:bottom_border, left_border:right_border], 35, 255, cv2.THRESH_BINARY)[1]

        # calculate right and bottom row of array
        bottom_row, right_col = number.shape
        bottom_row -= 1
        right_col -= 1

        # invert if signal is black
        if number[bottom_row, :].all() == 0:
            number = cv2.bitwise_not(number)
            # print("[DEBUG] Image is black")

        # check if bottom row and right col complete white
        if not number[:, right_col].all() != 0:
            if check("right_col not white", right_col):
                continue
        if not number[0, :].all() != 0:
            if check("top_row not white", 0):
                continue
        if not number[:, 0].all() != 0:
            if check("left_col not white", left_border):
                continue
        if not number[bottom_row, :].all() != 0:
            if check("bottom_row not white", bottom_row):
                continue

        # calculate relation of black and white
        nonzeroes = np.count_nonzero(number) / np.prod(number.shape)
        if nonzeroes < 0.6 and nonzeroes > 0.9:
            if check("bottom_row not white", nonzeroes):
                continue

        # calculations for  model
        addh_model = int(h / 5)
        addw_model = int(w / 2)
        top_border_model = y - addh_model
        bottom_border_model = y + h + addh_model
        left_border_model = x - addw_model
        right_border_model = x + w + addw_model

        if y >= 120:
            info = "stop"
        if y < 120:
            info = "info"

        ##############################
        # Select Recog Mode          #
        #                            #
        # Model, Template, Tesseract #
        ##############################

        if modeselector=="template":
            recognized_number = detect_with_template_matching(number)

        if modeselector=="model":
            recognized_number = detect_with_model(
                gray[max(0, top_border_model):bottom_border_model, max(0, left_border_model):right_border_model])

        if modeselector=="tesseract":
            recognized_number = detect_with_tesseract(number)
            #check for empty string
            if not recognized_number:
                recognized_number = 0 #just assign 0 for garbage


        # Save Image to Filesystem for Debugging ## !!!
        #cv2.rectangle(img, (x,y), (x+w+addw_model, y+h+addh_model), (255,0,0), 1)
        #cv2.imwrite('rectangle_'+str(counter)+"_"+str(current)+".jpg", img)

        #Print if it is a number (0=garbage)
        if int(recognized_number) > 0:
            print("signal erkannt")
            print(recognized_number)
            return recognized_number

        if int(recognized_number) > 0:
            break

#Frame Loop Methode for info/haltesignal detection
def signal_detection(camera, signalmode="info", infosig_nr=0): #returns number with treshold
    #Sanitizing signalmode...
    if not(signalmode=="info" or "halt"):
        print("WRONG SIGNALMODE!")
        return

    print("[INFO] Signal Detection(%s) started"%signalmode)

    frame_counter = 0

    recognized_number_array = np.array([0]) #Make list with one element
    most_frequent_number = 0

    for frame in camera.stream():
        # NEVER pass the frame, always pass the converted img
        if (signalmode=="info"):
            #1: höhe x, 2: breite y
            frame_capture = frame[:110, :260]
        elif (signalmode=="halt"):
            frame_capture = frame[135:, :225]


        #1. Check for number
        recognized_number = process_frame_worker(frame_capture, frame_counter)
        #2. Add recognized number to array 
        #if not((recognized_number == 0) or (recognized_number is None)): #Nur hinzufügen wenn etwas erkannt wurde
        #    recognized_number_array = np.append(recognized_number_array,recognized_number)

        #3. Check if a number was detected 'x' times -> definitive recognition treshold
        #most_frequent_number = count_occurences(np_array=recognized_number_array, frequency_treshold=1)
        if not((recognized_number == 0) or (recognized_number is None)):
            most_frequent_number = recognized_number
        if not (most_frequent_number == 0):
            camera.reset()
            if(signalmode=="info"):
                print("[IMPORTANT] Infosignal erkannt!")
                return most_frequent_number #Return number and end function if signal detected 'x' times, else loop continues
            elif(signalmode=="halt"):
                #If Haltemodus --> Compare haltesignal to infosignal
                if (most_frequent_number == infosig_nr):
                    print("[IMPORTANT] Haltesignal '%s' Match erkannt!"%infosig_nr)
                    return True
                else:
                    print("[Debug] Info(%s)<->Halte(%s) do not match"%(infosig_nr, most_frequent_number))
                    recognized_number_array = np.array([0]) #Nicht das korrekte Haltesignal -> Empty Array
            else:
                print("wrongmode")
      
        #start_signal_detection(frame)
        frame_counter = frame_counter + 1

        # Truncate Cam (else buffer overflows?)
        camera.reset()


#Frame Loop Methode for Startsignal detection
def start_startsignal_detection(camera):
    print("[INFO] STARTSIGNAL Detection started")

    frame_counter = 0

    for frame in camera.stream():
            frame_capture = frame[:100, :260]
            recognized = startsignal_detection(frame_capture)

            frame_counter += 1
            if (recognized):
                camera.reset()
                return True #TODO Aktion auslösen (?)
        
            # Truncate Cam (else buffer overflows?)
            camera.reset()


#Reads Images from a Filesystem Path and processes them [debug]
def detect_from_filesystem(path, printfilename=False, modeselector="model"):
    print("[INFO] detect_from_filesystem() started")

    # init templates
    init_template_matching()
    init_template_start_signal()

    frame_counter = 0

    #image_list = []
    for filename in glob.glob('%s/*.jpg' % path): #assuming jpg
        img=cv2.imread(filename)

        #Pass to detection
        if printfilename:
            print("Filename: '%s':"%filename)

        process_frame_worker(img, frame_counter, modeselector) #select mode with modeselector
        time.sleep(0.001)
        frame_counter += 1
        print("-"*20)
        #enter to continue
        input("press enter to continue")
