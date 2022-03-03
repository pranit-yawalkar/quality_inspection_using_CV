String InBytes;


void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0){
    InBytes = Serial.readStringUntil('\n');
    if(InBytes == "defective"){
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.write("Gear is defective");
    } 
    else{
      digitalWrite(LED_BUILTIN, LOW);
      Serial.write("Gear is ok");
    }

    if(InBytes == "quit"){
      digitalWrite(LED_BUILTIN, LOW);
      Serial.write("Program Finished...");
    }
    
//    if(InBytes == "ok"){
//      digitalWrite(LED_BUILTIN, LOW);
//      Serial.write("off");
//    } else{
//      Serial.write("Invalid input"); 
//    }
  }
}
