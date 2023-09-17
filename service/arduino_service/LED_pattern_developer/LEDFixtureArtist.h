#ifndef VisCreator_h
#define VisCreator_h

#include "Arduino.h" 
#include "PatternStructFrame.h"

// TODO - update to accept preallocated memory space to fill, free memory in scene file on exit
// https://stackoverflow.com/questions/23143624/c-return-array-of-structs

class LEDFixtureArtist {
public:
	LEDFixtureArtist();

	// Static, uniform fixture color functions
	void generate_static_color(int num_leds, int r, int g, int b);
	void generate_static_color(int num_leds, int *color);
	void generate_random_color(int num_leds);

	// Dynamic, uniform fixture color functions
	void generate_color_cycle(int num_leds, int speed);
	void generate_color_cycle(int num_leds, int speed, int num_cycles);
	void generate_color_fade(int num_leds, int r0, int g0, int b0, int r1, int g1, int b1, int speed);
	void generate_color_fade(int num_leds, int *color0, int *color1, int speed);

	// Static, non-uniform fixture color functions
	void generate_color_gradient(int num_leds, int r0, int g0, int b0, int r1, int g1, int b1);
	void generate_color_gradient(int num_leds, int *color0, int *color1);

	// Dynamic, non-uniform fixture color functions
	void generate_color_gradient_cycle(int num_leds, int r0, int g0, int b0, int r1, int g1, int b1, int speed);
	void generate_color_gradient_cycle(int num_leds, int *color0, int *color1, int speed);

	// Layering effects to combine patterns
	void add_layers(PatternStructFrame *pattern1, PatternStructFrame *pattern2);
	void subtract_layer(PatternStructFrame *pattern1, PatternStructFrame *pattern2);
	void multiply_layer(PatternStructFrame *pattern1, PatternStructFrame *pattern2);

private:
};

#endif