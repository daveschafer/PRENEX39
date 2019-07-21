#include "RPI.h"


/*******************************************************
 * Aufruf des Konstruktors.                            *
 *******************************************************/
   RPI :: RPI()
{
  
}


/*******************************************************
 * Überprüft den Befehl und führt die dazugehörige     *
 * Anweisung aus. Mit einem Acknowledge wird der Auf-  *
 * trag bestätigt.                                     *
 *******************************************************/
void RPI :: checkCommunication(String receivedMsg, SpeedMotor mot, LineSensor line, Servo myservo, AccelStepper stepper, int pos) //Check for the different Requests which are possible -> kann man evtl auch effizienter lösen mit threading oder so
{
      SpeedMotor motor = mot;
      LineSensor ls = line;
      //Servo myservo = myservo;
      //AccelStepper stepper = stepper;

      //blink when command received
      //blinkInternalLED();
      
      enum stateCommands command =  stringCompare(receivedMsg);

     
        switch (command){
          case speed01:   answer = "Arduino: speed01";
                          Serial.println(answer);
                          
                          // set Speed
                          motor.setMotSpeed(1);
                          
                          // return status
                          status = receivedMsg; 
                     
                          // return when job is done
                          Serial.println("done");
                          break; 
                     
          case speed02:   answer = "Arduino: speed02";
                          Serial.println(answer);
                          
                          // set Speed
                          motor.setMotSpeed(2);
  
                          // return status
                          status = receivedMsg; 
                     
                          // return when job is done
                          Serial.println("done");
                          break;  
  
          case speed03:   answer = "Arduino: speed03";
                          Serial.println(answer);
                       
                          
                          // set Speed
                          motor.setMotSpeed(3);
  
                          // return status
                          status = receivedMsg; 
                     
                          // return when job is done
                          Serial.println("done");
                          break;  
  
          case speed04:   answer = "Arduino: speed04";
                          Serial.println(answer);
                          
                          // set Speed
                          motor.setMotSpeed(4);
  
                          // return status
                          status = receivedMsg; 
                     
                          // return when job is done
                          Serial.println("done");
                          break; 
                     
          case speedcustom:   answer = "Arduino: speedcustom";
                          Serial.println(answer);
                          
                          //do nothing if false parameter set
                          if((customSpeedPercent > 100) || (customSpeedPercent < 0)){
                            Serial.println("!customspeed out of Range (0...100)! done");
                            break;
                          }

                          // set Speed custom
                          motor.setCustomMotSpeed(customSpeedPercent);
  
                          // return status
                          status = receivedMsg; 
                     
                          // return when job is done
                          Serial.println("done");
                          break;                      

          case stopMot:   answer = "Arduino: stopMot";
                          Serial.println(answer);
                          
                          //  set Speed
                          motor.setMotSpeed(5);
  
                          // return status
                          status = receivedMsg; 
                     
                          // return when job is done
                          Serial.println("done");
                          break;   
  
          case loadUp:    answer = "Arduino: loadUP";
                          Serial.println(answer);
                          
                          //ToDo - Kran aufladefunktion aufrufen (von JH)

                          status = "ladend";

                          // Todo, der Status soll auf "aufgeladen" oder "nichtgeladen" gesetzt werden -> Ich verwende diese Wörter im RPI Steuerprogramm
                          // Der Status muss nicht sofort gesetzt werden, er kann auch zuerst von JH auf "ladend" gesetzt werden
                          // und dann später von extern auf "aufgeladen" gesetzt werden
                          // Das Steuerprogramm prüft 20 Sekunden lang den MC Status.

                          pinMode(41, OUTPUT);
                          
                          myservo.attach(12);
                          myservo.write(pos);
                          delay(800);
                          for (pos = 0; pos <= 145; pos += 1) { // dreht von 0-180 Grad in 1 Grad Schritten
                            myservo.write(pos);              // Servo soll nach Position in Variable
                            delay(15);                       
                          }
                          delay(400);
                          
                          
                          //if stepper is at desired location
                          stepper.moveTo(4400); //move 32000 steps (should be 10 rev) 4850 für drei umdrehungen
                          while(stepper.distanceToGo() != 0){
                            digitalWrite(41, HIGH);
                            stepper.run();
                          }
                            //go the other way the same amount of steps
                            //so if current position is 400 steps out, go position -400
                            stepper.moveTo(-2900); //move 32000 steps (should be 10 rev) 4850 für drei umdrehungen
                          while(stepper.distanceToGo() != 0){
                            digitalWrite(41, HIGH);
                            stepper.run();
                          }
                         
                          
                          //these must be called as often as possible to ensure smooth operation
                          //any delay will cause jerky motion
                          
                          for (pos = 145; pos >= 0; pos -= 1) { // dreht von 180-0 Grad in 1 Grad Schritten
                            myservo.write(pos);              
                            delay(15);                       
                          }
                          delay(300);
                          
                          stepper.moveTo(200); //move 32000 steps (should be 10 rev) 4850 für drei umdrehungen
                          while(stepper.distanceToGo() != 0){
                            stepper.run();
                          }
                          myservo.detach();
                          digitalWrite(41, LOW);

                          // return status
                          status = "aufgeladen"; 
                     
                          // return when job is done
                          Serial.println("done");
                          break;  
                           
    case currentStatus:   answer = "Arduino: Status Request, sending current state";
                          Serial.println(answer); //Acknowledge
                          
                          //Result
                          Serial.println(status);
                          break;  

         case ticks:      answer = "Arduino: getTicks";
                          Serial.println(answer); //Acknowledge
                          
                          // Result
                          Serial.println(ls.getTicks());
                          
                          // bei Tick-Abfragen soll der Status NICHT überschrieben werden!
                          //status = receivedMsg; 
                          break;  
                          
         case rollUp:     pinMode(41, OUTPUT);
                          
                          stepper.moveTo(-3200); //move 32000 steps (should be 10 rev) 4850 für drei umdrehungen
                          while(stepper.distanceToGo() != 0){
                          digitalWrite(41, HIGH);
                          stepper.run();
                          }
                          digitalWrite(41, LOW);
                          break;
                               
         case rollDown:   pinMode(41, OUTPUT);
                          
                          stepper.moveTo(3200); //move 32000 steps (should be 10 rev) 4850 für drei umdrehungen
                          while(stepper.distanceToGo() != 0){
                          digitalWrite(41, HIGH);
                          stepper.run();
                          }
                          digitalWrite(41, LOW);
                          break;
                          
         default:         //Send back error message
                          Serial.println("Error");
                       //   motor.setMotSpeed(receivedMsg.toInt());
                         
                          break;
                                                                                                     
        };   
}


