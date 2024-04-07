const int sensorMin = 0;
const int sensorMax = 1024;
const int buzzer = 5;

void setup() {
  // put your setup code here, to run once:
  pinMode(A0,INPUT);
  pinMode(A1,INPUT);
  pinMode(buzzer,OUTPUT);
  Serial.begin(9600);

}

void loop() {
  // put your main code here, to run repeatedly:
  int flameValue = analogRead(A0);
  int smokeValue = analogRead(A1);
  int range = map(flameValue,sensorMin,sensorMax,0,3);
  Serial.println("Smoke: ");  
  Serial.println(smokeValue); delay(500);
  if(smokeValue>210){
      Serial.println("SMOKEEEEEEEE!!!!!!!!!");
      digitalWrite(buzzer,HIGH);
    }
 
  Serial.println("Fire: ");
  switch(range){
      case 0: 
        Serial.println("Close Fire");
        digitalWrite(buzzer,HIGH);
        break;      
      case 1:
        Serial.println("Distant Fire");
        digitalWrite(buzzer,HIGH);
        break;
      case 2:
        Serial.println("No Fire");
        break;
    }
}
