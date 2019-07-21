from picamera import PiCamera
from time import sleep
import io
import time
from PIL import Image

from datetime import datetime
t1 = datetime.now()

camera = PiCamera()
camera.resolution = (1280, 720)
#camera.framerate = 50
camera.shutter_speed = 1000
camera.iso = 1600
#camera.awb_mode = 'off'

#camera.start_preview()
sleep(2)

count = 100
# Set up 40 in-memory streams
outputs = [io.BytesIO() for i in range(100)]
start = time.time()
camera.capture_sequence(outputs, 'jpeg', use_video_port=True)
finish = time.time()
# How fast were we?
print('Captured 40 images at %.2ffps' % (100 / (finish - start)))
for test in outputs:
    count = count + 1
    test.seek(0)
    image = Image.open(test)
    image.save('/home/pi/Schreibtisch/test/fahrend_' + str(count) + '.jpg')

t2 = datetime.now()
delta = t2 - t1
delta.total_seconds()
print(delta)