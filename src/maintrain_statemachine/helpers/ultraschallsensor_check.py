###############
## Libraries ##
###############

import RPi.GPIO as GPIO
import time

try:
    import mc_communication as mc
except:
    import helpers.mc_communication as mc
#Logging
import log_helper
logger = log_helper.create_Logger(False, "ultraschallsensor_check")
 
###############
## Variables ##
###############
 
#GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
#GPIO Pins zuweisen
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
###############
## Functions ##
###############
 

def distanzmessung():
    # setze Trigger auf HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # setze Trigger nach 0.01ms aus LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartZeit = time.time()
    StopZeit = time.time()
 
    # speichere Startzeit
    while GPIO.input(GPIO_ECHO) == 0:
        StartZeit = time.time()
 
    # speichere Ankunftszeit
    while GPIO.input(GPIO_ECHO) == 1:
        StopZeit = time.time()
 
    # Zeit Differenz zwischen Start und Ankunft
    TimeElapsed = StopZeit - StartZeit
    # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
    # und durch 2 teilen, da hin und zurueck
    distanz = (TimeElapsed * 34300) / 2
 
    return distanz

 
def search_object(sonic_threshold_max_distance_cm=11, sonic_threshold_min_distance_cm=5, 
sonic_abtastrate=0.01, sonic_measurement_timeout_count=800):
    """Searches Object
    
    Keyword Arguments:
        threshold_max_distance {int} -- Maximale Distanz ab der Objekt als erkannt gilt(default: {10})
    
    Returns:
        Boolean - Erkannt oder nicht
    """
    lastgut_count = 0 

    for cnt in range(0, sonic_measurement_timeout_count):
            abstand = distanzmessung()
            print ("Gemessene Entfernung = %.1f cm" % abstand)
            time.sleep(sonic_abtastrate) 
            if(abstand <= sonic_threshold_max_distance_cm and abstand >= sonic_threshold_min_distance_cm):
                if(lastgut_count>=1): #Lastgut 3 mal erkennen!
                    logger.info("Lastgut definitiv erkannt!")
                    #Timeout Parameter - optimale Kran position
                    time.sleep(0.018) #0.15s pause
                    #MC Stop Train
                    mc.uart_send_stop()
                    return True
                else:
                    #print("Lastgut potentiell erkannt, count %i", lastgut_count)
                    lastgut_count += 1
    #return false if not recognized within 80 runs
    return False
