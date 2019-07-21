#Bibliotheken einbinden
import RPi.GPIO as GPIO
import time
 
#GPIO Modus (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
#sobald der count bei 10 ist wurde lastgut erkannt (10 * 0.1s = 1sekunde lange objekt erkannt)
lastgut_count = 0 
 
#GPIO Pins zuweisen
GPIO_TRIGGER = 18
GPIO_ECHO = 24
 
#Richtung der GPIO-Pins festlegen (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
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
 
if __name__ == '__main__':
    try:
        while True:
            abstand = distanzmessung()
            print ("Gemessene Entfernung = %.1f cm" % abstand)
            ### Webserver Mod ###
            #write abstand to file "/tmp/ultraschall_output.dat"
            with open("/tmp/ultraschall_output.dat", 'w') as filetowrite:
              filetowrite.write(str(round(abstand,2)))
              filetowrite.close()
            ### done ###
            time.sleep(0.25) #3 millisekonds
            if(abstand <= 10 and abstand >= 4):
                if(lastgut_count>=10):
                    print("Lastgut definitiv erkannt!")
                else:
                    print("Lastgut potentiell erkannt!")
                    lastgut_count += 1
 
        # Beim Abbruch durch STRG+C resetten
    except KeyboardInterrupt:
        print("Messung vom User gestoppt")
        GPIO.cleanup()