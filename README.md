Pleasure Dairy Lighting
=======================

# Introduction

# Pleasure Dairy Lighting System Overview

## Primary Control Subsystem

TBD - separate or merged into prior?

## Bar and Frontage Subsystem

- TBD x 30mm x 9ft LED meteor tubes (newer, sealed)
    - 30mm x 9ft LED meteor tubes
        - 360 degree light (2 sides light)
        - 64 pcs SMD5050 RGB LEDs/m 
        - 32 pcs UCS2903 ICs/m
    - 12V, 138.24 W per tube? Or 43W per tube?
    - SJ-9ft-UCS2903
- 1 x Raspberry Pi 
- 1 x Pixlite 16 MK2
- 12V Power Supply


## Pleasure Justice Subsystem

- Incenter LED Christmast Lights
    - 12mm x 200cm LED pixel light (~70 strings of 10 LED per string)
        - 12mm LED pixel light
        - UCS1903
        - 10pcs/Chain, 
        - 20cm length between each LED
    - 12V, 3W power consumption per string
- TBD control?
- 12V Power Supply

## Pleasure Comfort Subsystem

- 30mm x 9ft LED meteor tubes (older, unsealed)
    - LED Rope Lights - WS2813 - 30LED/m
- 1 x Raspberrry Pi (confirm model)
- 1 x Pixlite 16 MK2 
- 5V Power Supply

## TBD - Other subsystem components

- 5V power supply (model s 300 -5 power supply)

# Useful References

## Pixlite 16 MK II

