#include "LineSensor.h"
#include "SpeedMotor.h"
#include "RPI.h"
#include <Servo.h>
#include <AccelStepper.h>

/******************************************************* 
 *                Aktuelle Pinbelegung                 *              
 *                                                     *
 *  Sensoren:                                          *
 *  - LineSensor (ls1, ls2)                            *
 *                                                     *
 *  Aktoren:                                           *
 *  - Antriebsmotoren (m1, m2, m3, m4)                 *
 *******************************************************/
int sm1 = 3;
int pinLineSensor1 = 7;
int pinLineSensor2 = 8;
int servoConPin = 12;
int stepperDirPin = 47; //Für Mega 47
int stepperStepPin = 46; //Für Mega 46

/******************************************************* 
 *            Lokale Variablen                         * 
 *******************************************************/
String receivedMsg;
int stepperSpeed = 9600; //Maximale Anzahl Schritte pro Sekunde (3rps/ at 16 microsteps)
long stepperAccel = 80000; //Schritte / Sekunde/ Sekunde zum Beschleunigen
int pos = 0;

/******************************************************* 
 *            Instanziierung der Objekte               * 
 *******************************************************/
LineSensor ls1(pinLineSensor1);  // Konstruktorenaufruf
SpeedMotor m1(sm1);
RPI rpi0; //ohne () aufrufen für eine default instanzierung
AccelStepper stepper(1, stepperStepPin, stepperDirPin);
Servo myservo;

/******************************************************* 
 *            Programminitialisierung                  * 
 *                                                     *
 * Wird nur einmal Ausgeführt!                         *
 *******************************************************/
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.setTimeout(30); // Timout für Schnittstelle --> default = 1s
  Serial.println("[MC]: Program started");
  stepper.setMaxSpeed(stepperSpeed);
  stepper.setAcceleration(stepperAccel);
  rpi0.set_currentStatus("stopMot");

  // Initilize the digital pin LED_BUILTIN as output [nuetzlich zum debugen]
  pinMode(LED_BUILTIN, OUTPUT);
}



/******************************************************* 
 *                    Main Code                        *                    
 *                                                     * 
 * Functions:                                          *                                          
 * - Count the steps from linesensors                  *                   
 * - Check the serial input and reponds to command     * 
 *******************************************************/
void loop() {

  // put your main code here, to run repeatedly:
  // 1: Call Linesensor
  ls1.setStateAndCount();
  // 2: Manual Set Speed (Muss der SPeed wirklich bei JEDEM Loop auf Speed3 gesetzt werden?!?)
  //m1.setMotSpeed(3);
  
  // 3: Raspberry Communication -> Serial Buffer auslesen falls eine Nachricht ansteht.
   if (Serial.available()) {
      receivedMsg = Serial.readStringUntil('\n'); 
      //Mit diesem Befehl würde die Antwort jeweils wieder an den RPI zurückgesendet werden - das würde den Programmfluss stören
      //Wenn du den Serial zum debuggen brauchst, am besten einen der anderen Arduino Mega TX/RX Ports verwenden (Serial1, Serial2...)
      
      //Serial.println(receivedMsg);  
      rpi0.checkCommunication(receivedMsg, m1, ls1, myservo, stepper, pos);
  };           
  
}
