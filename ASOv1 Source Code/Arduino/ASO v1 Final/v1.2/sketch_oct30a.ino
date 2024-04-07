#include <SoftwareSerial.h>  
#include <Servo.h>

//Pi communication essentials
char dataString[50] = {0};
int raspiState = 0; // 0:sleep, 1:take a pic, 2:no smoke, 3:smoke!
boolean smokePresence = false;
boolean flamePresence = false;
boolean mqPresence = false;
// Arduino shit
const int sensorMin = 0;
const int sensorMax = 1024;
const int buzzer = 5;
SoftwareSerial mySerial(3, 2); //SIM800L Tx & Rx is connected to Arduino #3 & #2
Servo myservo;
String text, opp;
//String text;
//int degree, unsa;
int pos;
void setup() {
  
  pinMode(A0,INPUT);
  pinMode(A1,INPUT);
  pinMode(buzzer,OUTPUT);
  myservo.attach(6);
  Serial.begin(9600);  //Starting serial communication
  Serial.println("<Serial communication has begun>  ");
  while (raspiState == 0){
    listenToPi();
  }
  if (raspiState == 1){  
    Serial.println("<PiDuino is Ready>");
    sendMessage("A.S.O. is operational");
  }
  delay(1000);
}
  
void loop() {
  for (pos = 1; pos < 4; pos ++){ 
    monitor();
    
  }
}
void takePic() {
  //delay(700);
  raspiState = 1;
  Serial.println("<Taking a picture>");
  //int state = 0;
  while (raspiState == 1){
    listenToPi();
    listenToPi();//
    if (raspiState == 2){
    smokePresence = false;
    Serial.print(raspiState);
    Serial.println("No distant smoke detected :D");

    //se ndToPi();   
    }
    else if (raspiState == 3){
        smokePresence = true;
        //raspiState = 1;
        Serial.print(raspiState);
        Serial.println("Smoke presence is detected!");
        //sendToPi();
    }
 
  }
  
  //Serial.flush();
  //while (raspiState == 1){  
    //listenToPi();
  //}
  //Serial.println("<raspiState = " + String(raspiState) + ">");
  
  
}
void listenToPi() {
    if(Serial.available()) {      //From RPi to Arduino
    char check = Serial.read();
    raspiState = check - '0';  //conveting the value of chars to integer
    //Serial.println(raspiState);
    }
} 
void sendToPi(){
  sprintf(dataString,"%02X",raspiState); // convert a value to hexa 
  Serial.println(dataString);   // send the data;
}

