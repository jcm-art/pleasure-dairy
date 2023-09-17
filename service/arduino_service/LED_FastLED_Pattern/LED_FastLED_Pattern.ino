/*


*/
// Include the Arduino FastLED library
#include <FastLED.h>

// Define Addressable LED parameters
#define ADDRESSABLE_PIN_1 2
#define ADDRESSABLE_PIN_2 4
#define ADDRESSABLE_PIN_3 7
#define ADDRESSABLE_PIN_4 8
#define ADDRESSABLE_PIN_5 12
#define ADDRESSABLE_PIN_6 13
#define NUM_FIXTURES 6
#define NUM_LEDS_PER_FIXTURE 15
CRGB leds[NUM_FIXTURES][NUM_LEDS_PER_FIXTURE];


// Define limits for LED output based on device capabilities
#define MAX_Current 900
#define CURRENT_PER_LED 60
#define MAX_BRIGHTNESS 255 // Max brightness required due to current limiations of prototype board

// Initialize LED pin list
constexpr int addressable_pins[] = {ADDRESSABLE_PIN_1, ADDRESSABLE_PIN_2, ADDRESSABLE_PIN_3, ADDRESSABLE_PIN_4, ADDRESSABLE_PIN_5, ADDRESSABLE_PIN_6};
float output_current = 0.0;
int serial_counter = 0;

void setup() {
  Serial.begin(9600); // open the serial port at 9600 bps:
  // Set pin initial conditions once when you press reset or power the board
  initialize_addressable_LED_pins();
}

void initialize_addressable_LED_pins() {
  // Initialize addressable LED pins (unable to use a for loop)
  FastLED.addLeds<WS2812B, ADDRESSABLE_PIN_1, GRB>(leds[0], NUM_LEDS_PER_FIXTURE).setCorrection(TypicalLEDStrip);
  FastLED.addLeds<WS2812B, ADDRESSABLE_PIN_2, GRB>(leds[1], NUM_LEDS_PER_FIXTURE).setCorrection(TypicalLEDStrip);
  FastLED.addLeds<WS2812B, ADDRESSABLE_PIN_3, GRB>(leds[2], NUM_LEDS_PER_FIXTURE).setCorrection(TypicalLEDStrip);
  FastLED.addLeds<WS2812B, ADDRESSABLE_PIN_4, GRB>(leds[3], NUM_LEDS_PER_FIXTURE).setCorrection(TypicalLEDStrip);
  FastLED.addLeds<WS2812B, ADDRESSABLE_PIN_5, GRB>(leds[4], NUM_LEDS_PER_FIXTURE).setCorrection(TypicalLEDStrip);
  FastLED.addLeds<WS2812B, ADDRESSABLE_PIN_6, GRB>(leds[5], NUM_LEDS_PER_FIXTURE).setCorrection(TypicalLEDStrip);
  FastLED.clear();
}

// Set Addressable LED value w/ current tracking
void set_led(int strip_id, int led_id, int r, int g, int b){
  // Get prior value and update current
  int prior_val = leds[strip_id][led_id].r + leds[strip_id][led_id].g + leds[strip_id][led_id].b;
  output_current += (float((r + g + b) - prior_val))/(3*255) * CURRENT_PER_LED;

  if (serial_counter % 100 == 0){
    Serial.println("Current is " + String(output_current) + " vs. max of " + String(MAX_Current));
    serial_counter = 0;
  }
  serial_counter = serial_counter + 1;

  // Set new LED value
  leds[strip_id][led_id] = CRGB(r, g, b);

  // Check if current is over limit
  if (output_current > MAX_Current){
    float adjusted_current = 0.0;
    float current_ratio = MAX_Current / output_current;
    for (int i = 0; i< NUM_FIXTURES; i = i + 1) {
      for (int j = 0; j < NUM_LEDS_PER_FIXTURE; j = j + 1) {
        CRGB prior_color = leds[i][j];
        int adj_r = int(prior_color.r*current_ratio);
        int adj_g = int(prior_color.g*current_ratio);
        int adj_b = int(prior_color.b*current_ratio);
        leds[i][j] = CRGB(adj_r, adj_g, adj_b);
        adjusted_current+=(adj_r+adj_b+adj_g)/(3*255)*CURRENT_PER_LED;
      }
    }
    output_current = adjusted_current;
  }
}

// Turn off addressable LEDs
void addressable_off(){
  for (byte i = 0; i < NUM_FIXTURES ; i = i + 1) {
    for (byte j = 0; j < NUM_LEDS_PER_FIXTURE; j = j + 1) {
      set_led(i, j, 0, 0, 0);
    }
  }
  FastLED.show();
}

// Vertical traveling LED pattern
void vertical_traveling_led(int num_iterations, int delay_time) {
  // Run traveling LED animation n times
  for (int n = 0; n < num_iterations; n = n + 1) {

    int counter = 0;
    while (counter < NUM_LEDS_PER_FIXTURE) {
      // Set all equal to 0
      for (int i = 0; i< NUM_FIXTURES; i = i + 1){

        for (int j = 0; j < NUM_LEDS_PER_FIXTURE; j = j + 1) {
          set_led(i, j, 0, 0, 0);
        }

        // Set counter value to MAX_BRIGHTNESS
        set_led(i, counter, MAX_BRIGHTNESS, 0, 0);
      }
      FastLED.show();
      counter = counter + 1;
      delay(delay_time);
    }
  }
}

// Spiral traveling LED pattern
void spiral_traveling_led(int num_iterations, int delay_time) {
  // Run traveling LED animation n times
  for (int n = 0; n < num_iterations; n = n + 1) {

    int counter = 0;
    while (counter < NUM_LEDS_PER_FIXTURE) {
      // Set all equal to 0
      for (int i = 0; i< NUM_FIXTURES; i = i + 1){

        for (int j = 0; j < NUM_LEDS_PER_FIXTURE; j = j + 1) {
          set_led(i, j, 0, 0, 0);
        }

        // Set counter value to MAX_BRIGHTNESS
        set_led(i, counter, MAX_BRIGHTNESS, 0, 0);
        FastLED.show();
        counter = counter + 1;
        delay(delay_time);
      }

    }
  }
}

// Pulse
void pulse(int num_iterations, int delay_time, int low_brightness, int high_brightness) {
  // Run traveling LED animation n times
  for (int n = 0; n < num_iterations; n = n + 1) {

    int brightness = low_brightness;
  
    while (brightness < high_brightness) {
      // Set all equal to 0
      for (int i = 0; i< NUM_FIXTURES; i = i + 1){
        for (int j = 0; j < NUM_LEDS_PER_FIXTURE; j = j + 1) {
          set_led(i, j, brightness, 0, 0);
        }

        FastLED.show();
        brightness = brightness + 1;
        delay(delay_time);
      }

    }

    while (brightness >= low_brightness) {
      // Set all equal to 0
      for (int i = 0; i< NUM_FIXTURES; i = i + 1){
        for (int j = 0; j < NUM_LEDS_PER_FIXTURE; j = j + 1) {
          set_led(i, j, brightness, 0, 0);
        }

      }
      FastLED.show();
      brightness = brightness - 1;
      delay(delay_time);

    }
  }
}


// Loop function that runs over and over again forever
void loop() {
  vertical_traveling_led(2, 100);
  addressable_off();
  delay(500);
  spiral_traveling_led(2, 100);
  addressable_off();
  delay(500);
  pulse(2,20, 10, 80);
  addressable_off();
  delay(500);

  // blink_speed_sweep(200, 205);
  // sweep_pwm_values(0, MAX_BRIGHTNESS, 10);

}
