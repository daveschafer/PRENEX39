#ifndef SpeedMotor_h
#define SpeedMotor_h


  /*********************************
   * Bibliothek/en einfügen
   *********************************/
  #include "Arduino.h"

  /*********************************
   * Definition der Klasse LineSensor
   *********************************/
class SpeedMotor
{
  private:
  /*********************************
   * Private Attribute
   *********************************/
   int pinNumber;
   int speedNumber;
  /*********************************
   * Private Methoden
   *********************************/
 
  
  public:
  void setMotSpeed(int speedNmber);
  void setCustomMotSpeed(int percentValue);
  int getMotorState(void);
  int getPinNumber(void);
  /*********************************
   * Konstruktor
   *********************************/
  SpeedMotor(int pin);

};
#endif
   
