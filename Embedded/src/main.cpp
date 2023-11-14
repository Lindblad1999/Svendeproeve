#include <Arduino.h>


void setup() {
  Serial.begin(115200);
  analogReadResolution(12);  
}

void loop() {
  int voltageSensorRaw = analogRead(GPIO_NUM_36);
  Serial.println(voltageSensorRaw);
  int currentSensorRaw = analogRead(GPIO_NUM_39);
  Serial.println(currentSensorRaw);
  delay(1000);
}
