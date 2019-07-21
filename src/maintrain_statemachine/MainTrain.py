#####################
## Library Imports ##
#####################

#Import System Libraries
import sys
import time

#Import StateMachine Base
from StateMachine import StateMachine

#Logger
import log_helper
logger = log_helper.create_Logger(False, "MainTrain")

#Import Zug-Module / Aufgaben Klassen
import transportgutsuche
import healthcheck
import praezises_halten
#import haltesignal_erkennung
#import infosignal_erkennung
import runden_erkennung
import auflademodus
import helpers.mc_communication as mc_communication

#Import Threading classes
import threading
from multiprocessing.pool import ThreadPool
pool = ThreadPool(processes=4)

# Import Voice Out
#import modules.soundoutput as sound
import modules.beep as beep

#Signalerkennung Imports (dauert lange wegen Tensorflow)
import signalerkennung.initiator as initiator
import signalerkennung.number_detector as number_detector


###########################
##   Import Config       ##
##   Parametrisierung    ##
###########################

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

###########################

######################
## Global Variables ##
######################

infosig_nr = 666
camera = 0
 
############################################
##  State Transitions  Zustandsuebergaenge ##
############################################

##Definition der Zustanduebergaenge


def healthcheck_transitions(txt):
    """[Healthcheck Function]
    Function prueft die ansteuerung der Zentralen Komponenten

    Returns:
        boolean -- healthcheck erfolgreich oder nicht
    """

    logger.warn("Healthcheck implemented, transition to ready state anyway")
    if config.getboolean('Default', 'run_healthcheck'):
        healthy = healthcheck.run_healthcheck()
    #proceed anyway
    if(healthy):
        logger.info("Healthcheck passed")
        beep.beep(1)
    else:
        logger.error("Healthcheck not passed")
        beep.beep(2)

    time.sleep(2)

    #init mc
    mc_communication.preempt_serial_buffer()
    ##TODO: nur temporaer zum testen ohne aufladen
    #newState = "Infosignalerkennung"
    newState = "Transportgutsuche"
    return (newState, str(healthy))



def transportgutsuche_state_transitions(txt):
    """[Transportgutsuche Transition]
    Suche nach Transportgut.
    
    Returns:
        boolean -- Erkannt oder nicht erkannt.
    """
    logger.warn("Transportgutsuche implemented, Transition anyway")
    
    ##############################
    # Get Parameters from config #
    ##############################

    max_distance_cm = config.get('Sonic', 'sonic_threshold_max_distance_cm')
    min_distance_cm = config.get('Sonic', 'sonic_threshold_min_distance_cm')
    abtastrate = config.get('Sonic', 'sonic_abtastrate')
    timeout_count = config.get('Sonic', 'sonic_measurement_timeout_count')

    ###############################

    #Zug langsam anfahren lassen
    logger.info("Speed01 einleiten")
    #mc_communication.uart_send_speed01()
    mc_communication.uart_send_speedcustom("40")

    #t_return = transportgutsuche.run_transportgutsuche(sonic_threshold_max_distance_cm=max_distance_cm,
    #sonic_threshold_min_distance_cm=min_distance_cm, sonic_abtastrate=abtastrate,
    #sonic_measurement_timeout_count=timeout_count)
    #t_return = transportgutsuche.run_transportgutsuche()
    t_return = transportgutsuche.run_transportgutsuche(sonic_threshold_max_distance_cm=11,
    sonic_threshold_min_distance_cm=5, sonic_abtastrate=0.01,
    sonic_measurement_timeout_count=800)
  

    if(t_return == True):
        logger.info("Transportgutsuche erfolgreich!")
        logger.info("Zug Stop wurde eingeleitet")

    elif(t_return == False):
        logger.error("Transportgutsuche nicht erfolgreich!")
    else:
        logger.error("Got unrecognized value: ")
        logger.error(t_return)

    #proceed anyway at the moment
    newState = "Auflademodus"
    return (newState, t_return)


