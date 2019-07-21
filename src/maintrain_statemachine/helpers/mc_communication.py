###########
## Infos ##
###########

# Class for Communication with Microcontroller (arduino)
# more infos: https://www.electronicwings.com/raspberry-pi/raspberry-pi-uart-communication-using-python-and-c

# use gpio 14 and 15 // TX, RX (blau,orange)
# mini UART (ttyS0) or PL011 UART (ttyAMA0) is mapped to UART pins (GPIO14 and GPIO15)
# or ttyACM0 for USB
# if unsure use /dev/serial0 (generic, USB or GPIO)

# Manual Test: echo “Hello” > /dev/ttyACM0
# Manual 2: echo "Hello" > /dev/serial0

###############
## Libraries ##
###############

import serial
from time import sleep

# [Variante 1] Kommunikation via USB:
# arduino_serial = serial.Serial('/dev/ttyACM0', 9600, timeout = 3)   #Open port with baud rate

# [Variante 2] Kommunikation via USB wenn V1 nicht funktioniert

arduino_serial = serial.Serial('/dev/serial0', 115200, timeout = 1)   #Open port with baud rate

# [Variante 3] Kommunikation via Serial Port über GPIOs (mit lvl shifter)
# arduino_serial = serial.Serial('/dev/serial0', 9600, timeout=3) 


#Logger (muss im selben Ordner sein)
import log_helper
logger = log_helper.create_Logger(False, "mc_communication")


###############
## Functions ##
###############

# listens, gets and strips data
def uart_listener():
    response = arduino_serial.readline()
    response = response.rstrip().decode("utf-8")
    print("[RPI-Com]: Arduino response: ")
    print(response)  # print received data

    # Parsing: Daten verarbeiten/parsen
    parsed_data = parse_received_data(response)

    return parsed_data

# Parse received Data and Act
def parse_received_data(data):
    print("[RPI-Com] parsing data '%s'" % data)

    if (find_text(data,"Error") != -1):
        print("[RPI-Com] Error!")
        return "Error"
    if(find_text(data,"Arduino:") != -1):
        print("[RPI-Com] Arduino Command bestätigt")
        return "Ack"
    if(find_text(data, "done") != -1):
        print("[RPI-Com] Arduino Task erfolgreich")
        return "done"
    
    #else wenn command nicht erkannt - return answer
    print("[RPI-Com]: Unbekannte Rückmeldung: ", data)
    return data


#Returns -1 if not found and position Integer (between 0 and endless) if found
def find_text(text, searchword):
    return text.find(searchword)

# Send Data to Serial Bus
def uart_send_generic(data):
    print("[RPI-Com] RPI sending data: '%s'" % (data))
    arduino_serial.write(data.encode("utf-8"))


#Generic Handle Response:
def handle_response(function_identifier):
    #1 If message Acknowledged - get result of operation
    Ack_message = uart_listener()

    if Ack_message == "Ack":
        logger.info("[RPI-Com (ACK)]: '%s' Acknowledged" % function_identifier)
        #2 Get Result - Arduino response -> done or Error
        Arduino_response = uart_listener()
        if Arduino_response == "done":
            logger.info("[RPI-Com (Result)]: '%s' Set successfull" % function_identifier)
            return True
        else:
            logger.info("[RPI-Com (Payload)]: '%s' Payload received" % function_identifier)
            return Arduino_response

    else: #no acknowledge --> error
        logger.error("[RPI-Com (Result)]: '%s' Set Error" % function_identifier)
        return False

#Initial den Serial buffer auslesen um alle "Startup" Nachrichten des Arduinos aus dem Cache zu spülen
def preempt_serial_buffer():
    initial_read = arduino_serial.read(1000) #liest bis zu 1000 bytes oder bis der Buffer leer ist.
    initial_read = initial_read.rstrip().decode("utf-8")
    print("====================================")
    print("[RPI-Com : MC preempt] Initial Arduino Message:")
    print(initial_read)
    print("====================================")


def mc_setup(mccom_baudrate=115200, mccom_serial_interface='/dev/serial0'):
    global arduino_serial

    try:
        arduino_serial = serial.Serial(str(mccom_serial_interface), mccom_baudrate, timeout = 1)   #Open port with baud rate
        print("MC Serial %s geöffnet" % mccom_serial_interface)
    except:
        print("MC Serial konnte nicht geöffnet werden")

#######################
# Predefined Commands #
#######################


def uart_get_mc_status():
    """[Statusabfrage beim MC (Was machst du gerade)]

    Mögliche states:
      speed01,
      speed02,
      speed03,
      speed04,
      stopMot,
      loadUp,
      currentStatus,
      ticks,
      Error
    """
    print("Get MC Status (currentStatus)")
    
    uart_send_generic("currentStatus")
    logger.info("[RPI-COM] Get MC Status")
    
    processed_response = handle_response("get_mc_status")
    logger.info("[RPI-COM] Current MC Status: %s" % processed_response)

    return processed_response


def uart_get_ticks():
    """[Fragt MC nach Ticks vom Linesensor ab für Rundenerkennung]
    """
    logger.info("[RPI-Com]: Get ticks")
    uart_send_generic("ticks")

    processed_response = handle_response("ticks")
    return processed_response



def uart_send_speed01():
    '''[Speed01 - Slowest Speed Modus: Für Transportgutsuche und Praezises halten]
    '''
    logger.info("[RPI-Com]: Set speed01")
    uart_send_generic("speed01")

    processed_response = handle_response("speed01")
    return processed_response



def uart_send_speed02():
    '''[Speed02 - Second Slowest Speed Modus: Für 3te Runde, HaltesignalErkennung]
    '''
    logger.info("[RPI-Com]: Set speed02")
    uart_send_generic("speed02")

    processed_response = handle_response("speed02")
    return processed_response


def uart_send_speed03():
    '''[Speed03 - Fast Speed Modus: Für 1te Runde, Infosignalerkennung]
    '''
    logger.info("[RPI-Com]: Set speed03")
    uart_send_generic("speed03")

    processed_response = handle_response("speed03")
    return processed_response


def uart_send_speed04():
    '''[Speed04 - Super Speed Modus: Für 2te Runde, Infosignalerkennung]
    '''
    logger.info("[RPI-Com]: Set speed04")
    uart_send_generic("speed04")

    processed_response = handle_response("speed04")
    return processed_response

def uart_send_speedcustom(percentValue):
    '''[SpeedCustom - Prozentualer Speed von 0 bis 100]
    '''
    logger.info("[RPI-Com]: Set SpeedCustom")
    uart_send_generic("speedcustom %s" % percentValue)

    processed_response = handle_response("speedcustom")
    return processed_response

def uart_send_auflademodus():
    '''[Auflademodus Modus: Transportgut]
    '''
    logger.info("[RPI-Com]: Set loadUp")
    uart_send_generic("loadUp")

    processed_response = handle_response("loadUp")
    return processed_response

#Ohne Response
def uart_send_rollUp():
    '''[Seilzug aufrollen]
    '''
    logger.info("[RPI-Com]: Send rollUp")
    uart_send_generic("rollUp")

    return "rollup sent"

#Ohne Response
def uart_send_rollDown():
    '''[Seilzug abrollent]
    '''
    logger.info("[RPI-Com]: Send rollDown")
    uart_send_generic("rollDown")

    return "rollup sent"

def uart_send_stop():
    '''[Stopt den Zug total: für Auflademodus, Praezises_halten]
    '''
    logger.info("[RPI-Com]: Set stopMot")
    uart_send_generic("stopMot")

    processed_response = handle_response("stopMot")
    return processed_response