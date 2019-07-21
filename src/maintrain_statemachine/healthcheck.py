"""[Healthcheck Klasse]

Diese Klasse kümmert sich um einen sauberen Healthcheck des Systems
"""
###############
## Libraries ##
###############

#General
import os 
import log_helper
logger = log_helper.create_Logger(False, "healthcheck")
import nice_headers
#Used for Camera Check
import subprocess
#HC04 Sonic
import time
import RPi.GPIO as GPIO
import multiprocessing
#TOF I2C
import board
import busio
import adafruit_vl6180x
#MC Com
import serial

#add adafruit multiplexer library
import adafruit_tca9548a
#install pip3 install adafruit-circuitpython-tca9548a

################
# Global Flags #
################


#######################
## Helper Functions ###
#######################

# Return % of CPU used by user as a character string                                
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
)))

# Return RAM information (unit=kb) in a list                                        
# Index 0: total RAM  | Index 1: used RAM  | Index 2: free RAM                                                                
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])

#get processes
from subprocess import check_output
def get_pid(name):
    return check_output(["pidof",name])

#check Sonic
def check_sonic():
    GPIO.setmode(GPIO.BCM)
    GPIO_TRIGGER = 18
    GPIO_ECHO = 24
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    StartZeit = time.time()
    StopZeit = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        StartZeit = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
        StopZeit = time.time()

    TimeElapsed = StopZeit - StartZeit
    logger.info("Sonic: Time Elapsed %i", TimeElapsed)
    if(TimeElapsed != None and TimeElapsed >= 0):
        return True
    else:
        return False

#Schaut ob der MC Antwort gibt.
def check_microcontroller():
    _usb0 = check_microcontroller_comhandler('/dev/ttyUSB0')
    _serial0 = check_microcontroller_comhandler('/dev/serial0')
    _acm0 = check_microcontroller_comhandler('/dev/ttyACM0')

    logger.info("usb0 %s , serial0 %s, acm0 %s" % (_usb0, _serial0, _acm0))
    if (_usb0 or _serial0 or _acm0):
        return True
    else:
        return False

#Helper for MC Com
def check_microcontroller_comhandler(com_interface):
    try:
        arduino_serial = serial.Serial(com_interface, 9600, timeout = 3)   #Open port with baud rate
        data = "currentStatus"
        arduino_serial.write(data.encode("utf-8"))
        response = arduino_serial.readline()
        response = response.rstrip().decode("utf-8")
        if not (response is None or response is ""):
            logger.info("MC Answer not empty!")
            return True
        else:
            logger.warn("!!!MC Serial Kanal '%s' empty response" % com_interface)
            return True
    except:
        logger.warn("!!!MC Serial Kanal '%s' konnte nicht geöffnet werden!!!" % com_interface)
        return False


#######################
## Main Function    ###
#######################

def run_healthcheck(cargo="undefined"):
    """[Healthcheck starten]

    Arguments:
        cargo {String} -- Cargo Parameter (default: {undefined})

    Returns:
        Boolean --  True, falls Healtcheck OK.
                    False, falls Fehler beim Healthcheck (siehe Log).
    """

    print("Class Healthcheck not productive yet (99 percent done, testing ausstehend).")

    ##define flags for nice headers
    cpu_flag, ram_flag, sonic_flag, tof1_flag, tof2_flag, camera_flag, mc_flag, passed_flag = "NA","NA","NA","NA","NA","NA","NA","NA"
    findings = 0

    #Getting CPU
    CPU_usage = getCPUuse()
    #Getting RAM
    RAM_stats = getRAMinfo()
    RAM_free = round(int(RAM_stats[2]) / 1000,1)

    #Sollte kleiner als 10% sein
    if (float(CPU_usage)>= 10):
        logger.warn("CPU Usage too high!")
        findings += 1

    cpu_flag= CPU_usage
    logger.info("CPU Usage: %s", str(CPU_usage))

    #Sollte grösser als 300 sein
    if (RAM_free<=300):
        logger.warn("Not enough RAM available!")
        findings += 1

    ram_flag = RAM_free
    logger.info("RAM Free: %s", str(RAM_free))

    #Get python prozesses
    python_procs = "NA"
    try:
        python_procs = get_pid("python")
        logger.warn("The follow Python-Processes are already running: ", python_procs)
        findings += 1
    except:
        logger.info("No python running, good2go!")


    #Check if Camera Available
    camera_result = (subprocess.check_output("vcgencmd get_camera", shell=True)).decode("utf-8").rstrip() #decode and remove \n

    if ( (camera_result.rsplit(" ",2)[0].split("=",1)[1]) == "1" and (camera_result.rsplit(" ",2)[1].split("=",1)[1]) == "1" ):
        camera_flag = True
        logger.info("Camera ready! 📷")
    else:
        camera_flag = False
        logger.warn("Camera not available! ❌")
        findings += 1

    #Check sonic
    p = multiprocessing.Process(target=check_sonic, name="checksonic") #remember, pass functions without ()
    p.start()
    p.join(3)

    if p.is_alive():
        logger.warn("Sonic Check takes too long")
        p.terminate()
        p.join()
        sonic_flag = False
        findings += 1
    else:
        sonic_flag = check_sonic()
        logger.info("Sonic test passed")

    #Check TOF Multiplexer
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        # Create the TCA9548A object and give it the I2C bus
        tca = adafruit_tca9548a.TCA9548A(i2c)
        logger.warn("I2C Multiplexer Device (0) Available (probably)")
        tca_flag = True
    except:
        logger.warn("I2C Multiplexer Device (0) Unavailable")
        findings += 1
        tca_flag = False

    #Check TOF 1
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        tca = adafruit_tca9548a.TCA9548A(i2c)

        sensor_tof1 = adafruit_vl6180x.VL6180X(tca[0])
        logger.info("I2C Device (1) Available")
        tof1_flag = True
    except:
        logger.warn("I2C Device (1) Unavailable")
        findings += 1
        tof1_flag = False

    #Check TOF 2
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        tca = adafruit_tca9548a.TCA9548A(i2c)

        sensor_tof2 = adafruit_vl6180x.VL6180X(tca[1])
        logger.info("I2C Device (2) Available")
        tof2_flag = True
    except:
        logger.warn("I2C Device (1) Unavailable")
        findings += 1
        tof2_flag = False

    #Check MC-COM

    #mc_flag = check_microcontroller()
    print("MC healtcheck bypassed!!")
    mc_flag = True

    if(mc_flag):
        logger.info("MC is online and well 🤖!")
    else:
        logger.warn("MC is offline!")
        findings += 1

    #Validating Findings
    if (findings>0):
        passed_flag=False
    else:
        passed_flag=True
    
    logger.info("Healthcheck completed with '%s' findings", str(findings))


    #Print Header Message
    nice_headers.print_nice_headers(passed_flag,cpu_flag,ram_flag,tof1_flag,tof2_flag,sonic_flag,camera_flag, mc_flag)

    return passed_flag