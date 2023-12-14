// Title: UART Test
// Description: Test program to confirm UART functionality
// Usage: Connect to Arduino using Python UART test program, send two int values (two bytes each, four bytes total) for hardware to interpret.
// After sending int values, LED on Arduino will blink the number that was sent with a pause in between numbers.

byte incomingBytes[2];
// byte testBytes[] = {0x8C, 0xA0};
// byte testBytes[] = {0x00, 0x00, 0x80, 0x00};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  while (!Serial)
    ;
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  // unsigned int number = (testBytes[0]<<8)|(testBytes[1]);
  // Serial.println(number);
}

void loop() {
  // put your main code here, to run repeatedly:
  // send data only when you receive data:
  if (Serial.available() > 0) {
    // read the incoming byte:
    // incomingBytes = Serial.read();
    Serial.readBytes(incomingBytes, 2);

    // say what you got:
    // Serial.print("I received: ");
    // Serial.println(incomingByte, DEC);

    // int number = int((incomingBytes[0]<<24)|(incomingBytes[1]<<16)|(incomingBytes[2]<<8)|(incomingBytes[3]));
    // int number = int((unsigned char)(incomingBytes[0]) << 24 | (unsigned char)(incomingBytes[1]) << 16 | (unsigned char)(incomingBytes[2]) << 8 | (unsigned char)(incomingBytes[3]));
    unsigned int number = (incomingBytes[0]<<8)|(incomingBytes[1]);
    // int number = incomingBytes[0];

    // if(number == 36000)
    // {
    //   digitalWrite(LED_BUILTIN, HIGH);
    // }
    for(int i = 0; i < number; i++) {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(500);
      digitalWrite(LED_BUILTIN, LOW);
      delay(500);
    }

    // delay(1000);
  }
}