def auflademodus_state_transitions(txt):
    logger.warn("Auflademodus")
    time.sleep(0.5)
    auflademodus_flag = auflademodus.run_auflademodus()
    
    if(auflademodus_flag == True):
        logger.info("Aufladung erfolgreich! - Transition")
        beep.beep(1)


    elif(auflademodus_flag == False):
        logger.error("Aufladung nicht erfolgreich!")
    
    #proceed anyway
    newState = "Infosignalerkennung"
    return (newState, auflademodus_flag)


def infosignal_erkennung_state_transitions(txt):
    logger.warn("Infosignal Erkennung")

    ##############################
    # Get Parameters from config #
    ##############################

    #Not implemented - all parameters get imported directly in Sub File!

    ##############################
    #Camera starten
    global camera
    camera = initiator.init_camera()

    #Speed03 einleiten
    logger.info("Speed03 einleiten")
    #mc_communication.uart_send_speed03()
    mc_communication.uart_send_speedcustom("76")


    #Image Recognition starten
    infosignal_detect = number_detector.signal_detection(camera=camera, signalmode="info") #or signalmode="halte"

    global infosig_nr #globale Zuweisung der entdeckten Infosignalnummer
    infosig_nr = infosignal_detect
    
    logger.info("Infosignal erkannt: %i", infosig_nr)
    #beep as many times as the sig nr
    beep.beep(int(infosig_nr))

    ##Speed Change
    logger.info("Speed04 einleiten")
    #mc_communication.uart_send_speed04()
    mc_communication.uart_send_speedcustom("76")

    
    #proceed anyway
    newState = "Rundenerkennung"
    return (newState, "parameters")

#State zwischen Infosignal erkennung und Erkennung Runde 2 abgeschlossen (Runde 3) und dann Haltesignalerkennung
def runden_erkennung_state_transitions(txt):
    logger.warn("Runden-Erkennung mit Startsignalerkennung,  Kamera Mode!")

    startsignal_counter = 0
    startsignal_recogtime1 = 0
    startsignal_recogtime2 = 0

    global camera

    # Startsignal Counter --> Zeitstempel | 
    # Wenn Startsignal 1 erkannt wird und innert 5 sekunden nochmals, soll der counter nicht hochgezaehlt werden

    #solange startsignalcounter < 2 ist fahren
    while(startsignal_counter < 2):
        startsignal_recognized = number_detector.start_startsignal_detection(camera)
        if(startsignal_recognized):
            if (startsignal_counter==0):
                startsignal_counter += 1
                startsignal_recogtime1 = time.time()
            elif(startsignal_counter>=1):
                startsignal_recogtime2 = time.time()
                sig1_sig2_dif = int(startsignal_recogtime2 - startsignal_recogtime1)
                if (sig1_sig2_dif>5): #Nur hinzufuegen wenn Zeit diff groesser als 5s ist
                    startsignal_counter += 1


    if(startsignal_counter>=2):
        print("[Info] Startsignal 2 mal erkannt! Abbremsen und auf Haltesignalerkennung wechseln.")

    #Speed Change
    logger.info("Speed02 einleiten")
    #mc_communication.uart_send_speed02()
    mc_communication.uart_send_stop()
    time.sleep(0.2)
    mc_communication.uart_send_speedcustom("53") #evtl 52


    #proceed anyway
    newState = "Haltesignalerkennung"
    return (newState, "parameters")


def haltesignal_erkennung_state_transitions(txt):
    logger.warn("Haltesignal-Erkennung")

    ##############################
    # Get Parameters from config #
    ##############################

    #Not implemented - Config direct in SubFiles

    ##############################

    #Image Recognition starten
    global camera
    global infosig_nr
    haltesignal_detected = number_detector.signal_detection(camera=camera, signalmode="halt", infosig_nr=infosig_nr) #pass infosig_nr

    if(haltesignal_detected):
        logger.info("Haltesignal erkannt: %i" % haltesignal_detected)
        

    else:
        logger.error("Haltesignal nicht erkannt (fail)")

    #proceed anyway
    newState = "Praeziseshalten"
    return (newState, haltesignal_detected)