/*********************************
 *  Setter und Getter für Status *
 *                               *
 *********************************/

//do sanity check
 void RPI :: set_currentStatus(String newStatus){
  Serial.print("Setting status to: ");
  Serial.println(newStatus);
  status = newStatus;
 }

 String RPI :: get_currentStatus(){
  return status;
 }

//Dont use this, only for testing
  void RPI :: blinkInternalLED(){
    for (int i = 0; i <= 4; i++){
    digitalWrite(LED_BUILTIN, HIGH);   // Turn the built-in LED on
    delay(40);                       // Pause for 1 second (1000 milliseconds)
  
    digitalWrite(LED_BUILTIN, LOW);    // Turn the built-in LED on
    delay(40); 
    }
  }
 
/*******************************************************
 * Wandelt den String des Befehls in einen Enumwert um *
 *                                                     *
 * @return: enum stateCommands                         *
 *******************************************************/
enum  stateCommands RPI ::  stringCompare (String command){

  //Das hier stört die Kommunikation, please dont do this
  //Serial.println(command);
  if (command.equals("speed01")){
    return speed01;
  }; 
  if (command.equals("speed02")){
    return speed02;
  };
  if (command.equals("speed03")){
    return speed03;
  };
  if (command.equals("speed04")){
    return speed04;
  };
  if(command.indexOf("speedcustom", 0) >= 0){ //Special Mod for custom Speed
    //set glob var customspeed
    String stringspeed = command.substring(11);
    customSpeedPercent = stringspeed.toInt();
    return speedcustom;
  };
  if (command.equals("stopMot")){
    return stopMot;
  };
  if (command.equals("loadUp")){
    return loadUp;
  };
  if (command.equals("currentStatus")){
    return currentStatus;
  };
  if (command.equals("ticks")){
    return ticks;
  };
  if (command.equals("rollUp")){
    return rollUp;
  };
  if (command.equals("rollDown")){
    return rollDown;
  }else {
    return Error;
  };
}
