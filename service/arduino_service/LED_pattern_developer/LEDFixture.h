#ifndef VisCreator_h
#define VisCreator_h

#include "Arduino.h" 
#include "PatternStructFrame.h"

// TODO (jcm-art) - Implement LED pattern Library if Arduino selected for project, else deprecate

// TODO - update to accept preallocated memory space to fill, free memory in scene file on exit
// https://stackoverflow.com/questions/23143624/c-return-array-of-structs

// TODO - determine how to store time information vs. spatial information + correct encapsulation

class LEDFixture {
public:
	LEDFixture(int num_leds, int led_pin);
    // Methods to retreive stored values
    int get_num_leds();
    int get_led_pin();
    int *get_leds();

private:
    int *leds;
    int num_leds;
    int led_pin;
};

#endif