/*


*/
// Include the Arduino FastLED library
#include <FastLED.h>

// Add missing definitions from library
#define PIN9 9

// Define Addressable LED parameters
#define LED_PIN 7
#define NUM_LEDS 5
CRGB leds[NUM_LEDS];

// Initialize LED pin list
int output_pins[] = {LED_BUILTIN, PIN3, PIN5, PIN6, PIN9};
int num_pins = sizeof(output_pins) / sizeof(output_pins[0]);

// the setup function runs once when you press reset or power the board
void setup() {

  // Set pin initial conditions
  initialize_output_pins();
  initialize_addressable_LED_pins();

}

// Initialize output pins to off
void initialize_output_pins() {
  for (byte i = 0; i < num_pins; i = i + 1) {
    // initialize output pins as an output.
    pinMode(output_pins[i], OUTPUT);

    // write pin to low to ensure it is off
    analogWrite(output_pins[i], 0);
  }
}

void initialize_addressable_LED_pins() {
  // Initialize addressable LED pins
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
}

// Enable a custom delay factor for blink
void timed_blink(int pin, int on_time_multiplier, int delay_multiplier) {
  
  analogWrite(pin, 255);  // turn the LED on (HIGH is the voltage level)
  delay(1 * on_time_multiplier);                      // wait for a second
  analogWrite(pin, 0);   // turn the LED off by making the voltage LOW
  delay(1 * delay_multiplier);                      // wait for a second
}

// Blink all pins in sequence
void blink_all_pins_sequential(int speed) {
  // Iterate over initialized pin list and blink each one
  for (byte i = 0; i < num_pins; i = i + 1) {
    timed_blink(output_pins[i], speed, speed);
  }

}

// Sweep blink pattern with different speeds
void blink_speed_sweep(int start, int end) {
  for (byte i = start; i < end; i = i + 1) {
    blink_all_pins_sequential(i);
  }
  delay(1000);
}

// Sweep PWM values for LEDs
void sweep_pwm_values(int start, int end, int delay_time) {
  // Forward sweep through all int8 pwm values
  for (byte i = start; i < end; i = i + 1) {
    // Turn pins on with PWM value
    for (byte j = 0; j < num_pins; j = j + 1) {
      analogWrite(output_pins[j], i);
    }
    delay(delay_time);
  }

  // Backwards sweep through all int8 pwm values
  for (byte i = start; i < end; i = i + 1) {
    // Turn pins on with PWM value
    for (byte j = 0; j < num_pins; j = j + 1) {
      analogWrite(output_pins[j], 255-1-i);
    }
    delay(delay_time);
  }
  delay(1000);
}

// Short demo script for LED
void addressable_demo_pattern(){
  leds[0] = CRGB(255, 0, 0);
  FastLED.show();
  delay(500);  
  leds[1] = CRGB(0, 255, 0);
  FastLED.show();
  delay(500);
  leds[2] = CRGB(0, 0, 255);
  FastLED.show();
  delay(500);
  leds[3] = CRGB(150, 0, 255);
  FastLED.show();
  delay(500);
  leds[4] = CRGB(255, 200, 20);
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
      leds[counter] = CRGB(255, 0, 0);
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
  // sweep_pwm_values(0, 255, 10);

}
