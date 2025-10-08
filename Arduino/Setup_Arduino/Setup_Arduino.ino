#include <WiFiS3.h>

const char* ssid = "ArduinoAP";
const char* pass = "123456789";
const uint8_t apChannel = 1;
WiFiServer server(8080);


//PIN MAPPING
//First signal 
#define LED_R1 2
#define LED_Y1 4
#define LED_G1 7

//Second signal
#define LED_R2 8
#define LED_Y2 12
#define LED_G2 13

String inbuf;

/**
 * @brief Turns off all LEDs for both traffic light signals.
 *
 * This function ensures that every LED (red, yellow, green) 
 * in both Signal 1 and Signal 2 is set to LOW, effectively 
 * switching off all lights.
 */
void allOff()
{
  // Turn off all LEDs of the first signal
  digitalWrite(LED_R1, LOW);
  digitalWrite(LED_Y1, LOW);
  digitalWrite(LED_G1, LOW);

  // Turn off all LEDs of the second signal
  digitalWrite(LED_R2, LOW);
  digitalWrite(LED_Y2, LOW);
  digitalWrite(LED_G2, LOW); 
}


/**
 * @brief Forces all signals to red (safe state).
 *
 * Sets both Signal 1 and Signal 2 to red, turning off yellow and green.
 * Useful as an initial or transitional safety condition.
 */
void allRed()
{
  digitalWrite(LED_G1, LOW);
  digitalWrite(LED_Y1, LOW);
  digitalWrite(LED_R1, HIGH);
  digitalWrite(LED_G2, LOW);
  digitalWrite(LED_Y2, LOW);
  digitalWrite(LED_R2, HIGH);
}

/**
 * @brief Configure GPIO pins for both traffic light signals.
 *
 * Initializes all LED pins (red, yellow, green) for Signal 1 and Signal 2
 * as outputs, then ensures every LED starts in the OFF state by calling
 * allOff().
 *
 * @pre LED_R1, LED_Y1, LED_G1, LED_R2, LED_Y2, LED_G2 must be defined.
 * @post All LEDs are configured as OUTPUT and set to LOW.
 * @note Call this once in setup() before driving any LEDs.
 */
void setupPins()
{
  // Signal 1 LED directions
  pinMode(LED_R1, OUTPUT);
  pinMode(LED_Y1, OUTPUT);
  pinMode(LED_G1, OUTPUT);

  // Signal 2 LED directions
  pinMode(LED_R2, OUTPUT);
  pinMode(LED_Y2, OUTPUT);
  pinMode(LED_G2, OUTPUT);

  allRed();
}



/**
 * @brief Set the active light for a specific traffic signal.
 *
 * This function turns ON only one LED (Red, Yellow, or Green)
 * based on the character provided, while ensuring the other two
 * LEDs are turned OFF.
 *
 * @param R The pin number of the red LED.
 * @param Y The pin number of the yellow LED.
 * @param G The pin number of the green LED.
 * @param c The character representing the color to turn ON:
 *          - `'R'` → Red
 *          - `'Y'` → Yellow
 *          - `'G'` → Green
 *
 * @note Any character other than `'R'`, `'Y'`, or `'G'` will turn all LEDs OFF.
 * @pre The pin modes must have been configured as OUTPUT.
 * @post Exactly one LED corresponding to @p c will be HIGH, others LOW.
 */
void setLight(int R, int Y, int G, char c)
{
  digitalWrite(R, c == 'R');
  digitalWrite(Y, c == 'Y');
  digitalWrite(G, c == 'G');
}



/**
 * @brief Safe transition to a target green using an all-red and yellow phase.
 *
 * Executes a safety sequence before setting the target green:
 * 1) All signals to red for a short interval.
 * 2) Yellow on the target direction for a short interval.
 * 3) Final target: one direction green, the other red.
 *
 * @param which '1' for Signal 1 (G1), '2' for Signal 2 (G2).
 * @param yellow_ms Duration of the yellow phase in milliseconds.
 * @param red_ms Duration of the all-red phase in milliseconds.
 *
 * @pre Pins configured and LEDs connected as mapped.
 * @post Target direction shows green, the opposite shows red.
 */
