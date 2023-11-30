#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "config.h"

const String API_ADDRESS = "https://svendeproeve-api-7b4ec1c0ab8f.herokuapp.com";
const String VOLTAGE_POST_ENDPOINT = "https://svendeproeve-api-7b4ec1c0ab8f.herokuapp.com/voltage";
const String CURRENT_POST_ENDPOINT = "https://svendeproeve-api-7b4ec1c0ab8f.herokuapp.com/current";
const int RELAY_PIN = GPIO_NUM_22;
const int CURRENT_PIN = GPIO_NUM_39;
const int VOLTAGE_PIN = GPIO_NUM_36;
const String API_KEY = "secretkey1";

// Code will be run once, in the startup
void setup() {
  Serial.begin(115200); // Open serial connection (For debugging purposes)
  pinMode(RELAY_PIN, OUTPUT); // Set the relay pin to output for control
  digitalWrite(RELAY_PIN, HIGH); // Activate relay to close circuit as default.

  // Start a connection to WiFi and wait for a connection to be established
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
  }
  Serial.println("Connected to Wifi");

  // Post a relay status log that tells relay is ON
  if (WiFi.status() == WL_CONNECTED) {
    // Start a HTTP connection to the API /relay/status endpoint 
    HTTPClient http;
    http.begin(API_ADDRESS + "/relay/status?apikey=" + API_KEY);
    http.addHeader("Content-type", "application/json");

    // Format the data to be posted to JSON format, and send POST request
    char requestString[128];
    sprintf(requestString, "{\"state\":%d, \"device_id\":%d}", 1, device_id);
    int httpResponseCode = http.POST(requestString);
    http.end(); // Close HTTP connection
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
  if (digitalRead(RELAY_PIN) == 1){
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
    digitalWrite(RELAY_PIN, HIGH);
  } 
  else if (state == 0) {
    digitalWrite(RELAY_PIN, LOW);
  }
}

// Main loop that runs continuously
void loop() {
  // Read voltage sensor measurement and calculate the voltage from the raw ADC value.
  float voltage = calculate_voltage(analogRead(VOLTAGE_PIN)); 
  // Send a POST request to the API with a voltage measurement
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(VOLTAGE_POST_ENDPOINT + "?apikey=" + API_KEY);
    http.addHeader("Content-type", "application/json");

    char requestString[128];
    sprintf(requestString, "{\"meas\":%.2f, \"device_id\":%d}", voltage, device_id);
    int httpResponseCode = http.POST(requestString);
    http.end();
  }

  // Read current sensor measurement and calculate the current from the raw ADC value.
  float current = calculate_current(analogRead(CURRENT_PIN));
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(CURRENT_POST_ENDPOINT + "?apikey=" + API_KEY);
    http.addHeader("Content-type", "application/json");

    char requestString[128];
    sprintf(requestString, "{\"meas\":%.2f, \"device_id\":%d}", current, device_id);
    int httpResponseCode = http.POST(requestString);
    http.end();
  }

  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(API_ADDRESS + "/relay/status?apikey=" + API_KEY);

    int httpResponseCode = http.GET();
    if (httpResponseCode > 0) {
      handle_relay_get(http.getString());
    }
    http.end();
}

  delay(1000);
}

