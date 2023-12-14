// Title: Potentiometer test program
// Description: Displays the current position read by each potentiometer
// Usage: Upload to the Arduino and open Serial Monitor to see the current rotation value of each potentiometer
// Note: Potentiometer connections must be made according to wiring diagram

#define POT1_PIN A0
#define POT2_PIN A1

int pot1Val = 0;
int pot2Val = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("Program Begin");
}

void loop() {
  // put your main code here, to run repeatedly:
  pot1Val = analogRead(POT1_PIN);
  pot2Val = analogRead(POT2_PIN);
  Serial.print("Potentiometer 1: ");
  Serial.print(pot1Val);
  Serial.print("        Potentiometer 2: ");
  Serial.println(pot2Val);
}
