const int sensorMin = 0;
const int sensorMax = 1024;
void setup() {
  // put your setup code here, to run once:
   pinMode(A0,INPUT);
   Serial.begin(9600);


}

void loop() {
  // put your main code here, to run repeatedly:
  int flameValue = analogRead(A0);
   int range = map(flameValue,sensorMin,sensorMax,0,3);
   Serial.println(flameValue);
    delay (1000);
     switch(range){
      case 0: 
       Serial.println(text);
      digitalWrite(buzzer,HIGH);
      boolean flamePresence = true;
        break;      
      case 1:
        Serial.println(text);
        digitalWrite(buzzer,HIGH);
        boolean flamePresence = true;
        break;
      case 2:
        Serial.println("No nearby fire detected :D");
        boolean flamePresence = false;
        break;
    }
}
