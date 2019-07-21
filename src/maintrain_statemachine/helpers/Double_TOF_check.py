###############
## Libraries ##
###############

import time
import board
import busio

#Logging
import log_helper
logger = log_helper.create_Logger(False, "Double_TOF_check")

#install beforehand with sudo pip3 install adafruit-circuitpython-vl6180x
import adafruit_vl6180x

#add adafruit multiplexer library
import adafruit_tca9548a
#install pip3 install adafruit-circuitpython-tca9548a

#MC Com
try:
    import mc_communication as mc
except:
    import helpers.mc_communication as mc

###############
## Variables ##
###############

# Create I2C bus. (careful with 2 TOFs)
i2c = busio.I2C(board.SCL, board.SDA)

# Create the TCA9548A object and give it the I2C bus
tca = adafruit_tca9548a.TCA9548A(i2c)

#Create TOF Sensors 1 and 2 | Zuweisung wird spaeter noch ueberschrieben
sensor_tof1 = adafruit_vl6180x.VL6180X(tca[0])
sensor_tof2 = adafruit_vl6180x.VL6180X(tca[1])

###############
## Functions ##
###############

#Die TOFS spinnen am Anfang etwas, also muss man sie ca 5-10 sekunden "warm laufen" lassen
def calibrate_tofs():
    logger.info("Calibrating TOFS (ss)...")
    calcount=0
    while(calcount <= 10):
        range_mm_tof1 = sensor_tof1.range
        range_mm_tof2 = sensor_tof2.range
        time.sleep(0.01)
        calcount+=1

    logger.info("TOFS calibrated!")
    return
    

def tof1_distanzmessung():
    range_mm_tof1 = sensor_tof1.range
    print('Range TOF1: {0}mm'.format(range_mm_tof1))
    time.sleep(0.0020)

    return range_mm_tof1

def tof2_distanzmessung():
    range_mm_tof2 = sensor_tof2.range
    print('Range TOF2: {0}mm'.format(range_mm_tof2))
    time.sleep(0.0020)

    return range_mm_tof2


def combined_distanzmessung():
    # Read the range in millimeters and print it.
    range_mm_tof1 = sensor_tof1.range
    range_mm_tof2 = sensor_tof2.range

    #Durchschnitt berechnen:
    range_mean = ((range_mm_tof1 + range_mm_tof2) / 2)

    #print('Range TOF1: {0}mm'.format(range_mm_tof1))
    #print('Range TOF2: {0}mm'.format(range_mm_tof2))
    print('Range Mean: {0}mm'.format(range_mean))

    # Delay for a second.
    time.sleep(0.100)

    return range_mean

#Generic selection of TOF Methode
def tof_selector(tof_nr):
    if(tof_nr == 1):
        #Use TOF1
        return tof1_distanzmessung()
    elif(tof_nr == 2):
        #use tof 2
        return tof2_distanzmessung()
    elif(tof_nr == 3):
        #use combined tofs
        return combined_distanzmessung()

#TOF 1 = Gerade
#TOF 2 = Schraeg

def search_haltesignal(tof_measurement_timeout_millis=310, tof1_port=0, tof1_threshold_max_distance_mm=170, 
tof1_treshold_min_distance_mm=100, tof2_port=1, tof2_threshold_max_distance_mm=180, tof2_treshold_min_distance_mm=100):
    """Searches Object
    
    Keyword Arguments:
    
    Returns:
        Boolean - Erkannt oder nicht
    """
    logger.info("DoubleTOF Check called (100% validated)")

    #TOF Port zuweisung
    global sensor_tof1, sensor_tof2, adafruit_vl6180x, tca

    # sensor_tof1 = adafruit_vl6180x.VL6180X(tca[int(tof1_port)])
    # sensor_tof2 = adafruit_vl6180x.VL6180X(tca[int(tof2_port)])
    sensor_tof1 = adafruit_vl6180x.VL6180X(tca[0])
    sensor_tof2 = adafruit_vl6180x.VL6180X(tca[1])

    #Calibrating TOFS
    calibrate_tofs()


    ##########################################
    # Measure Distance till Treshold reached #
    ##########################################

    #Init with basic values
    measured_distance = 666
    measure_time = 0
    treshold_tof1_reached_counter=0 #success if 3 times under the treshold distance
    treshold_tof2_reached_counter=0 #success if 3 times under the treshold distance


    while(measure_time <= tof_measurement_timeout_millis):
        measured_distance_tof1 = tof1_distanzmessung()
        measured_distance_tof2 = tof2_distanzmessung()

        measure_time += 1

        #Check Distanz1 Tof1 (etwas erkannt?)
        if(measured_distance_tof1 <= tof1_threshold_max_distance_mm and treshold_tof1_reached_counter<3):
            treshold_tof1_reached_counter += 1
        elif(treshold_tof1_reached_counter>=3):
            logger.info("[TOF1]: Signal 3 mal unter Treshold, erkannt!")
            #STOP Train
            mc.uart_send_stop()
            break

        #Check Distanz2 Tof2 (etwas erkannt?)
        if(measured_distance_tof2 <= tof2_threshold_max_distance_mm and treshold_tof2_reached_counter<3):
            treshold_tof2_reached_counter += 1
        elif(treshold_tof2_reached_counter>=3):
            logger.info("[TOF2]: Signal 3 mal unter Treshold, erkannt!")
            #STOP Train
            mc.uart_send_stop()
            break         
        

    #########################################
    # Return result (erkannt oder Timeout?) #
    #########################################
    
    if(treshold_tof1_reached_counter>=3 or treshold_tof2_reached_counter>=3):
        logger.info("Haltesignal erkannt, Treshold erreicht, Stop the train!")
        #stop train Signal senden!
        return True
    else:
        logger.error("Timeout erreicht, Haltesignal Treshold nicht erreicht. Halte Zug an...")
        mc.uart_send_stop()
        return False