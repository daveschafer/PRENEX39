#ifndef RPI_h
#define RPI_h

////////////////////////////////////////////////////////
// Library einfügen:
////////////////////////////////////////////////////////
#include "Arduino.h"
#include "SpeedMotor.h"
#include "LineSensor.h"
#include <Servo.h>
#include <AccelStepper.h>

      // Definition Enum
      enum stateCommands {
      speed01,
      speed02,
      speed03,
      speed04,
      speedcustom,
      stopMot,
      loadUp,
      currentStatus,
      ticks,
      rollUp,
      rollDown,
      Error
      }; 
      
class RPI 
{
  private:
  /*********************************
   * Private Attribute
   *********************************/
   int pinNumber;
   String receivedMsg;
   String answer;
   String status;
   int pos;

  /*********************************
   * Private Methoden
   *********************************/  
   enum stateCommands stringCompare(String command);   
   void blinkInternalLED();

  
  public:
   void checkCommunication( String receivedMsg, SpeedMotor mot, LineSensor line, Servo myservo, AccelStepper stepper, int pos);
   void set_currentStatus(String newStatus);
   String get_currentStatus();
   int customSpeedPercent;
 
  
  /*********************************
   * Konstruktor                   *
   *********************************/
  RPI();

};
#endif
