#define RED_LED 2
#define YLW_LED 4
#define GRN_LED 7


void setup() {
  pinMode(RED_LED, OUTPUT);
  pinMode(YLW_LED, OUTPUT);
  pinMode(GRN_LED, OUTPUT);
}

void loop() {
  digitalWrite(RED_LED, HIGH);
  delay(2000);
  digitalWrite(RED_LED, LOW);
  digitalWrite(YLW_LED, HIGH);
  delay(2000);
  digitalWrite(YLW_LED, LOW);
  digitalWrite(GRN_LED, HIGH);
  delay(2000);
  digitalWrite(GRN_LED, LOW);
  digitalWrite(YLW_LED, HIGH);
  delay(2000);
  digitalWrite(YLW_LED, LOW);
}
