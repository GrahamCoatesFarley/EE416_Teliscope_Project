// Title: Telescope Firmware
// Description: Firmware for Pan/Tilt Telescope System
// Usage: Upload to Arduino and send UART data
// Note: Arduino expects a character 'h' or 'v' depending on which motor to control followed by an int
// that indicates the desired degree rotation for the corresponding motor

#include <Arduino.h>
#include <RotaryEncoder.h>
#include <Servo.h>

// Pin Definitions
#define PIN_IN1 2
#define PIN_IN2 3
#define PWM0_PIN 5  // Linear Actuator PWM
#define PWM1_PIN 6  // DC Motor PWM

// Mathematic Definitions
#define ENC_360 20 // Encoder rotations for 360 degrees
#define GEAR_RATIO 6 // Gear ratio from telescope arm gear to encoder gear
#define H_MAX_ANGLE 36000 //360.00 degrees max horizontal angle
#define V_MAX_ANGLE 9000 // 90.00 degrees max vertical angle 

#define MIN_PULSE 1000 // Min pulse width in microseconds for Motor PWM
#define MAX_PULSE 2000 // Max pulse width in microseconds for Motor PWM

// Pointer to encoder instance
RotaryEncoder *encoder = nullptr;

// Servo object
Servo pwm0;
Servo pwm1;

// Encoder Position Variable
static int enc_pos = 0; // current encoder position
int target_pos = 0; // target encoder position
bool moving = false; // indicates if the telescope arm is currently rotating

// New Position Variable
int newPos;

// UART Received Byte Array
byte incomingBytes[3];

// Encoder pins interrupt function
void checkPosition() {
  encoder->tick();  // checks the state of encoder.
}

// Update linear actuator function
void updateLin(unsigned int degree) {
  // TODO: Change to include trig calculations
  pwm0.writeMicroseconds((int)degree);
}

// Update DC Motor target position
void updateDC(unsigned int degree) {
  // Calculates target encoder position from desired degrees
  target_pos = (int)degree;
}

void setup() {
  Serial.begin(115200);
  while (!Serial)
    ;
  // Serial.println("Program Start\n");
  // End of Debug Serial

  pwm0.attach(PWM0_PIN);
  pwm1.attach(PWM1_PIN);

  encoder = new RotaryEncoder(PIN_IN1, PIN_IN2, RotaryEncoder::LatchMode::TWO03);

  // register interrupt routine
  attachInterrupt(digitalPinToInterrupt(PIN_IN1), checkPosition, CHANGE);
  attachInterrupt(digitalPinToInterrupt(PIN_IN2), checkPosition, CHANGE);

  // Set PWM to default values
  pwm0.writeMicroseconds(1000);  // Linear Actuator PWM set to 0 extension
  pwm1.writeMicroseconds(1500);  // DC Motor PWM set to neutral
}

void loop() {
  newPos = encoder->getPosition();
  if (enc_pos != newPos) {
    // Serial.print("pos:");
    // Serial.print(newPos);
    // Serial.print(" dir:");
    // Serial.println((int)(encoder->getDirection()));
    enc_pos = newPos;
  }

  // Check if the telescope arm has reached the correct position
  if(moving && (enc_pos == target_pos)) {
    pwm1.writeMicroseconds(1500); // Stop DC motor
    moving = false;
  }

  if(!moving && (enc_pos != target_pos)) {
    // Check if arm passed desired position
    if(enc_pos - target_pos < 0) {
      pwm1.writeMicroseconds(1000); // Move motor backwards
    }
    else {
      pwm1.writeMicroseconds(2000); // Move motor forwards
    }
    moving = true;
  }

  if (Serial.available() > 0) {
    Serial.readBytes(incomingBytes, 3);
    char angle_dir = incomingBytes[0];
    unsigned int uart_num = (incomingBytes[1] << 8) | (incomingBytes[2]);
    // pwm0.writeMicroseconds(uart_num);
    if(angle_dir == 'v'){
      updateLin(uart_num);
    }
    if(angle_dir == 'h'){
      updateDC(uart_num);
    }
  }
}