def praezises_halten_state_transitions(txt):
    logger.warn("PraezisesHalten not implemented,  nicht validiert, treshold nicht validiert")


    ##############################
    # Get Parameters from config #
    ##############################

    tof_measurement_timeout_millis = config.get('TOF', 'tof_measurement_timeout_millis')

    tof1_port = config.get('TOF', 'tof1_port')
    tof1_threshold_max_distance_mm = config.get('TOF', 'tof1_threshold_max_distance_mm')
    tof1_treshold_min_distance_mm = config.get('TOF', 'tof1_treshold_min_distance_mm')

    tof2_port = config.get('TOF', 'tof2_port')
    tof2_threshold_max_distance_mm = config.get('TOF', 'tof2_threshold_max_distance_mm')
    tof2_treshold_min_distance_mm = config.get('TOF', 'tof2_treshold_min_distance_mm')

    ##############################

    ##TODO: Temporaer disabled, just stop
    # praezises_halten_flag = praezises_halten.run_haltesignal_precise_stop(tof_measurement_timeout_millis=tof_measurement_timeout_millis, 
    # tof1_port=tof1_port, tof1_threshold_max_distance_mm=tof1_threshold_max_distance_mm, 
    # tof1_treshold_min_distance_mm=tof1_treshold_min_distance_mm, tof2_port=tof2_port, 
    # tof2_threshold_max_distance_mm=tof2_threshold_max_distance_mm, tof2_treshold_min_distance_mm=tof2_treshold_min_distance_mm)
    mc_communication.uart_send_stop()
    praezises_halten_flag = True


    if(praezises_halten_flag):
        logger.info("Praezises Halten erfolgreich, Zug gestoppt: %i" % praezises_halten_flag)
        
    else:
        logger.error("Praezises Halten nicht erfolgreich (fail), Zug gestoppt: %s" % praezises_halten_flag)

    #proceed anyway
    newState = "Fertig"
    return (newState, praezises_halten_flag)

def fertig_state(txt):
    logger.info("Zugreise erfolgreich abgeschlossen (Fertig)")
    beep.beep(2)
    time.sleep(1)
    print("Danke!")
    beep.beep(2)

def error_state(txt):
    logger.info("Error State reached")

    #back to ready
    return ("Ready", "parameters")



########################################
##  State Registrierung | Entry Point ##
########################################

if __name__== "__main__":
    logger.info("MainTrain started")
    #StateMachine initialize
    m = StateMachine()

    #Zustaende hinzufuegen
    m.add_state("Healthcheck", healthcheck_transitions)
    m.add_state("Transportgutsuche", transportgutsuche_state_transitions)
    m.add_state("Auflademodus", auflademodus_state_transitions)
    m.add_state("Infosignalerkennung", infosignal_erkennung_state_transitions)

    # Kein eigentlicher State, nur Hilsklasse und nuetzliche Transition
    m.add_state("Rundenerkennung", runden_erkennung_state_transitions)

    m.add_state("Haltesignalerkennung", haltesignal_erkennung_state_transitions)
    m.add_state("Praeziseshalten", praezises_halten_state_transitions)
    m.add_state("Error",None, end_state=1)
    m.add_state("Fertig",None, end_state=1)

    #Startpunkt setzen
    m.set_start("Healthcheck")

    # Setup Arduino Com #
    mccom_baudrate = config.get('MCCOM', 'mccom_baudrate')
    mccom_serial_interface = config.get('MCCOM', 'mccom_serial_interface')
    mc_communication.mc_setup(mccom_baudrate, mccom_serial_interface)
    #Initialize Arduino --> Preempt Buffer
    mc_communication.preempt_serial_buffer()

    #Program starten (parameterisierung moeglich)
    m.run("Zug starten, Gute Reise")
