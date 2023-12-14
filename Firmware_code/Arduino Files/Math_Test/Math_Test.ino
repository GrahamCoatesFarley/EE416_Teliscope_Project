// Title: Math test program
// Description: Tests feedback loop used in the telescope firmware
// Usage: Upload to the Arduino and move the potentiometer rotation to see if the appropriate control statements are reached
// Note: Potentiometer connections must be made according to wiring diagram
// Note: Assumes that the potentiometer can be manually rotated (not connected to motors)

#define POT1_PIN A0
#define POT2_PIN A1

#define GEAR_RATIO 6 // Gear ratio from horizontal telescope arm gear to potentiometer gear
#define H_MIN_ANGLE 0 // 0.00 degrees min horizontal angle
#define V_MIN_ANGLE 0 // 0.00 degrees min vertical angle 
#define H_MAX_ANGLE 36000 //360.00 degrees max horizontal angle
#define V_MAX_ANGLE 9000 // 90.00 degrees max vertical angle 
#define H_POT_VAL_0 5 // Potentiometer value for 0 degree horizontal rotation
#define V_POT_VAL_0 0 // Potentiometer value for 0 degree vertical rotation
#define H_POT_ROT 101 // Change in horizontal potentiometer value for 1 rotation
#define H_POT_VAL_360 H_POT_ROT*GEAR_RATIO // Potentiometer value for 360 degree horizontal rotation
#define V_POT_VAL_90 305 // Potentiometer value for 90 degeree vertical rotation
#define H_POT_TOL 2 // +/- Tolerance in horizontal potentiometer value (total horizontal error is twice this value)
#define V_POT_TOL 2 // +/- Tolerance in vertical potentiometer value (total vertical error is twice this value)
static float H_SLOPE = float(H_POT_VAL_360-H_POT_VAL_0)/float(H_MAX_ANGLE-H_MIN_ANGLE); // Slope for mapping horizontal degree to potentiometer value
static float H_OFFSET = H_POT_VAL_360-H_SLOPE*H_MAX_ANGLE; // Offset for mapping horizontal degree to potentiometer value
static float V_SLOPE = float(V_POT_VAL_90-V_POT_VAL_0)/float(V_MAX_ANGLE-V_MIN_ANGLE); // Slope for mapping vertical degree to potentiometer value
static float V_OFFSET = V_POT_VAL_90-V_SLOPE*V_MAX_ANGLE; // Offset for mapping horizontal degeree to potentiometer value

// Motor States
#define MOTOR_STOPPED 0
#define MOTOR_FORWARDS 1
#define MOTOR_BACKWARDS 2

unsigned int hdegree = 18000;
unsigned int vdegree = 4500;
long h_target = long(H_SLOPE*hdegree + H_OFFSET);
long v_target = long(V_SLOPE*vdegree + V_OFFSET);

unsigned int v_pot1Val = 0; // Value of elevation potentiometer
unsigned int h_pot2Val = 0;
int v_state = MOTOR_STOPPED;
int h_state = MOTOR_STOPPED;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.print("Horizontal Target: ");
  Serial.println(h_target);
  Serial.print("Vertical Target: ");
  Serial.println(v_target);
  delay(2000);
}

void loop() {
  v_pot1Val = analogRead(POT1_PIN);
  h_pot2Val = analogRead(POT2_PIN);

  Serial.print("v_pot1Val: ");
  Serial.print(v_pot1Val);
  Serial.print("      h_pot2Val: ");
  Serial.println(h_pot2Val);

  Serial.println(abs(v_pot1Val - v_target));
  if((v_state != MOTOR_STOPPED) && (abs(v_pot1Val - v_target) <= V_POT_TOL)) {
    Serial.println("Vertical Motor Stopped");
    v_state = MOTOR_STOPPED;
  } 
  else if((abs(v_pot1Val - v_target) > V_POT_TOL)) {
    Serial.println("Vertical If statement reached");
    // Check if arm passed desired position
    if((v_state != MOTOR_BACKWARDS) && (v_pot1Val - v_target > 0)) {
      Serial.println("Vertical Motor Backwards");
      v_state = MOTOR_BACKWARDS;
    }
    else if ((v_state != MOTOR_FORWARDS) && (v_pot1Val - v_target < 0)){
      Serial.println("Vertical Motor Forwards");
      v_state = MOTOR_FORWARDS;
    }
  }

  if((h_state != MOTOR_STOPPED) && (abs(h_pot2Val - h_target) <= H_POT_TOL)) {
    Serial.println("Horizontal Motor Stopped");
    h_state = MOTOR_STOPPED;
  }
  else if((abs(h_pot2Val - h_target) > H_POT_TOL)) {
    Serial.println("Horizontal If statement reached");
    // Check if arm passed desired position
    if((h_state != MOTOR_BACKWARDS) && (h_pot2Val - h_target < 0)) {
      Serial.println("Horizontal Motor Backwards");
      h_state = MOTOR_BACKWARDS;
    }
    else if ((h_state != MOTOR_FORWARDS) && (h_pot2Val - h_target > 0)){
      Serial.println("Horizontal Motor Forwards");
      h_state = MOTOR_FORWARDS;
    }
  }
  delay(1000);
}
