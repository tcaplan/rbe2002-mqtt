#include <Romi32U4.h>
#include "IR_sensor.h"

void IRsensor::Init(void)
{
    pinMode(pin_IR, INPUT);
}

float IRsensor::PrintData(void)
{
    Serial.println(ReadData());
}

float IRsensor::ReadData(void)
{
  //assignment 1.1
  //read out and calibrate your IR sensor, to convert readouts to distance in [cm]

  int adc = analogRead(pin_IR);
  
  float v_ref = 5.0; // V
  int bits = pow(2, 10) - 1;

  // Calibration equation format: adc = a*(1/distance) + b
  float a = 4631.1;
  float b = 37.177;
  float cm = 1 / ((adc - b) / a);

  return cm;

}

