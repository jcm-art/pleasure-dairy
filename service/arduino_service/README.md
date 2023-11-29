Arduino Based Lighting Service
========================


# Introduction and Documentation

## Using the Arduiono Lighting Service




## Developing for Pleasure Dairy Arduino

### Setting up the Arduino IDE

### Developing with VS Code 

#### Setting up VS Code

This [guide](https://www.circuitstate.com/tutorials/how-to-use-vs-code-for-creating-and-uploading-arduino-sketches/) contains instructions on how to set up VS Code for Arduino development. This includes instructions to generate a configuration file for compiling Arduino sketches, which is required for the Arduino extension to work effectively.

#### Using the Arduino Extension to deploy the service

The Arduino extension can also be used to verify and build Arduino sketches. This is done by selecting the `Arduino: Verify` command from the command palette. This will compile the sketch and report any errors.

This compiled sketch can then be deploted to the Arduino. This is done by selecting the `Arduino: Upload` command from the command palette. This will take the compiled sketch and upload it to the Arduino. The Arduino extension will automatically detect the Arduino board and port, and will use the configuration file generated in the previous step to compile the sketch.
 
# LED Control background information

## Introduction

In this section, we will discuss the basics of LED control with Arduino. This will include a discussion of the different types of LEDs, how to control them, and how to use mosfets to control higher power devices.

There are two main types of LED control discussed here; with "Direct Control", the Arduino's output value directly sets the strength of either a single LED or a single color channel of a strip. In this case, setting a pin connected to "R" to a PWM value of 127 (50% of the int8 max of 255) would set the LED or entire LED strip to have an R channel value of 50% output.

The second type of control is for individually addressable LEDs. These LEDs have an integrated circuit either embedded on the LED or adjacent on the strip. This allows each LED in a strip to be controlled separately by sending digital messages from the Arduino to the LED strip. This is discussed in more detail in the "Individually Addressable LED Control" section.

## Direct Onboard LED Control

The simplist way to verify LED functionality with the Arduio service is to control the onboard LED, if available on the Arduino model in usage. The pin number for this is LED_BUILTIN and it can be turned on and off by writing HIGH and LOW values to the digital output.

```
digitalWrite(pin, HIGH);  // turn the LED on (HIGH is the voltage level)
delay(100 * on_time_multiplier); // wait for a second
digitalWrite(pin, LOW);   // turn the LED off by making the voltage LOW
```

## Direct LED Control

External LEDs can be controlled with a similar method; however, to prevent burning out the LED or placing strain on the Arduino output pins (both of which are designed for very low, signal currents), a dropdown resistor should be added in series between the GND -> LED -> Pin. The value of this resistor should be calculated based on the voltage drop across the LED and the current required to drive the LED. The voltage drop across the LED is typically 1.8V, and the current required to drive the LED is typically 20mA. The voltage drop across the resistor is the difference between the voltage supplied by the Arduino and the voltage drop across the LED. The current through the resistor is the same as the current through the LED. The resistor value can then be calculated using Ohm's law. For a single LED and the Arduino Uno, this results in a 220 Ohm resistor.

Note that for standalone LEDs, the longer side of the LED pins should go to the high voltage side of the circuit.


## Direct LED Control with Mosfet

Mosfets can be used as gates to turn on and off devices requiring higher current / power than can be provided by the Arduino. These work by having a gate pin, a source pin, and a drain pin. The source pin should be connected to the ground of the voltage source (either on the Arduino for low power devices equivalent to the setup in the "Direct LED Control" section) while the "drain" pin should be connected to the load and ultimately to high voltage.

The mosfets used in the direct control demonstration example are [here](https://www.amazon.com/gp/product/B07LG5BCDY/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1).

## Individually Addressable LED Control

To control individually addressable LEDs, the FastLED library is used to send commands. This library can be installed in VS Code by opening the command pallette and selecting "Arduino: Library Manager". This will open a new window where the FastLED library can be searched for and installed.

For more details on individually addressable LED control, see this [reference](https://howtomechatronics.com/tutorials/arduino/how-to-control-ws2812b-individually-addressable-leds-using-arduino/).