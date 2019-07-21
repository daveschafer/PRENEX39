# Add Libraries
import time
import board
import busio
#install beforehand with sudo pip3 install adafruit-circuitpython-vl6180x
import adafruit_vl6180x

#add adafruit multiplexer library
import adafruit_tca9548a
#install pip3 install adafruit-circuitpython-tca9548a



# Create I2C bus. (careful with 2 TOFs)
i2c = busio.I2C(board.SCL, board.SDA)

# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)

sensor_tof1 = adafruit_vl6180x.VL6180X(tca[2])
sensor_tof2 = adafruit_vl6180x.VL6180X(tca[3])

# Create sensor instance.


# Main loop prints the range (and lux) every 0.25s
while True:
    # Read the range in millimeters and print it.
    range_mm_tof1 = sensor_tof1.range
    range_mm_tof2 = sensor_tof2.range
    print('Range TOF1: {0}mm'.format(range_mm_tof1))
    print('Range TOF2: {0}mm'.format(range_mm_tof2))

    
    # Delay for a second.
    time.sleep(0.250)

