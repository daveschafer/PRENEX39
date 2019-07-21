"""[Transportgutsuche Klasse]

Diese Klasse kümmert sich um die Transportgutsuche.
"""

###############
## Libraries ##
###############

from helpers import ultraschallsensor_check as ultraschallsensor_check
#import MC Com
import helpers.mc_communication as mc_communication


#Logging
import log_helper
logger = log_helper.create_Logger(False, "transportgutsuche")


###############
## Functions ##
###############
 

def run_transportgutsuche(sonic_threshold_max_distance_cm, sonic_threshold_min_distance_cm, 
sonic_abtastrate, sonic_measurement_timeout_count):
    """[Transportgutsuche starten]

    Arguments:
        threshold_max_distance {int} -- Max Distanz zur Transportguterkennung (default: {10})

    Returns:
        Boolean --  True, falls Transportgut erkannt
                    False, falls nicht erkannt
    """
    logger.info("Transportgutsuche productive.")

    #Run check
    recognized = ultraschallsensor_check.search_object(sonic_threshold_max_distance_cm, 
    sonic_threshold_min_distance_cm, sonic_abtastrate, sonic_measurement_timeout_count)

    if(recognized):
        logger.info("Transportgut erkannt - Zug gestoppt!")
        transportgut_flag = True
    else:
        logger.warn("Transportgut nicht erkannt!")
        transportgut_flag = False


    return transportgut_flag
