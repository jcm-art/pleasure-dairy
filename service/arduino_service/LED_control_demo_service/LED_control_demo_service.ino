/*


*/
// Include the Arduino FastLED library
#include <FastLED.h>

// Add missing definitions from library
#define PIN9 9

// Define Addressable LED parameters
#define LED_PIN 2
#define NUM_LEDS 15
#define MAX_BRIGHTNESS 50 // Max brightness required due to current limiations of prototype board
// TODO - replace max brightness with current check function
CRGB leds[NUM_LEDS];

// the setup function runs once when you press reset or power the board
void setup() {

  // Set pin initial conditions
  initialize_addressable_LED_pins();

}

// Initialize output pins to off
void initialize_addressable_LED_pins() {
  // Initialize addressable LED pins
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
}

// Short demo script for Fast LED
void addressable_demo_pattern(){
  leds[0] = CRGB(MAX_BRIGHTNESS, 0, 0);
  FastLED.show();
  delay(500);  
  leds[1] = CRGB(0, MAX_BRIGHTNESS, 0);
  FastLED.show();
  delay(500);
  leds[2] = CRGB(0, 0, MAX_BRIGHTNESS);
  FastLED.show();
  delay(500);
  leds[3] = CRGB(150, 0, MAX_BRIGHTNESS);
  FastLED.show();
  delay(500);
  leds[4] = CRGB(MAX_BRIGHTNESS, 200, 20);
  FastLED.show();
  delay(500);
}

// Turn off addressable LEDs
void addressable_off(){
  for (byte i = 0; i < NUM_LEDS; i = i + 1) {
    leds[i] = CRGB(0, 0, 0);
  }
  FastLED.show();
}

// Traveling LED pattern
void traveling_led(int num_iterations, int delay_time) {
  for (int j = 0; j < num_iterations; j = j + 1) {
    int counter = 0;
    while (counter < NUM_LEDS) {
      // Set all equal to 0
      for (int i = 0; i < NUM_LEDS; i = i + 1) {
        leds[i] = CRGB(0, 0, 0);
      }

      // Set counter value to 255
      leds[counter] = CRGB(MAX_BRIGHTNESS, 0, 0);
      FastLED.show();
      counter = counter + 1;
      delay(delay_time);
    }
  }
}


// Loop function that runs over and over again forever
void loop() {
  addressable_demo_pattern();
  addressable_off();
  traveling_led(5, 100);
  // blink_speed_sweep(200, 205);
  // sweep_pwm_values(0, MAX_BRIGHTNESS, 10);

}
