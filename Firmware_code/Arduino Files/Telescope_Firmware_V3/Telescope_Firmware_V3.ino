// Title: Telescope Firmware V3
// Description: Final Firmware for Pan/Tilt Telescope System
// Usage: Upload to Arduino and send UART data
// Note: Arduino expects a character 'h' or 'v' depending on which motor to control followed by an int
// that indicates the desired degree rotation for the corresponding motor

#include <Arduino.h>
#include <Servo.h>

// Pin Definitions
#define POT1_PIN A0 // Telescope Arm Elevation Potentiometer Wiper Pin
#define POT2_PIN A1 // Telesceop Arm Azimuth Poteniometer Wiper Pin
#define PWM0_PIN 5  // Linear Actuator PWM
#define PWM1_PIN 6  // DC Motor PWM

// Mathematic Definitions
#define GEAR_RATIO 3 // Gear ratio from horizontal telescope arm gear to potentiometer gear
#define H_MIN_ANGLE 0 // 0.00 degrees min horizontal angle
#define V_MIN_ANGLE 0 // 0.00 degrees min vertical angle 
#define H_MAX_ANGLE 36000 //360.00 degrees max horizontal angle
#define V_MAX_ANGLE 9000 // 90.00 degrees max vertical angle 
#define H_POT_VAL_0 507 // Potentiometer value for 0 degree horizontal rotation
#define V_POT_VAL_0 45 // Potentiometer value for 0 degree vertical rotation
#define H_POT_ROT 103 // Change in horizontal potentiometer value for 1 rotation
#define H_POT_VAL_360 H_POT_VAL_0 + H_POT_ROT*GEAR_RATIO // Potentiometer value for 360 degree horizontal rotation
#define V_POT_VAL_90 425 // Potentiometer value for 90 degree vertical rotation
#define H_POT_TOL 1 // +/- Tolerance in horizontal potentiometer value (total horizontal error is twice this value)
#define V_POT_TOL 0 // +/- Tolerance in vertical potentiometer value (total vertical error is twice this value)
static float H_SLOPE = float(H_POT_VAL_360-H_POT_VAL_0)/float(H_MAX_ANGLE-H_MIN_ANGLE); // Slope for mapping horizontal degree to potentiometer value
static float H_OFFSET = H_POT_VAL_360-H_SLOPE*H_MAX_ANGLE; // Offset for mapping horizontal degree to potentiometer value
static float V_SLOPE = float(V_POT_VAL_90-V_POT_VAL_0)/float(V_MAX_ANGLE-V_MIN_ANGLE); // Slope for mapping vertical degree to potentiometer value
static float V_OFFSET = V_POT_VAL_90-V_SLOPE*V_MAX_ANGLE; // Offset for mapping horizontal degeree to potentiometer value

// Speed of the motors in repective directions can be adjusted by changing these values
// 1500 pulse width corresponds to no motor movement
#define LIN_MIN_PULSE 1300 // Min pulse width in microseconds for Lin Motor PWM (backwards)
#define LIN_MAX_PULSE 1700 // Max pulse width in microseconds for Lin Motor PWM (forwards)
#define DC_MIN_PULSE 1300 // Min pulse width in microseconds for DC Motor PWM (backwards)
#define DC_MAX_PULSE 1800 // Max pulse width in microseconds for DC Motor PWM (forwards)

// Initial Degree Values
static unsigned int INITIAL_V = 4500;
static unsigned int INITIAL_H = 0;

// Motor States
#define MOTOR_STOPPED 0
#define MOTOR_FORWARDS 1
#define MOTOR_BACKWARDS 2

// Servo object
Servo pwm0;
Servo pwm1;

// Potentiometer Position Variables
unsigned int v_pot1Val = 0; // Value of elevation potentiometer
unsigned int h_pot2Val = 0; // Value of azimuth potentiometer
long v_target = 0; // Target elevation potentiometer value
long h_target = 0; // Target azimuth potentiometer value
bool v_state = MOTOR_STOPPED; // Indicates state of the linear actuator DC motor
bool h_state = MOTOR_STOPPED; // Indicates state of the horizontal rotation DC motor

// UART Received Byte Array
byte incomingBytes[3];

// Update linear actuator function
void updateLin(unsigned int degree) {
  // Calculate new vertical target potentiometer position from desired degree rotation
  v_target = long(V_SLOPE*degree + V_OFFSET);
}

// Update DC Motor target position
void updateDC(unsigned int degree) {
  // Calculates new horizontal target potentiometer position from desired degree rotation
  h_target = long(H_SLOPE*degree + H_OFFSET);
}

void setup() {
  Serial.begin(115200);
  while (!Serial)
    ;
    
  // End of Debug Serial

  pwm0.attach(PWM0_PIN);
  pwm1.attach(PWM1_PIN);

  // Set PWM to default values
  pwm0.writeMicroseconds(1500);  // Linear Actuator PWM set to neutral
  pwm1.writeMicroseconds(1500);  // DC Motor PWM set to neutral

  // Initialize target values to 0 degrees
  updateLin(INITIAL_V);
  updateDC(INITIAL_H);
}

void loop() {
  // Update potentiometer values
  v_pot1Val = analogRead(POT1_PIN);
  h_pot2Val = analogRead(POT2_PIN);

  // Vertical Rotation Linear Actuator Control Loop
  if(abs(v_pot1Val - v_target) <= V_POT_TOL) {
    pwm0.writeMicroseconds(1500); // Stop Linear Actuator motor
    v_state = MOTOR_STOPPED;
  }
  else if(v_pot1Val - v_target > 0) {
    pwm0.writeMicroseconds(LIN_MIN_PULSE); // Move motor backwards
    v_state = MOTOR_BACKWARDS;
  }
  else if (v_pot1Val - v_target < 0) {
    pwm0.writeMicroseconds(LIN_MAX_PULSE); // Move motor forwards
    v_state = MOTOR_FORWARDS;
  }

  // Horizontal Rotation DC Motor Control Loop
  if(abs(h_pot2Val - h_target) <= H_POT_TOL) {
    pwm1.writeMicroseconds(1500); // Stop DC motor
    h_state = MOTOR_STOPPED;
  }
  else if(h_pot2Val - h_target > 0) {
    pwm1.writeMicroseconds(DC_MIN_PULSE); // Move motor backwards
    h_state = MOTOR_BACKWARDS;
  }
  else if (h_pot2Val - h_target < 0) {
    pwm1.writeMicroseconds(DC_MAX_PULSE); // Move motor forwards
    h_state = MOTOR_FORWARDS;
  }

  // Read from UART
  if (Serial.available() > 0) {
    Serial.readBytes(incomingBytes, 3);
    char angle_dir = incomingBytes[0];
    unsigned int uart_num = (incomingBytes[1] << 8) | (incomingBytes[2]);
    if(angle_dir == 'v'){
      updateLin(uart_num);
    }
    if(angle_dir == 'h'){
      updateDC(uart_num);
    }
  }
}
