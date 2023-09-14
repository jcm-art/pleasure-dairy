#include "LEDFixtureArtist.h"
#include "PatternStructFrame.h"

LEDFixtureArtist::LEDFixtureArtist() {
}



// Static, uniform fixture color functions
void LEDFixtureArtist::generate_static_color(int num_leds, int r, int g, int b){

}
void LEDFixtureArtist::generate_static_color(int num_leds, int *color){
    
}
void LEDFixtureArtist::generate_random_color(int num_leds){
    
}

// Dynamic, uniform fixture color functions
void LEDFixtureArtist::generate_color_cycle(int num_leds, int speed){
    
}
void LEDFixtureArtist::generate_color_cycle(int num_leds, int speed, int num_cycles){
    
}
void LEDFixtureArtist::generate_color_fade(int num_leds, int r0, int g0, int b0, int r1, int g1, int b1, int speed){
    
}
void LEDFixtureArtist::generate_color_fade(int num_leds, int *color0, int *color1, int speed){
    
}

// Static, non-uniform fixture color functions
void LEDFixtureArtist::generate_color_gradient(int num_leds, int r0, int g0, int b0, int r1, int g1, int b1){
    
}
void LEDFixtureArtist::generate_color_gradient(int num_leds, int *color0, int *color1){
    
}

// Dynamic, non-uniform fixture color functions
void LEDFixtureArtist::generate_color_gradient_cycle(int num_leds, int r0, int g0, int b0, int r1, int g1, int b1, int speed){
    
}
void LEDFixtureArtist::generate_color_gradient_cycle(int num_leds, int *color0, int *color1, int speed){
    
}

// Layering effects to combine patterns
void LEDFixtureArtist::add_layers(PatternStructFrame *pattern1, PatternStructFrame *pattern2){
    
}
void LEDFixtureArtist::subtract_layer(PatternStructFrame *pattern1, PatternStructFrame *pattern2){
    
}
void LEDFixtureArtist::multiply_layer(PatternStructFrame *pattern1, PatternStructFrame *pattern2){
    
}
