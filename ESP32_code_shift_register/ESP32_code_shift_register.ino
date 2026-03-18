const int dataPin  = 23;  
const int latchPin = 5;   
const int clockPin = 18;  

void setup() {
  Serial.begin(115200);
  pinMode(dataPin, OUTPUT);
  pinMode(latchPin, OUTPUT);
  pinMode(clockPin, OUTPUT);
}

// Your custom wiring fix (LED 1 is on Q7)
byte applyWiringFix(byte logical) {
  byte physical = 0;
  if (bitRead(logical, 0)) bitSet(physical, 7); // Logical Bit 0 (Resistor) -> Q7
  physical |= (logical >> 1);                  // Bits 1-7 (Others) -> Q0-Q6
  return physical;
}

void loop() {
  if (Serial.available() > 0) {
    // Read the raw byte sent from Python
    byte incomingBitmask = Serial.read();

    // Push to hardware
    digitalWrite(latchPin, LOW);
    shiftOut(dataPin, clockPin, MSBFIRST, applyWiringFix(incomingBitmask));
    digitalWrite(latchPin, HIGH);
  }
}