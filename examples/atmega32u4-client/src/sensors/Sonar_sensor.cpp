#include <Romi32U4.h>
#include "Sonar_sensor.h"
#include <math.h>

unsigned long readingStartTime = 0;
unsigned long duration = 0;

const unsigned int speed_of_sound = 340; // m/s
const float micros_in_sec = pow(10, 6);
const float cm_in_m = pow(10, 2);


void SonarSensor::Init(void)
{
    pinMode(pin_TRIG,OUTPUT);
    pinMode(pin_ECHO, INPUT);   
}

float SonarSensor::PrintData(void)
{
    Serial.println(ReadData());
}

float SonarSensor::ReadData(void)
{
    //assignment 1.2
    //read out and calibrate your sonar sensor, to convert readouts to distance in [cm]

    // Send the TRIG pulse for 10 microseconds
    if(millis() - readingStartTime > 6) {

        // set the time for the start of the measurement window
        readingStartTime = millis();

        // send the pulse
        digitalWrite(pin_TRIG, LOW);
        delayMicroseconds(2);
        digitalWrite(pin_TRIG, HIGH);
        delayMicroseconds(10);
        digitalWrite(pin_TRIG, LOW);
        unsigned long temp_duration = pulseIn(pin_ECHO, HIGH);
        if(temp_duration > 0) {
            duration = temp_duration; // us
        }
    }

    // return the time difference
    float range = duration / micros_in_sec * speed_of_sound * cm_in_m / 2.0;
    // Calibration equation format: y = a*x + b
    // Calibration equation: read_cm = a(distance) + b
    float a = 0.9206;
    float b = 1.3252;
    float distance = (range - b) / a;  

    return distance;

}