- [Pixlite Manual](https://www.advateklights.com/downloads/user-manuals/pixlite-16-mk2)
- [Pixlite Configuration Guide](https://www.advateklights.com/downloads/user-manuals/pixlite-configuration-guide)

## Raspberry Pi 4 Model B Rev 1.2

- [Raspberry Pi 4 Model B Rev 1.2 Specs](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/specifications/)
- [General Raspberry Pi User Guide](https://www.cs.unca.edu/~bruce/Fall14/360/RPiUsersGuide.pdf)
- [General Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)
- [Raspberry Pi Display 1.1 Documentation](https://www.raspberrypi.com/documentation/accessories/display.html)

## LED Programming

- [Overview of WS2813 Lights and Control](https://www.sdiplight.com/what-is-ws2813-led-and-how-to-use-ws2813/)
- [UCS1903 Overview and Electrical Background](https://cdn.sparkfun.com/assets/6/d/6/c/3/UCS1903_IC-manul.pdf)
- [UCS2903 Pixel Protocol Overview](https://www.advateklights.com/knowledge-base/ucs2903)

## Power Supplies

- [5V Power Supply Purchase Link](https://www.sunsky-online.com/p/S-RSP-0111A/S-300-5-DC-0-5V-60A-Regulated-Switching-Power-Supply-100~240V-.htm)
- [General Switching Power Supply Manual from Meanwelll](https://www.power-supplies.com.au/files/mean-well-user-technical-manual.pdf)
- [12V Power Supply Datasheet](https://www.meanwell.com/productPdf.aspx?i=469#1)
- [12V Power Supply Purchase Link](https://www.mouser.com/ProductDetail/MEAN-WELL/SE-600-12?qs=%252B6mEGs9UJHwj0bmY3T4KsQ%3D%3D&gclid=Cj0KCQjwwvilBhCFARIsADvYi7LZ1YHaaP-1CW_h0xP9RxNGU6WAKvi664m51BgY7NbI-mHp1WlqSWQaArVWEALw_wcB)

# Setup

## Raspberry Pi 

### Initial Setup

1. Download the Raspberry Pi Imager to create the SD card with the Raspberry Pi OS.  The Raspberry Pi Imager can be downloaded from [here](https://www.raspberrypi.com/software/).
2. Gather required supplies for installation; you'll need a USB mouse, USB keyboard, display, cables to hook up the display (the Pleasure Dairy Raspberry Pi comes with an attached display) if running the Raspberry Pi with a U.I. If running headless, these are not required.
3. Run the Raspberry Pi Imager and select the right operating system for install
    - For older (model 1/2) raspberry Pis, select a 32 bit operating system
    - Newer versions can use a 64 bit
    - Raspberry Pi OS Lite (64 bit), the headless version of the operating system, was selected for the Pleasure Dairy devices
4. Select the SD card to install the operating system on
5. Click settings and set a hostname for the device (write this down), toggle enable SSH, and set a username and password for the device
6. Set the WIFI SSID, name, password, and country for the device
7. Write the image to the card
8. Install the microSD card onto the raspberry pi and power on the device
9. Follow directions [here](https://www.tomshardware.com/reviews/raspberry-pi-headless-setup-how-to,6028.html) to set up access over wifi or ethernet

### Raspberry Pi VNC Setup

To setup a VNC connection for a headless system, additional instructions are needed beyond those provided in the link above.

1. First, install / upgrade the VNC server on the Raspberry Pi.  This can be done by running the following command on the Raspberry Pi:
    ```
    sudp apt update
    sudo apt install realvnc-vnc-server realvnc-vnc-viewer
    ``` 
2. Follow these [instructions](https://m.clearbluedesign.com/make-headless-raspberry-pi-vnc-open-in-1080p-9f644ecc3cdd) to force a screen resolution for headless VNC.
2. Next, set the VNC resolution via terminal using the following process.
    - Enter "sudo raspi-config" in the terminal
    - Select "Display Resolution"
    - Select "VNC Resolution" and choose a resolution
    - Reboot the device
3. Unfortunately, VNC viewer does not work with a console only boot so you'll need to change the boot settings to boot to the desktop
    - Install lxsession using "sudo apt-get install lxsession" to enable the desktop environment
    - Enter "sudo raspi-config" in the terminal
    - Select "System Settings" and then "Boot / Auto Login" and change Autologin to "Desktop Autologin"
    - Reboot the device
4. Verify that the VNC server is set up correctly by following the local connection over wifi instructions below
5. To enable a remote connection over the internet, a RealVNC account is required; the RealVNC lite account option is free for non-commercial use and limited to 1 user, 3 devices
6. After an account is made, run "vnclicensewiz" on the Raspberry Pi to provide login information via a graphical interface

References: [Setup guide for headless (no monitor)](https://www.tomshardware.com/reviews/raspberry-pi-headless-setup-how-to,6028.html) and [Setup guide for normal operation (with monitor)](https://www.raspberrypi.com/documentation/computers/getting-started.html)

## Pixlite Configuration with Avatek Asistant 

Download the Avatek Assistant SW for the MK1/2 models from [here](https://www.advateklights.com/downloads/advatek-assistant). Avatek does not appear to offer a linux version of the Avatek Assistant 2 so you'll need to use an osx or windows computer. The Avatek Assistant 3 is available for linux but does not appear support the MK1/2 models (it's paired with MK3).


# Developing for Pleasure Dairy

## Connect to Raspberry Pi

### Local connection (ssh)

Use the login information in the .env file (procured directly from @jcm-art) to connect to the Raspberry Pi over SSH.

### Local connection to GUI (VNC)

1. Download and install [VNC Viewer](https://www.realvnc.com/en/connect/download/viewer/macos/) for your non-Raspberry Pi device
2. Run the VNC Viewer and select "run without account"
5. If connecting over Wifi on a local network:
    - Enter the hostname for the Raspberry Pi (this is the hostname you set in the Raspberry Pi Imager)
    - Enter the username and password for the Raspberry Pi 

### Remote connection to GUI (VNC)

1. Download and install [VNC Viewer](https://www.realvnc.com/en/connect/download/viewer/macos/) for your non-Raspberry Pi device
2. Run the VNC Viewer and sign into your RealVNC account
    - You will need to sign in to the Pleasure Dairy RealVNC account on your computer to connect to the device; this account is limited to one user and 3 devices total (login information is in the .env file, obtained directly from @jcm-art)
3. If connecting over the internet:
    - Navigate to the "Pleasure Dairy" team in VNC Viewer and select the name of the raspberry pi device you want to connect to 

### Remote connection to Console (VNC)

TODO - this is not working yet

## Setting up the Raspberry Pi Webcam

To use the webcam attached to the raspberry pi for remote development, install cheese by running the following command in terminal:
```
sudo apt-get install cheese

```

After the installation is complete, open cheese by entering "cheese" in terminal.