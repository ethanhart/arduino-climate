/*
Temperature Guage

Based on the current temperature, light up LED(s) to indicate, within a range,
the current temperature. Designed for normal housing temperatures.

From cold to warm:
b --> bg --> g --> gy --> y --> yr --> r

Author: Ethan Hart
Date: 2015-01-11
*/

#include <Time.h>

#define TIME_MSG_LEN  11   // time sync to PC is HEADER followed by Unix time_t as ten ASCII digits
#define TIME_HEADER  'T'   // Header tag for serial time sync message
#define TIME_REQUEST  7    // ASCII bell character requests a time sync message 


const int sensorPin = A0; // TMP36 sensor pin

void setup() {
  Serial.begin(9600); // open a serial port

  // Initialize output pins for LEDs
  for(int pinNumber = 2; pinNumber<6; pinNumber++) {
    pinMode(pinNumber, OUTPUT);
    digitalWrite(pinNumber, LOW);
  }
  
}

void loop() {
  int sensorVal = analogRead(sensorPin);
  //Serial.print("Sensor Value: ");
  //Serial.print(sensorVal);

  // convert ADC reading to voltage
  float voltage = (sensorVal/1024.0) * 5.0;
  //Serial.print(", Volts: ");
  //Serial.print(voltage);

  // convert voltage to temperature
  float tempC = (voltage - 0.5) * 100; // get temp in Celcius
  float tempF = (tempC * 9.0/5.0) + 32; // temp in Fahrenheit (because USA)
 

  int blue = 3; // blue and green are "swapped" so blue can run off pin 3 to use analogWrite()
  int blueBright = 10; // blue needs to be dim: otherwise, it overpowers green light
  int green = 2;
  int yellow = 4;
  int red = 5;

  // write out temperature
  //Serial.print(", degrees C: ");
  //Serial.print(tempC);
  //Serial.print(", degrees F: ");
  //Serial.print(tempF);
  Serial.println(tempF);
  String temp_str;

  if(tempF < 60) {
    temp_str = "COLD";
    analogWrite(blue, blueBright);
    digitalWrite(green, LOW);
    digitalWrite(yellow, LOW);
    digitalWrite(red, LOW);
  }else if(tempF >= 60 && tempF < 63) {
    temp_str = "COOL";
    analogWrite(blue, blueBright);
    digitalWrite(green, HIGH);
    digitalWrite(yellow, LOW);
    digitalWrite(red, LOW);
  }else if(tempF >= 63 && tempF < 67) {
    temp_str = "PERFECT";
    digitalWrite(blue, LOW);
    digitalWrite(green, HIGH);
    digitalWrite(yellow, LOW);
    digitalWrite(red, LOW);
  }else if(tempF >= 67 && tempF < 70) {
    temp_str = "WARM";
    digitalWrite(blue, LOW);
    digitalWrite(green, HIGH);
    digitalWrite(yellow, HIGH);
    digitalWrite(red, LOW);
  }else if(tempF >= 70 && tempF < 73) {
    temp_str = "HOT";
    digitalWrite(blue, LOW);
    digitalWrite(green, LOW);
    digitalWrite(yellow, HIGH);
    digitalWrite(red, HIGH);
  }else if(tempF >= 73) {
    temp_str = "YOWZA";
    digitalWrite(blue, LOW);
    digitalWrite(green, LOW);
    digitalWrite(yellow, LOW);
    digitalWrite(red, HIGH);
  }
  
  delay(180000);
  
}
