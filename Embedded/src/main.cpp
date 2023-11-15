#include <Arduino.h>


void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  pinMode(GPIO_NUM_22, OUTPUT);
}

void loop() {
  int voltageSensorRaw = analogRead(GPIO_NUM_33);
  Serial.println(voltageSensorRaw);
  int currentSensorRaw = analogRead(GPIO_NUM_39);
  Serial.println(currentSensorRaw);

  digitalWrite(GPIO_NUM_22, HIGH);
  delay(1000);
  digitalWrite(GPIO_NUM_22, LOW);
  delay(1000);

}
