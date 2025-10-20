#include <Servo.h>

Servo gateServo;
int servoPin = 9;   // servo control
int ledPin = 8;     // optional LED

void setup() {
  Serial.begin(9600);
  gateServo.attach(servoPin);
  pinMode(ledPin, OUTPUT);
  gateServo.write(0);          // gate closed
  digitalWrite(ledPin, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == 'O') {          // open signal from Python
      gateServo.write(90);     // open
      digitalWrite(ledPin, HIGH);
      delay(3000);             // stay open 3 s
      gateServo.write(0);      // close
      digitalWrite(ledPin, LOW);
    }
  }
}
