#include "LineSensor.h"

/*******************************************************
 * Aufruf des Konstruktors.                            *
 *******************************************************/
LineSensor :: LineSensor(int pin)
{
  state = 'h';
  tickCounter = 0;
  stateValueLineSensor = 0;
  pinNumber = pin;
  
  pinMode(pin, INPUT);
  digitalWrite(pin, HIGH);
}

/*******************************************************
 * Liest den digitalen Wert (0 oder 1 für hell oder    *                             
 * dunkel) aus dem Sensor aus und gibt diesen zurück   *
 * @return: Integer                                    *
 *******************************************************/
int LineSensor :: getLineSensorState(void){
  return digitalRead(pinNumber);  
}

/*******************************************************
 * Setzt den Counterwert + 1 wenn eine Farbänderung    *                             
 * erkannt wird.                                       *
 *******************************************************/
void LineSensor :: setStateAndCount (void){
 if (getLineSensorState() == 0)
  {
    setCountH();
    state = 'h';
  }
  else if (getLineSensorState() == 1)
  {
    setCountD();
    state = 'd';
  };
}


/*******************************************************
 * Zählt vom Übergang hell --> dunkel den Counter um   *
 * einen Wert nach oben.                               *
 *******************************************************/
void LineSensor :: setCountH (void){
  if (state == 'd')
  {
   countTicks(); 
  };
}

/*******************************************************
 * Zählt vom Übergang dunkel --> hell den Counter um   *
 * einen Wert nach oben.                               *
 *******************************************************/
void LineSensor :: setCountD (void){
   if (state == 'h')
  {
    countTicks();
  };
}

/*******************************************************
 * Zählt die Steps des Quadraturencoders.              *
 * @                                                   *
 *******************************************************/
void LineSensor :: countTicks(void){
  tickCounter = tickCounter + 1;  
}

/*******************************************************
 * Gibt die gezählten Steps zurück.                    *
 * @return: Integer                                    *
 *******************************************************/
long LineSensor :: getTicks(void){
  return tickCounter;  
}
