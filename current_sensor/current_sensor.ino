#include "ACS712.h"

ACS712 sensor(ACS712_30A, A1);

void setup() {
  Serial.begin(9600);
  sensor.calibrate();
}

void loop() {
  float I = sensor.getCurrentDC();
  Serial.println(I);
  delay(1000);
}
