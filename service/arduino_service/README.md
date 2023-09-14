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

## Onboard LED Control

The simplist way to verify LED functionality with the Arduio service is to control the onboard LED, if available on the Arduino model in usage. The pin number for this is LED_BUILTIN and it can be turned on and off by writing HIGH and LOW values to the digital output.

```
digitalWrite(pin, HIGH);  // turn the LED on (HIGH is the voltage level)
delay(100 * on_time_multiplier); // wait for a second
digitalWrite(pin, LOW);   // turn the LED off by making the voltage LOW
```

## Direct LED Control

External LEDs can be controlled with a similar method; however, to prevent burning out the LED or placing strain on the Arduino output pins (both of which are designed for very low, signal currents), a dropdown resistor should be added in series between the GND -> LED -> Pin. The value of this resistor should be calculated based on the voltage drop across the LED and the current required to drive the LED. The voltage drop across the LED is typically 1.8V, and the current required to drive the LED is typically 20mA. The voltage drop across the resistor is the difference between the voltage supplied by the Arduino and the voltage drop across the LED. The current through the resistor is the same as the current through the LED. The resistor value can then be calculated using Ohm's law. For a single LED and the Arduino Uno, this results in a 220 Ohm resistor.

Note that for standalone LEDs, the longer side of the LED pins should go to the high voltage side of the circuit.


## LED Control with Mosfet

Mosfets can be used as gates to turn on and off devices requiring higher current / power than can be provided by the Arduino. These work by having a gate pin, a source pin, and a drain pin. The source pin should be connected to the ground of the voltage source (either on the Arduino for low power devices equivalent to the setup in the "Direct LED Control" section) while the "drain" pin should be connected to the load and ultimately to high voltage.