#include <Servo.h>
Servo myservo;
void setup() {
  // put your setup code here, to run once:
  myservo.attach(6);
}

void loop() {
  // put your main code here, to run repeatedly:
  myservo.write(180);
  delay(140);
  myservo.write(90);   
  delay(5000);
}
