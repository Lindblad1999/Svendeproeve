#include <Arduino.h>
#include <WiFi.h>
#include "config.h"

void setup() {
  Serial.begin(115200); // Open serial connection (To be removed)
  pinMode(GPIO_NUM_22, OUTPUT);
  digitalWrite(GPIO_NUM_22, HIGH); // Activate relay to close circuit as default.

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
  }
  Serial.println("Connected to Wifi");
  
}

void loop() {
  int voltageSensorRaw = analogRead(GPIO_NUM_36);
  Serial.println(voltageSensorRaw);
  int currentSensorRaw = analogRead(GPIO_NUM_39);
  Serial.println(currentSensorRaw);

  delay(1000);

}
