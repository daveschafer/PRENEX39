#testklasse zur OCR Erkennung von Nummern via Azure

####################################

########### Python 3.2 #############
import http.client, urllib.request, urllib.parse, urllib.error, base64

###Read Image

# Set image_path to the local path of an image that you want to analyze.
image_path = "../6_multitest.jpg"

# Read the image into a byte array
image_data = open(image_path, "rb").read()


headers = {
    # Request headers
    #'Content-Type': 'application/json',
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': 'getYourOwnKey',
}

params = urllib.parse.urlencode({
    # Request parameters
    'language': 'de',
    'detectOrientation ': 'true',
})

try:
    print("Uploading to Azure")
    conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/ocr?%s" % params, image_data, headers)
    response = conn.getresponse()
    data = response.read()
    print(data)
    conn.close()
except Exception as e:
    print("Something went wrong")
    print("[Errno {0}] {1}".format(e.errno, e.strerror))