"""[Runden Erkennung Klasse]

Diese Klasse kümmert sich um die Erkennung der Runden.
"""

###############
## Libraries ##
###############

import log_helper
logger = log_helper.create_Logger(False, "Rundenerkennung")

#import MC Com
import helpers.mc_communication as mc_communication

###############
## Functions ##
###############


#Main callable Function
def get_track(rundenerkennung_ticks_per_round=3000):
    logger.info("Get Track called (not implemented yet)")
    distance = get_ticks()
    #calulate track
    track = __translate_dist_to_track(distance, rundenerkennung_ticks_per_round)

    return track

#Direkte Kommunikation zu MC
def get_ticks():
    logger.info("Get Distance called")

    #MC: Get Ticks
    ticks = mc_communication.uart_get_ticks() 

    return ticks

def __translate_dist_to_track(distance, rundenerkennung_ticks_per_round):
    #irgend eine umrechnungsformel, tbd, TODO
    logger.warn("Umrechnung Ticks zu Tracks noch nicht validiert!!")
    return distance / rundenerkennung_ticks_per_round