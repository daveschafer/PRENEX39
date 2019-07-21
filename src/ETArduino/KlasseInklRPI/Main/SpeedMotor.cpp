#include "SpeedMotor.h"
#include "Arduino.h"

////////////////////////////////////////////////////////
// Konstanten definieren
////////////////////////////////////////////////////////
const int SPEED1 = 99; //ToDo - finetuning
const int SPEED2 = 122;    
const int SPEED3 = 200;   
const int SPEED4 = 204;    
const int HALT = 0;
const int START_SPEED = 255; //<-- To Do

/*******************************************************
 * Aufruf des Konstruktors.                            *
 *******************************************************/
SpeedMotor :: SpeedMotor(int pin)
{
  speedNumber = 5;
  pinNumber = pin;
}

/*******************************************************
 * Schaltet anhand des Eingabefaktors den Motor in die *
 * entsprechende Geschwindigkeit                       *
 * @                                                   *
 *******************************************************/

 //die Serial messages stören das Kommunikationsprotokoll -> deshalb momentan alles geändert auf print statt println.
 //am besten anpassen auf Serial1.println...
 
void SpeedMotor :: setMotSpeed(int speedValue){
 speedNumber = speedValue;
 switch (speedNumber){
  case 0:   Serial.print("langsames beschleunigen: 1 ... ");  //<------------------------------------------------------------------ To Do
            for (int i = 30; i <= START_SPEED; i=i+1){ //langsames beschleunigen --> nur zu speed01 und speed03 möglich
                analogWrite(pinNumber, i);
                delay(10);                 
            };
            //Serial.print(START_SPEED);
            Serial.print(" abgeschlossen. ");
            break;
            
  case 1:   analogWrite(pinNumber, SPEED1);
            Serial.print("Speed auf 1 gesetzt. ");
            break;
            
  case 2:   analogWrite(pinNumber, SPEED2);
             Serial.print("Speed auf 2 gesetzt. "); 
            break;
            
  case 3:   analogWrite(pinNumber, SPEED3);
             Serial.print("Speed auf 3 gesetzt. "); 
            break;
            
  case 4:   analogWrite(pinNumber, SPEED4);
             Serial.print("Speed auf 4 gesetzt. "); 
            break;
            
  case 5:   analogWrite(pinNumber, HALT);
             Serial.print("Speed auf 0 gesetzt. "); 
            break;
 }
}

//Custom Speed Set in Percent (0...100)
void SpeedMotor :: setCustomMotSpeed(int percentValue){
  //apply some math magic
  int effectiveSpeed = (int)(2.550f * percentValue);  
  analogWrite(pinNumber, effectiveSpeed);
  
  Serial.print("Customspeed auf ");
  Serial.print(effectiveSpeed);
  Serial.print(" gesetzt. ");
  return;
}

/*******************************************************
 * Gibt die aktuelle Geschwindigkeitsstufe der Motoren *
 * an.                                                 *
 * @return = int                                       *
 *******************************************************/
int SpeedMotor :: getMotorState(void){
  return speedNumber;
  }

/*******************************************************
 * Gibt die Pinbelegung des Motors zurück              *
 *                                                     *
 * @return = int                                       *
 *******************************************************/
int SpeedMotor :: getPinNumber(void){
  return pinNumber;
  }
