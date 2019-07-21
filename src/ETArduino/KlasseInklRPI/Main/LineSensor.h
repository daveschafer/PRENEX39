#ifndef LineSensor_h
#define LineSensor_h

  /*********************************
   * Bibliothek/en einfügen
   *********************************/
#include "Arduino.h"


  /*********************************
   * Definition der Klasse LineSensor
   *********************************/
class LineSensor
{
  private:
  /*********************************
   * Private Attribute
   *********************************/
  long tickCounter;
  char state;
  int stateValueLineSensor;
  int pinNumber;
  /*********************************
   * Private Methoden
   *********************************/
  int getLineSensorState(void);
  void setCountH (void);
  void setCountD (void);
  void countTicks(void);
  
  
  public:
  void setStateAndCount (void); 
  long getTicks(void);
  
  /*********************************
   * Konstruktor
   *********************************/
  LineSensor(int pin);

};
#endif
