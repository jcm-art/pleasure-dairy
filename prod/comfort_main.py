#!/bin/python3
import glob
import os
import subprocess
import sounddevice
import soundfile
import threading
import signal
import time

import rpi.GPIO as GPIO

# Pi 3/4 have two built-in audio interfaces: 3.5mm and HDMI.  Extra USB audio
# interfaces are expected to show up in indices 2 & 3, though that may not be
# stable.  Order of sub/main is arbitrary.
SUB_INDEX = 1
MAIN_INDEX = 2

# Can be any, just needs to match what's plugged in.
BUTTON_PIN = 17

# Data type for audio samples.
DTYPE = "float32"

# How many seconds to wait before advancing to the next scene.
TIMEOUT = 3

def play_audio(buf, dev, name, signal):
    print('Playing audio on %s' % name)
    dev.start()
    dev.write(buf)

    signal.wait()
    print('[%s]: Received stop signal!' % name)

    dev.stop()
    print('[%s]: Closed device, exiting.' % name)

def launch_lxp(lxp, signal):
    print('Launching %s with LX headless' % lxp)
    lx = subprocess.Popen([
        'java', '-cp', 'lx-0.4.1-with-deps.jar:.', 'HeadlessMain', lxp])

    signal.wait()
    print('[%s]: Received stop signal!' % lxp)

    # Send the signal to all the process groups
    os.killpg(os.getpgid(lx.pid), signal.SIGTERM)
    print('[%s]: Killed LX process, exiting.' % lxp)


class PleasureComfort:
    def __init__(self):
        self.main = sounddevice.OutputStream(
            device=MAIN_INDEX, dtype=DTYPE, channels=2)
        self.sub = sounddevice.OutputStream(
            device=SUB_INDEX, dtype=DTYPE, channels=2)
        
        self.stop_signal = threading.Event()

        self.idx = 0
        self._load_scenes()
        self._init_gpio()

        self.alarm = threading.Timer(TIMEOUT, self.next)

    def _init_gpio(self):
        """ Initialize button-listening gpio pin.
        
        The button is an SPST switch which connects to 5V, so the pin is 
        configured as a pull-down.  When the button is pressed, the rising edge
        of the voltage change will trigger the callback.
        """
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(
            BUTTON_PIN, GPIO.RISING, callback=self.next, bouncetime=200)

    def _load_scenes(self):
        """ Load audio and LXP files for each scene in the scenes directory.

        A scene is any subdirectory of `scenes` containing exactly
        - one .lxp file and
        - two .wav files with naming pattern *.main.wav and *.sub.wav
        The wav files are opened immediately and loaded into numpy arrays.
        """
        self.scenes = []
        for path in os.listdir('scenes'):
            if not os.path.isdir(path): continue
            
            lxp = glob.glob(os.path.join(path, '*.lxp'))
            main_wav = glob.glob(os.path.join(path, '*main.wav'))
            sub_wav = glob.glob(os.path.join(path, '*sub.wav'))

            if len(lxp) != 1 or len(main_wav) != 1 or len(sub_wav) != 1:
                continue

            print(lxp, main_wav, sub_wav)
            self.scenes.append({
                'lxp': lxp[0], 
                'main': soundfile.read(main_wav[0], dtype=DTYPE),
                'sub': soundfile.read(sub_wav[0], dtype=DTYPE),
            })

    def run(self):
        while True:
            print('Starting scene %d' % self.idx)
            self.play_scene()

    def play_scene(self):
        self.alarm.start()

        scene = self.scenes[self.idx]
        self.threads = [
            threading.Thread(
                target=play_audio, 
                args=[scene['main'], self.main_out, 'main', self.stop_signal]),
            threading.Thread(
                target=play_audio, 
                args=[scene['sub'], self.sub_out, 'sub', self.stop_signal]),
            threading.Thread(
                target=launch_lxp, 
                args=[scene['lxp'], self.stop_signal])
        ]

        self.stop_signal.wait()

    def next(self):
        # Ensure that any pending alarm is cancelled, and re-initialize so it
        # can be started again by the next scene.
        self.alarm.cancel()
        self.alarm = threading.Timer(TIMEOUT, self.next)

        # Tell all threads it's time to stop, then wait for them to clean up and
        # exit gracefully, before clearing the stop signal.
        self.stop_signal.set()
        for t in self.threads:
            t.join()
        self.stop_signal.clear()

        self.idx = (self.idx + 1) % len(self.scenes)


if __name__ == "__main__":
    pd = PleasureComfort()
    try:
        pd.run()
    finally:
        print("GPIO CLEANUP")
        GPIO.cleanup()
