// Title: PWM test program
// Description: uses Pins 5 and 6 to send a PWM signal to the DC motor and Linear actuator
// Usage: Change the microseconds to change the speed of DC motor or extension of Linear actuator
// Note: Motor connections must be made according to wiring diagram

#include <Servo.h>

#define PWM0_PIN 5  // Linear Actuator PWM
#define PWM1_PIN 6  // DC Motor PWM

// Servo object
Servo pwm0;
Servo pwm1;

void setup() {
  Serial.begin(115200);

  // put your setup code here, to run once:
  pwm0.attach(PWM0_PIN);
  pwm1.attach(PWM1_PIN);

  pwm0.writeMicroseconds(1500);  // Linear Actuator PWM set to 0 extension
  pwm1.writeMicroseconds(1500);  // DC Motor PWM set to neutral

  // for(int count = 2000; count > 1000; count--){
  //   Serial.println(count);
  //   pwm0.writeMicroseconds(count);
  //   delay(2000);
  // }
}

void loop() {
  // put your main code here, to run repeatedly:
}
