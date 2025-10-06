#include <WiFiS3.h>

const char* ssid = "ArduinoAP";
const char* pass = "123456789";
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

  allOff();
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
 * @brief Parse and execute LED control commands received from the Raspberry Pi.
 *
 * This function interprets a string command and updates the LEDs of one or both
 * traffic light signals accordingly. Commands can control individual lights or
 * both signals simultaneously.
 *
 * **Supported commands:**
 * - `"LED_R1"`, `"LED_Y1"`, `"LED_G1"` → Set Signal 1 (Red, Yellow, Green)
 * - `"LED_R2"`, `"LED_Y2"`, `"LED_G2"` → Set Signal 2 (Red, Yellow, Green)
 * - `"S:XY"` → Combined command for both signals,  
 *   where `X` controls Signal 1 and `Y` controls Signal 2  
 *   (`R`, `Y`, or `G`, e.g. `"S:GR"` = Signal 1 Green, Signal 2 Red)
 * - `"ALL:OFF"` → Turn off all LEDs.
 *
 * @param cmd The command string to be processed (case-insensitive).
 *
 * @note Unknown or malformed commands are ignored silently.
 * @pre Pins must be initialized via setupPins().
 * @post The LEDs will reflect the last valid command executed.
 */
void handleCmd(String cmd)
{
  cmd.trim();
  cmd.toUpperCase();

  if (cmd == "R1") { setLight(LED_R1, LED_Y1, LED_G1, 'R'); }
  else if (cmd == "Y1") { setLight(LED_R1, LED_Y1, LED_G1, 'Y'); }
  else if (cmd == "G1") { setLight(LED_R1, LED_Y1, LED_G1, 'G'); }
  else if (cmd == "R2") { setLight(LED_R2, LED_Y2, LED_G2, 'R'); }
  else if (cmd == "Y2") { setLight(LED_R2, LED_Y2, LED_G2, 'Y'); }
  else if (cmd == "G2") { setLight(LED_R2, LED_Y2, LED_G2, 'G'); }
  else if (cmd.startsWith("S:") && cmd.length() == 4)
  {
    char a = cmd.charAt(2);
    char b = cmd.charAt(3);
    setLight(LED_R1, LED_Y1, LED_G1, a);
    setLight(LED_R2, LED_Y2, LED_G2, b);
  }
  else if (cmd == "ALL:OFF") { allOff(); }
}


void setup()
{
  Serial.begin(115200);
  setupPins();

  if (WiFi.beginAP(ssid, pass) != WL_AP_LISTENING)
  {
    Serial.println("AP failed, rebooting...");
    NVIC_SystemReset();

  
  }

  delay(500);
  Serial.print("AP IP: ");
  Serial.println(WiFi.localIP());
  server.begin();

}


void loop()
{
  WiFiClient c = server.available();
  
  if (!c) return;
  c.setTimeout(2000);
  String cmd = c.readStringUntil('\n');

  if (cmd.length())
  {
    Serial.print("CMD: ");
    Serial.println(cmd);
    handleCmd(cmd);
    c.println("OK");
  
  }
  c.stop();
}

























