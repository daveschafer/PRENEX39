
# Add Libraries
import time

#smbus wird benötigt "sudo apt-get install python3-smbus"
#install beforehand with sudo pip3 install adafruit-circuitpython-vl6180x
from ST_VL6180X import VL6180X


def get_sensor_data(tof_sensor):
    #starup sensor 
    tof_sensor.get_identification()
    print("**************************************")
    if tof_sensor.idModel != 0xB4:
        print("Not a valid sensor id: {:X}".format(tof_sensor.idModel))
    else:
        print("Sensor model: {:X}".format(tof_sensor.idModel))
        print("Sensor model rev.: {:d}.{:d}"
            .format(tof_sensor.idModelRevMajor, tof_sensor.idModelRevMinor))
        print("Sensor module rev.: {:d}.{:d}"
            .format(tof_sensor.idModuleRevMajor, tof_sensor.idModuleRevMinor))
        print("Sensor date/time: {:X}/{:X}".format(tof_sensor.idDate, tof_sensor.idTime))
        print("Sensor address: {:X}".format(tof_sensor.address))
    tof_sensor.default_settings()
    print("**************************************")

    time.sleep(1)
    print("Measured distance is : ", tof_sensor.get_distance(), " mm" )

# Main loop prints the range (and lux) every 0.25s

def change_i2c_addr(tof_sensor, tof_address, tof_address_new):
    tof_sensor.change_address(tof_address, tof_address_new)

def measure_10seconds(tof_sensor):
    for x in range(0,10):
        print("Measured distance is : ", tof_sensor.get_distance(), " mm" )
        print("Measured distance is : ", tof_sensor.get_distance(), " mm" )
        print("Measured distance is : ", tof_sensor.get_distance(), " mm" )
        time.sleep(1)

if __name__ == '__main__':
    #x30 = tof1
    #x29 = tof2
    debug = False
    #init the sensor
    tof_address = 0x29
    tof_address_new = 0x30
    tof_sensor1 = VL6180X(address=tof_address, debug=debug)

    #readout sensordata
    get_sensor_data(tof_sensor1)

    #now change the address
    change_i2c_addr(tof_sensor1, tof_address, tof_address_new)
    
    #sensor nochmals auslesen
    get_sensor_data(tof_sensor1)

    print("TOF1 ready.")
    #tof1 muss nun deaktiviert werden sonst werden immer beide tofs überschrieben
    #tof2 hat jetzt übrigens auch adresse 30
    

    #jetzt tof sensor 2 einlesen
    tof_sensor2 = VL6180X(address=tof_address, debug=debug)

    #readout sensordata2
    get_sensor_data(tof_sensor2)

    #readout sensor1
    print("sensor1 wird ausgelesen: ")
    measure_10seconds(tof_sensor1)

    #readout sensor2
    print("sensor2 wird ausgelesen: ")
    measure_10seconds(tof_sensor2)

    print("init completed. TOF ready")

    #fin