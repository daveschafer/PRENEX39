
"""[Praezises Halten Klasse]

Diese Klasse kümmert sich um das Präzise halten des Zuges zum Haltesignal.
"""

###############
## Libraries ##
###############

import log_helper
logger = log_helper.create_Logger(False, "Praezises halten")

import helpers.Double_TOF_check as Double_TOF_check

#import MC Com
import helpers.mc_communication as mc_communication



###############
## Functions ##
###############

def run_haltesignal_precise_stop(tof_measurement_timeout_millis, tof1_port, tof1_threshold_max_distance_mm, 
tof1_treshold_min_distance_mm, tof2_port, tof2_threshold_max_distance_mm, tof2_treshold_min_distance_mm):
    """[Praezises halten starten]

    TOF1 = Schaut Gerade
    TOF2 = Schaut Schräg

    Arguments:

    Returns:
        Boolean --  True, falls angehalten.
    """

    logger.warn("Praezises Halten not productive yet (90%) - not tested")

    # Temporaer deaktiviert
    # recognized = Double_TOF_check.search_haltesignal(tof_measurement_timeout_millis=tof_measurement_timeout_millis, 
    # tof1_port=tof1_port, tof1_threshold_max_distance_mm=tof1_threshold_max_distance_mm, 
    # tof1_treshold_min_distance_mm=tof1_treshold_min_distance_mm, tof2_port=tof2_port, 
    # tof2_threshold_max_distance_mm=tof2_threshold_max_distance_mm, tof2_treshold_min_distance_mm=tof2_treshold_min_distance_mm)

    recognized = Double_TOF_check.search_haltesignal()

    if(recognized):
        logger.info("Haltesignal erkannt! Train Stopped!")
        praezises_halten_flag = True
    else:
        logger.warn("Haltesignal nicht erkannt, Train stopped!")
        praezises_halten_flag = False


    return praezises_halten_flag 
