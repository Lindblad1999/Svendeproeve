#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "config.h"

const String API_ADDRESS = "https://svendeproeve-api-7b4ec1c0ab8f.herokuapp.com";
const String VOLTAGE_POST_ENDPOINT = "https://svendeproeve-api-7b4ec1c0ab8f.herokuapp.com/voltage";
const String CURRENT_POST_ENDPOINT = "https://svendeproeve-api-7b4ec1c0ab8f.herokuapp.com/current";

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

  // Post a relay status log that tells relay is ON
  if (WiFi.status() == WL_CONNECTED) {
  HTTPClient http;
  http.begin(API_ADDRESS + "/relay/status");
  http.addHeader("Content-type", "application/json");

  char requestString[128];
  sprintf(requestString, "{\"state\":%d, \"device_id\":%d}", 1, device_id);
  int httpResponseCode = http.POST(requestString);
  http.end();
}
  
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
  float current;
  // Check if the relay PIN is high or low
  // If high, calculate the current. If low return 0, as the sensor is too unprecise. 
  if (digitalRead(GPIO_NUM_22) == 1){
    current = (float)rawData - 2200;
    current = current / 4096 * 3.3;
  } else {
    current = 0.0;
  }
  
  return current;
}

void handle_relay_get(String response){
  DynamicJsonDocument doc(1024);
  deserializeJson(doc, response);

  int state = doc["state"];
  if (state == 1){
    digitalWrite(GPIO_NUM_22, HIGH);
  } 
  else if (state == 0) {
    digitalWrite(GPIO_NUM_22, LOW);
  }
}

void loop() {
  float voltage = calculate_voltage(analogRead(GPIO_NUM_36));
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(VOLTAGE_POST_ENDPOINT);
    http.addHeader("Content-type", "application/json");

    char requestString[128];
    sprintf(requestString, "{\"meas\":%.2f, \"device_id\":%d}", voltage, device_id);
    int httpResponseCode = http.POST(requestString);
    http.end();
  }

  float current = calculate_current(analogRead(GPIO_NUM_39));
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(CURRENT_POST_ENDPOINT);
    http.addHeader("Content-type", "application/json");

    char requestString[128];
    sprintf(requestString, "{\"meas\":%.2f, \"device_id\":%d}", current, device_id);
    int httpResponseCode = http.POST(requestString);
    http.end();
  }

  if (WiFi.status() == WL_CONNECTED) {
  HTTPClient http;
  http.begin(API_ADDRESS + "/relay/status");

  int httpResponseCode = http.GET();
  if (httpResponseCode > 0) {
    handle_relay_get(http.getString());
  }
  http.end();
}

  delay(1000);
}

