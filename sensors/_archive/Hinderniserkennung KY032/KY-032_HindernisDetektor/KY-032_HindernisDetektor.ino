int Sensor = 33; // Deklaration des Sensor-Eingangspin
  
void setup ()
{
  Serial.begin(9600); // Initialisierung serielle Ausgabe
  pinMode (Sensor, INPUT); // Initialisierung Sensorpin

  analogReadResolution(11); // Default of 12 is not very linear. Recommended to use 10 or 11 depending on needed resolution.
 // analogSetAttenuation(ADC_6db); /
  Serial.println("Modul gestartet");
}
  
// Das Programm liest den aktuellen Status des Sensor-Pins aus und
// gibt in der seriellen Konsole aus, ob ein Hindernis aktuell erkannt wird
// oder ob kein Hindernis sich vor dem Sensor befindet
void loop ()
{
  Serial.println("Loop running...");
  bool val = digitalRead (Sensor) ; // Das gegenwärtige Signal am Sensor wird ausgelesen
  
  if (val == HIGH) // Falls ein Signal erkannt werden konnte, wird die LED eingeschaltet.
  {
    Serial.println("Kein Hindernis");
  }
  else
  {
    Serial.println("Hindernis erkannt");
  }
  Serial.println("------------------------------------");
  delay(500); // Pause zwischen der Messung von 500ms
}
