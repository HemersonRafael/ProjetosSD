// Wire Slave Receiver
// by Nicholas Zambetti <http://www.zambetti.com>

// Demonstrates use of the Wire library
// Receives data as an I2C/TWI slave device
// Refer to the "Wire Master Writer" example for use with this

// Created 29 March 2006

// This example code is in the public domain.
int cont = 0;
int x;
#include <Wire.h>

void setup() {
  Wire.begin(8);                // join i2c bus with address #8
  Wire.onReceive(receiveEvent); // register event
  Serial.begin(9600);           // start serial for output
  pinMode(13, OUTPUT);
}

void loop() {
  delay(100);
}

// function that executes whenever data is received from master
// this function is registered as an event, see setup()
void receiveEvent(int howMany) {
  while (1 < Wire.available()) { // loop through all but the last
    char c = Wire.read(); // receive byte as a character
    Serial.print(c);         // print the character
  }
  ++cont;
  if (cont == 1) {
    x = Wire.read();    // receive byte as an integer
    Serial.print("contG = ");
    Serial.print(x);         // print the integer
    Serial.print("  ");
  }
  if (cont == 2) {
    x = Wire.read();    // receive byte as an integer
    Serial.print("contP = ");
    Serial.print(x);         // print the integer
    Serial.print("  ");
  }
   if (cont == 3) {
    x = Wire.read();    // receive byte as an integer
    if(x == 1){
      Serial.println("Esteira ON");
      digitalWrite(13, LOW);
    } else{
        Serial.println("Esteira OFF");
        digitalWrite(13,HIGH);
      }
    cont = 0;
  }
}
