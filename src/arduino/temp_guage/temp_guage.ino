/*
Temperature Guage

Based on the current temperature, light up LED(s) to indicate, within a range,
the current temperature. Designed for normal housing temperatures.

From cold to warm:
b --> bg --> g --> gy --> y --> yr --> r

Author: Ethan Hart
Date: 2015-01-11
*/

const int sensorPin = A0; // TMP36 sensor pin
char recMsg = '0';
int blue = 3; // blue and green are "swapped" so blue can run off pin 3 to use analogWrite()
int blueBright = 10; // blue needs to be dim: otherwise, it overpowers green light
int green = 2;
int yellow = 4;
int red = 5;

void setup() {
  Serial.begin(9600); // open a serial port

  // Initialize output pins for LEDs
  for(int pinNumber = 2; pinNumber<6; pinNumber++) {
    pinMode(pinNumber, OUTPUT);
    digitalWrite(pinNumber, LOW);
  }
  
}

void loop() {
  
  while(Serial.available() > 0) {
    recMsg = Serial.read();
  }

  // check to see if python has requested temp
  if (recMsg != '0') {
    int sensorVal = analogRead(sensorPin);
  
    // convert ADC reading to voltage
    float voltage = (sensorVal/1024.0) * 5.0;

    // convert voltage to temperature
    float tempC = (voltage - 0.5) * 100; // get temp in Celcius
    float tempF = (tempC * 9.0/5.0) + 32; // temp in Fahrenheit (because USA)

    Serial.println(tempF);
    String temp_str;

    if(tempF < 60) {
      analogWrite(blue, blueBright);
      digitalWrite(green, LOW);
      digitalWrite(yellow, LOW);
      digitalWrite(red, LOW);
    }else if(tempF >= 60 && tempF < 63) {
      analogWrite(blue, blueBright);
      digitalWrite(green, HIGH);
      digitalWrite(yellow, LOW);
      digitalWrite(red, LOW);
    }else if(tempF >= 63 && tempF < 67) {
      digitalWrite(blue, LOW);
      digitalWrite(green, HIGH);
      digitalWrite(yellow, LOW);
      digitalWrite(red, LOW);
    }else if(tempF >= 67 && tempF < 70) {
      digitalWrite(blue, LOW);
      digitalWrite(green, HIGH);
      digitalWrite(yellow, HIGH);
      digitalWrite(red, LOW);
    }else if(tempF >= 70 && tempF < 73) {
      digitalWrite(blue, LOW);
      digitalWrite(green, LOW);
      digitalWrite(yellow, HIGH);
      digitalWrite(red, HIGH);
    }else if(tempF >= 73) {
      digitalWrite(blue, LOW);
      digitalWrite(green, LOW);
      digitalWrite(yellow, LOW);
      digitalWrite(red, HIGH);
    }
 
  }
}
