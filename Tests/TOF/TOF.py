# Add Libraries
import time
import board
import busio
#install beforehand with sudo pip3 install adafruit-circuitpython-vl6180x
import adafruit_vl6180x

# Create I2C bus. (careful with 2 TOFs)
i2c = busio.I2C(board.SCL, board.SDA)

# Create sensor instance.
sensor = adafruit_vl6180x.VL6180X(i2c)

# Main loop prints the range (and lux) every 0.25s
while True:
    # Read the range in millimeters and print it.
    range_mm = sensor.range
    print('Range: {0}mm'.format(range_mm))
        # Read the light, note this requires specifying a gain value:
            # - adafruit_vl6180x.ALS_GAIN_1 = 1x
            # - adafruit_vl6180x.ALS_GAIN_1_25 = 1.25x
            # - adafruit_vl6180x.ALS_GAIN_1_67 = 1.67x
            # - adafruit_vl6180x.ALS_GAIN_2_5 = 2.5x
            # - adafruit_vl6180x.ALS_GAIN_5 = 5x
            # - adafruit_vl6180x.ALS_GAIN_10 = 10x
            # - adafruit_vl6180x.ALS_GAIN_20 = 20x
            # - adafruit_vl6180x.ALS_GAIN_40 = 40x
    #light_lux = sensor.read_lux(adafruit_vl6180x.ALS_GAIN_1)
    #print('Light (1x gain): {0}lux'.format(light_lux))
    
    # Delay for a second.
    time.sleep(0.250)