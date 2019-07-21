from pytesseract import image_to_string
import numpy as np
import cv2
import warnings

warnings.filterwarnings('ignore')
import glob

count_pictures = 0
count_number = 0
count_number_temp = 0
count_not_a_number = 0
template_check = []

startsignal = cv2.imread('template_start/startsignal.png') # Path to startsignal 
startsignal = cv2.cvtColor(startsignal, cv2.COLOR_BGR2HSV)
histr = cv2.calcHist([startsignal], [0, 1], None, [45, 32], [0, 180, 0, 256])
cv2.normalize(histr, histr, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)

count_signal = 0
count_picture = 0


def sliding_window(image, window_size, step_size=1):
    for y in range(0, image.shape[0], step_size):
        for x in range(0, image.shape[1], step_size):
            yield (x, y, image[y:y + window_size[1], x:x + window_size[0]])


# change path to test pictures
for filepath in sorted(glob.iglob(
        '/Users/tluscre1/Documents/Studium.Local/PREN/repo/resources/pictures/20190622_lights_with_lens/startsignal/*.jpg')):
    count_picture = count_picture + 1

    # Captures the live stream frame-by-frame 
    img_ganz = cv2.imread(filepath)

    img = cv2.imread(filepath)[0:110, 0:160]
    image_total = img.copy()

    """
        Testing frame for start signal
    """
    cv2.rectangle(img_ganz, (0, 0), (160, 110), (0, 255, 0), 1)

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
    cv2.imshow('frame', img_ganz)
    cv2.imshow('mask', mask)
    cv2.imshow('res', res)

    # print(filepath  + " " + str(np.count_nonzero(mask)))

    print(str(count_picture) + " " + str(np.count_nonzero(mask)))
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

    # jump if mask does not match
    if np.count_nonzero(mask) < 350:
        continue

    signal_detected = False

    for i in range(0, 70, 5):
        if signal_detected:
            break
        for j in range(0, 120, 5):
            if mask[i, j] == 0:
                continue
            print("found;x=(" + str(j) + "),y=(" + str(i) + ")")
            sub_image = hsv[i:i + 40, j:j + 40]
            window_hist = cv2.calcHist([sub_image], [0, 1], None, [45, 32], [0, 180, 0, 256])
            cv2.normalize(window_hist, window_hist, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
            dist_bhatt = cv2.compareHist(histr, window_hist, cv2.HISTCMP_BHATTACHARYYA)
            if dist_bhatt < 1:
                print("x=" + str(j) + " y=" + str(i) + " dist_bhatt=" + str(dist_bhatt) + " " + str(mask[i, j]))
                if (dist_bhatt < 0.98):
                    cv2.rectangle(image_total, (j, i), (j + 40, i + 40), (0, 255, 0), 1)
                    signal_detected = True
                    print(filepath + " SIGNAL FOUND " + str(np.count_nonzero(mask)))
                    count_signal += 1
                    cv2.putText(image_total, str(np.count_nonzero(mask)), (110, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (255, 255, 0), 1)
                    cv2.imshow('total', image_total)
                    cv2.waitKey(0)
                    break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print("found signals: " + str(count_signal))

# cv2.destroyAllWindows()