void sendMessage(String message) {
  //Serial.println("<Sending message>");
  
  mySerial.println("AT"); //Once the handshake test is successful, it will back to OK
  //Serial.println("AT");
  updateSerial();

  mySerial.println("AT+CMGF=1"); // Configuring TEXT mode
  updateSerial();
  mySerial.println("AT+CMGS=\"+639087179343\"");//change ZZ with country code and xxxxxxxxxxx with phone number to sms
  updateSerial();
  mySerial.print(message); //text content
  Serial.println("");
  updateSerial();
  mySerial.write(26);
}
void updateSerial()
{
  delay(500);
  while (Serial.available()) 
  {
    mySerial.write(Serial.read());//Forward what Serial received to Software Serial Port
  }
  while(mySerial.available()) 
  {
    Serial.write(mySerial.read());//Forward what Software Serial received to Serial Port
  }
}
void turnServo ( int type, int tuyok) {
  //Serial.println("<Turning servo>");
  myservo.write(type);
  delay(tuyok);
  //while(raspiState == 0){
    //listenToPi();
  myservo.write(90);
  //delay(1);
  //}
}
void MQ2() {
  Serial.println("<Using MQ2 sensor>");

  //boolean mq = false;
  //mqPresence = false;
  int smokeNaa;
  for (int i = 0; i < 4; i ++){
    int smokeValue = analogRead(A1);
    
    Serial.println(smokeValue);
    if (smokeValue > 152)  {
      //digitalWrite(buzzer,HIGH);
      //boolean mq = true;
      smokeNaa = smokeNaa + 1;
      //mqPresence = true;
      //Serial.println(text);
      //
    }
    
    delay(125);
  }
  if (smokeNaa > 1) {
      //digitalWrite(buzzer,HIGH);
      //Serial.println("No nearby smoke detected :D");
      mqPresence = true;
       text = "MQ-2 SMOKE Sensor has detected possible nearby smoke! Verifying ... ";
      digitalWrite(buzzer,HIGH);
      delay(250);
      digitalWrite(buzzer,LOW);
      sendMessage(text);
    }
    else{
      mqPresence = false;
       text = "No nearby smoke detected =D";
       //sendMessage(text);
    }
 
 
  
  delay(1000);
  
}
void IRF(){
  Serial.println("<Using IR Flame sensor>");
  //flamePresence = false;
  
  for (int i = 0; i < 4 ; i ++ ) {
    int flameValue = analogRead(A0);
    int range = map(flameValue,sensorMin,sensorMax,0,3);
    Serial.println(flameValue);
    switch(range){ 
      case 0: 
       //Serial.println(text);
       //digitalWrite(buzzer,HIGH);
       //Serial.println("Nearby fire detected!");
       flamePresence = true;
        break;      
      case 1:
        Serial.println("Nearby fire detected!");
        //digitalWrite(buzzer,HIGH);
         flamePresence = true;
        break;
      case 2:
        Serial.println("No nearby fire detected :D");
         flamePresence = false;
        break;
    }
    
  delay(125);
  }
  Serial.println(String (flamePresence));
  text = "IR FLAME sensor has detected possible nearby fire! Verifying...";
  if (flamePresence == true){
    //sendMessage(text);
    digitalWrite(buzzer,HIGH);
    delay(250);
    digitalWrite(buzzer,LOW);
    sendMessage(text);
  }
  else{
    text = "No nearby flame detected =D";
    //sendMessage(text);
    //senMessage("IR FLAME sensor: No nearby flame has been detected. Verifying...");
  }
  delay(1000);
  
}
void monitor() {
  //takePic();
  
  IRF();
  MQ2();
  raspiState = 0;
  takePic();

  

  //Serial.println(pos);
  //String text, opp;
  int tayp; int count; int tayp2; int count2; int tayp3; int count3;
  switch(pos){
    case 1:
       text = "Smoke presence detected NORTH/POSITION 1 of A.S.O. Verify findings IMMEDIATELY!";
       opp = "Smoke presence detected SOUTH/POSITION 3 of A.S.O  Verify findings IMMEDIATELY!";
       tayp = 80; count = 4500; tayp2 = 100; count2 = 9000; tayp3 = 80; count3 = 4500; 
       break;
    case 2:
       text = "Smoke presence detected EAST/POSITION 2 of A.S.O Verify findings IMMEDIATELY!";
       opp = "Smoke presence detected WEST/POSITION 4 of A.S.O Verify findings IMMEDIATELY!";
       tayp = 80; count = 4500; tayp2 = 100; count2 = 9000; tayp3 = 80; count3 = 13500;
       break;
    case 3:
       text = "Smoke presence detected SOUTH/POSITION 3 of A.S.O  Verify findings IMMEDIATELY!";
       opp = "Smoke presence detected NORTH/POSITION 1 of A.S.O. Verify findings IMMEDIATELY!";
       tayp = 100; count = 13500; tayp2 = 100; count2 = 9000; tayp3 = 100; count3 = 9000; 
       break;
    case 4: 
       text = "Smoke presence detected NORTH/POSITION 1 of A.S.O Verify findings IMMEDIATELY!";
       opp = "Smoke presence detected SOUTH/POSITION 3 of A.S.O Verify findings IMMEDIATELY!";
       tayp = 100; count = 9000; tayp2 = 80; count2 = 9000; tayp3 = 100; count3 = 13500;
      break;
    case 5:
     text = "Smoke presence detected WEST/POSITION 4 of A.S.O Verify findings IMMEDIATELY!";
       opp = "Smoke presence detected EAST/POSITION 2 of A.S.O Verify findings IMMEDIATELY!";
      tayp = 100; count = 9000; tayp2 = 80; count2 = 9000; tayp3 = 100; count = 13500;
      break;
     case 6: 
      text = "Smoke presence detected SOUTH/POSITION 3 of A.S.O Verify findings IMMEDIATELY!";
       opp = "Smoke presence detected NORTH/POSITION 1 of A.S.O Verify findings IMMEDIATELY!";
       tayp = 80; count = 9000; tayp2 = 80; count2 = 9000; tayp3 = 80; count3 = 9000;
       break;
  }
  
  if (smokePresence == true){
    
    digitalWrite(buzzer,HIGH);
    delay(3100);
    digitalWrite(buzzer,LOW);
    sendMessage(text);
  }
    
  if ((flamePresence == true) || ( mqPresence == true)){
    //Serial.println("Going round two");
    turnServo(tayp2, count2); //goes to the opposite side
    takePic();
    if (smokePresence == true){
      digitalWrite(buzzer,HIGH);
      delay(3100);
      digitalWrite(buzzer,LOW);
      sendMessage(text);
    }
    //Serial.println(tayp3);
    //Serial.println(count3);
    //(tayp3,count3);
    flamePresence = false;
    mqPresence = false;
    turnServo(tayp3, count3);
  }
  
  turnServo( tayp,  count);
  
}
