// Define the built-in LED pin. On most Arduino boards, this is pin 13.
const int ledPin = LED_BUILTIN;
const int led2Pin = 14;
const int MotorRedPin = 5;
const int MotorBluePin = 4;
int loopy = 0;

void setup() {
  // Initialize the digital pin as an output.
  pinMode(ledPin, OUTPUT);
  pinMode(led2Pin, OUTPUT);
//  pinMode(MotorRedPin, OUTPUT);
//  pinMode(MotorBluePin, OUTPUT);
}

void loop() {
  // Turn the LED on for 3 milliseconds
  digitalWrite(ledPin, HIGH); // Turn the LED on
  digitalWrite(led2Pin, HIGH);
  // digitalWrite(MotorRedPin, HIGH);
  // digitalWrite(MotorBluePin, LOW);
  delay(3); // Wait for 3 milliseconds

  // Then turn the LED off for the remainder of the 25ms cycle
  // to achieve a 40 Hz blinking frequency
  digitalWrite(ledPin, LOW); // Turn the LED off
  digitalWrite(led2Pin, LOW);
  // digitalWrite(MotorRedPin, LOW);
  // digitalWrite(MotorBluePin, LOW);
  delay(22); // Wait for 22 milliseconds
}