void safeGo(char which, unsigned long yellow_ms = 700, unsigned long red_ms = 700)
{
  if (which == '1')
  {
    setLight(LED_R2, LED_Y2, LED_G2, 'Y');
    delay(yellow_ms);
    setLight(LED_R2, LED_Y2, LED_G2, 'R');
    allRed();
    delay(red_ms);
    setLight(LED_R1, LED_Y1, LED_G1, 'G');
    setLight(LED_R2, LED_Y2, LED_G2, 'R');
  }
  else
  {
    setLight(LED_R1, LED_Y1, LED_G1, 'Y');
    delay(yellow_ms);
    setLight(LED_R1, LED_Y1, LED_G1, 'R');
    allRed();
    delay(red_ms);
    setLight(LED_R1, LED_Y1, LED_G1, 'R');
    setLight(LED_R2, LED_Y2, LED_G2, 'G');
  }
}



/**
 * @brief Parse and execute LED control commands received from the Raspberry Pi.
 *
 * Supported commands (case-insensitive, newline-terminated):
 * - "R1" / "Y1" / "G1" → set Signal 1 (Red / Yellow / Green)
 * - "R2" / "Y2" / "G2" → set Signal 2 (Red / Yellow / Green)
 * - "S:XY"             → combined command (X for Signal 1, Y for Signal 2; X,Y∈{R,Y,G})
 * - "ALL:OFF"          → turn off all LEDs
 * - "ALL:RED"          → force all-red safe state
 * - "SAFE:G1"          → safe transition to green on Signal 1
 * - "SAFE:G2"          → safe transition to green on Signal 2
 *
 * Unknown or malformed commands return "ERR".
 *
 * @param raw The raw command string to be processed.
 * @return An acknowledgment string ("ACK <cmd>" or "ERR").
 */
String handleCmd(const String& raw)
{
  String cmd = raw;
  cmd.trim();
  cmd.toUpperCase();

  if (cmd == "R1") { setLight(LED_R1, LED_Y1, LED_G1, 'R'); return "ACK R1"; }
  if (cmd == "Y1") { setLight(LED_R1, LED_Y1, LED_G1, 'Y'); return "ACK Y1"; }
  if (cmd == "G1") { setLight(LED_R1, LED_Y1, LED_G1, 'G'); return "ACK G1"; }

  if (cmd == "R2") { setLight(LED_R2, LED_Y2, LED_G2, 'R'); return "ACK R2"; }
  if (cmd == "Y2") { setLight(LED_R2, LED_Y2, LED_G2, 'Y'); return "ACK Y2"; }
  if (cmd == "G2") { setLight(LED_R2, LED_Y2, LED_G2, 'G'); return "ACK G2"; }

  if (cmd == "ALL:OFF") { allOff(); return "ACK ALL:OFF"; }
  if (cmd == "ALL:RED") { allRed(); return "ACK ALL:RED"; }

  if (cmd.startsWith("S:") && cmd.length() == 4)
  {
    char a = cmd.charAt(2);
    char b = cmd.charAt(3);
    setLight(LED_R1, LED_Y1, LED_G1, a);
    setLight(LED_R2, LED_Y2, LED_G2, b);
    return "ACK S:XY";
  }

  if (cmd == "SAFE:G1") { safeGo('1'); return "ACK SAFE:G1"; }
  if (cmd == "SAFE:G2") { safeGo('2'); return "ACK SAFE:G2"; }

  return "ERR";
}


void setup()
{
  Serial.begin(115200);
  delay(300);
  setupPins();

  Serial.println("Starting Wi-Fi Access Point...");
  int apres = WiFi.beginAP(ssid, pass, apChannel);
  if (apres != WL_AP_LISTENING)
  {
    delay(200);
    Serial.print(".");

  }

  Serial.println("\nAP started.");
  Serial.print("AP SSID: "); Serial.println(ssid);
  Serial.print("AP PASS: "); Serial.println(pass);
  Serial.print("AP CHAN: "); Serial.println(apChannel);
  Serial.print("AP  IP : "); Serial.println(WiFi.localIP());

  server.begin();
  Serial.println("TCP server listening on port 8080");

  inbuf.reserve(64);

}


void loop()
{
  WiFiClient c = server.available();
  if (!c) return;

  Serial.println("Client connected.");
  c.setTimeout(5000);
  unsigned long lastRx = millis();

    while (c.connected())
  {
    if (c.available())
    {
      String line = c.readStringUntil('\n');
      lastRx = millis();
      line.trim();

      if (line.length() > 0)
      {
        Serial.print("CMD: ");
        Serial.println(line);
        String ack = handleCmd(line);
        c.println(ack);
      }
    }

    if (millis() - lastRx > 15000UL)
    {
      Serial.println("Client timeout -> disconnect.");
      break;
    }

    delay(5);
  }

  c.stop();
  Serial.println("Client disconnected.");
  
}