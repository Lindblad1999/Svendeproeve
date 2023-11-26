#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include "config.h"

const String VOLTAGE_POST_ENDPOINT = "http://127.0.0.1:5000/voltage";
const String CURRENT_POST_ENDPOINT = "127.0.0.1:5000/current";

HTTPClient http;

void setup() {
  Serial.begin(115200); // Open serial connection (For debugging purposes)
  pinMode(GPIO_NUM_22, OUTPUT); // Set the relay pin to output for control
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
  float voltage = calculate_voltage(analogRead(GPIO_NUM_36));
  
  if (WiFi.status() == WL_CONNECTED) {
    http.begin(VOLTAGE_POST_ENDPOINT);
    http.addHeader("Content-type", "application/json");

    char requestString[128];
    sprintf(requestString, "{\"meas\":%d, \"device_id\":%d}", voltage, device_id);
    int httpResponseCode = http.POST(requestString);
    Serial.println(httpResponseCode);
    http.end();
  }

  Serial.println(voltage);

  int currentSensorRaw = analogRead(GPIO_NUM_39);
  Serial.println(calculate_current(currentSensorRaw));

  delay(1000);

}

