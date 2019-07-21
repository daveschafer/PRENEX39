####################################
## Libraries and global Vars #######
####################################

import http.client, urllib.request, urllib.parse, urllib.error, base64, time
import py_progbar as pbar
apiKey = "getYourOwnKey"


######################
###Read Image OCR#####
######################


def test_AZ_OCR(image_path = "../test.jpg"):
    # Set image_path to the local path of an image that you want to analyze.

    # Read the image into a byte array
    image_data = open(image_path, "rb")

    headers = {
        # Request headers
        #'Content-Type': 'application/json',
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': apiKey,
    }

    params = urllib.parse.urlencode({
        # Request parameters
            'language': 'unk',
            'detectOrientation': 'false'
    })

    try:
        print("Azure Call - OCR")
        conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v2.0/ocr?%s" % params, image_data, headers)
        response = conn.getresponse()
        #printing response
        data = response.read()
        print("OCR-API data: ", data)
        print("OCR-API headers: ")
        print(response.getheaders())
        conn.close()
    except Exception as e:
        print("Something went wrong")
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


########################################
###Read Image text Recog API (better)###
########################################


def test_AZ_textRecog(image_path = "../test.jpg"):
    # Set image_path to the local path of an image that you want to analyze.
    #image_path = "../test.jpg"

    # Read the image into a byte array
    image_data = open(image_path, "rb")

    ###

    headers = {
        # Request headers
        #'Content-Type': 'application/json',
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': apiKey,
    }

    params = urllib.parse.urlencode({
        # Request parameters
        'mode': 'Handwritten', #Printed or Handwritten
    })

    try:
        print("Azure Call - Text Recognize")
        conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        conn.request("POST", "/vision/v2.0/recognizeText?%s" % params, image_data, headers)
        response = conn.getresponse()
        #printing response
        print(response)
        data = response.read()
        print("Recognize-API data: ", data)
        print("Recognize-API headers Operation Location: ")
        OPLocation = response.getheader("Operation-Location")
        print(OPLocation)
        conn.close()
        return OPLocation
    except Exception as e:
        print("Something went wrong")
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

###########################
## Get Text Recog Result ##
###########################


def test_AZ_getResult_textRecog(OPLocation):
    headers = {
        # Request headers
        'Ocp-Apim-Subscription-Key': apiKey,
    }

    params = urllib.parse.urlencode({
    })

    try:
        print("Azure Call - Result (Text Recognize)")
        conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        conn.request("GET", "/vision/v2.0/textOperations/%s" % OPLocation,"", headers)
        response = conn.getresponse()
        data = response.read()
        print("Recogized Text Result: ", data)
        ####
        print("##################")
        print("recognition Result: ", response.getheader("recognitionResult"))
        conn.close()
    except Exception as e:
        print("Something went wrong")
        print("[Errno {0}] {1}".format(e.errno, e.strerror))


###############
## Run Recog ##
###############

if False:
    #upload img to azure
    opLocation = test_AZ_textRecog(image_path="../734_test.png")

    oploc_id = opLocation.split("/").pop()
    print("Oploc ID: ", oploc_id)

    #wait 5 seconds to process
    pbar.printProgressBar(0, 6, prefix = 'Progress:', suffix = 'Complete', length = 50)
    for i in range(6):
        time.sleep(1)
        pbar.printProgressBar(i + 1, 6, prefix = 'Progress:', suffix = 'Complete', length = 50)

    print("Getting Azure Recognize Text Result")
    #get result:
    test_AZ_getResult_textRecog(oploc_id)

##OCR Call
print("Plain OCR:")
test_AZ_OCR("../6_cropped.png")

