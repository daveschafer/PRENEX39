"""[Auflademodus Klasse]

Diese Klasse kümmert sich um die Lastgut Aufladung.
"""

###############
## Libraries ##
###############

#Logging
import log_helper
import time
logger = log_helper.create_Logger(False, "auflademodus")

#import MC Com
import helpers.mc_communication as mc_communication

###############
## Functions ##
###############

def run_auflademodus(cargo="undefined"):
    """[Auflademodus starten]

    Arguments:
        cargo {String} -- Cargo Parameter (default: {undefined})

    Returns:
        Boolean --  True, falls Lastgut aufgeladen
                    False, falls Lastgut nicht aufgeladen (proceed anyway?)
    """

    logger.warn("Auflademodus - proceed")

    #Send Aufladebefehl:
    mc_communication.uart_send_auflademodus()

    #Check for max. x seconds
    for cnt in range(0, 130):
        #MC: Get Status
        status = mc_communication.uart_get_mc_status()
        if(status == "aufgeladen"):
            logger.info("Lastgut aufgeladen! Fahre fort.")
            return True
        else:
            logger.info("Lastgut noch nicht aufgeladen")
            time.sleep(0.15) #3 millisekonds --> 150 miliseconds
    
 
    #Fals das Lastgut nach x Sekunden nicht aufgeladen ist -> False zurücksenden
    return False
