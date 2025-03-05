#include <Servo.h>
#include <Serial.h>

Servo xServo;
Servo yServo;

void setup() {
  Serial.begin(9600);
  
  xServo.attach(2);
  yServo.attach(3);
  xServo.write(0);
  yServo.write(0);
} 

void loop() {
  if (Serial.available() > 0) {
    String coordinates = Serial.readStringUntil('\n');
    int commaIndex = coordinates.indexOf(',');

    if (commaIndex > 0) {
      int x_coordinate = coordinates.substring(0, commaIndex).toInt();
      int y_coordinate = coordinates.substring(commaIndex + 1).toInt();

      // Adjustments for motor and camera placement
      
      // x_coordinate = x_coordinate - 10;
      y_coordinate = y_coordinate - 10;
      
      if (y_coordinate < 0) {
        y_coordinate = 0;
      }

      if (x_coordinate < 0) {
        x_coordinate = 0;
      }

      xServo.write(x_coordinate);
      yServo.write(y_coordinate);
    }
  }
}
