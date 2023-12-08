#ifndef SONAR_SENSOR
#define SONAR_SENSOR

#include <Romi32U4.h>

class SonarSensor{
    private:
        const int pin_TRIG = 12;
        const int pin_ECHO = 7;
    public:
        void Init(void); 
        float ReadData(void); 
        float PrintData(void);
};

#endif