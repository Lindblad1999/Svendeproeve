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

float calculate_voltage(int rawData) {
  // Divide the raw ADC reading with the ADC resoulution (12-bit)
  // and multiply with Vref
  float voltage = (float)rawData / 4096 * 3.3;

  // The sensor outputs in a 1:5 ratio, so there must be multiplied with 5
  voltage = voltage * 5;

  return voltage;
}

float calculate_current(int rawData) {
  float current = (float)rawData - 2500;
  current = current / 4096 * 3.3;
  
  return current;
}

void loop() {
  int voltageSensorRaw = analogRead(GPIO_NUM_36);
  Serial.println(calculate_voltage(voltageSensorRaw));

  int currentSensorRaw = analogRead(GPIO_NUM_39);
  Serial.println(calculate_current(currentSensorRaw));

  delay(1000);

}

