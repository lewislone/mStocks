#include <Servo.h>

Servo myServo; 
int pos = 90;
String data = "";

void setup() {
  Serial.begin(115200);
  Serial.println();

  myServo.attach(4); //IO4
  Serial.printf("init pos:%d\n", myServo.read());
  myServo.write(90); 
  Serial.printf("init pos:%d\n", myServo.read());
}

void loop() { 
  
    while (Serial.available() > 0) {
      data += char(Serial.read());
      delay(2);
    }
    
    if (data.length()>0) {
      pos = data.toInt();
      Serial.printf("get value:%d\n", pos);
      data = "";
    }
    
    if(pos != 90) {
      myServo.write(pos);
      delay(50);
      if(pos <= 80)
        myServo.write(pos+10);
      else if(pos >= 100) 
        myServo.write(pos-10);
    }
    
/*
    for (pos = 0; pos <= 1800000; pos ++) { //0~90
       // in steps of 1 degree
       myServo.write(100);
       delay(15);
       //Serial.printf("pos:%d\n", myServo.read());
    }

    delay(100);

    Serial.printf("pos:%d\n", myServo.read());

    for (pos = 180; pos >= 0; pos --) {
        myServo.write(pos);
        delay(15);
    }

    delay(2000);
    Serial.printf("pos:%d\n", myServo.read());
*/
}
