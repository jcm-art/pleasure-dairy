#!/bin/python3
import glob
import os
import subprocess
import sounddevice
import soundfile
import threading
import time

import RPi.GPIO as GPIO

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
TIMEOUT = 10

def launch_lxp(lxp, signal):
    print('Launching %s with LX headless' % lxp)
    lx = subprocess.Popen([
        'java', '-cp', 'lx-0.4.1-with-deps.jar:.', 'HeadlessMain', lxp])

    signal.wait()
    
    print('[%s]: Received stop signal!' % lxp)
    lx.terminate()
    
    print('[%s]: Killed LX process, exiting.' % lxp)


class PleasureComfort:
    def __init__(self):
        
        self.stop_signal = threading.Event()
        self.next_signal = threading.Event()

        self._init_gpio()
        self._load_scenes()
        self.idx = 0

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
        print('Loading scenes from %s' % os.getcwd())
        print(os.listdir('scenes'))
        self.scenes = []
        for path in os.listdir('scenes'):
            prefix = os.path.join(os.getcwd(), 'scenes', path)
            if not os.path.isdir(prefix): continue
            
            lxp = glob.glob(os.path.join(prefix, '*.lxp'))
            main_wav = glob.glob(os.path.join(prefix, '*main.wav'))
            sub_wav = glob.glob(os.path.join(prefix, '*sub.wav'))

            if len(lxp) != 1 or len(main_wav) != 1 or len(sub_wav) != 1:
                continue

            self.scenes.append({
                'lxp': os.path.join(prefix, lxp[0]), 
                'main': os.path.join(prefix, main_wav[0]),
                'sub': os.path.join(prefix, sub_wav[0]),
            })
        print('Loaded %d scenes.' % len(self.scenes))

    def run(self):
        while True:
            try:
                print('Starting scene %d' % self.idx)
                self.play_scene()
            except Exception as e:
                self.alarm.cancel()
                raise e

    def play_scene(self):
        self.alarm.start()
        self.next_signal.clear()

        scene = self.scenes[self.idx]

        print('[play_scene] Launching scene with {lxp}, {main}, {sub}'
              .format(**scene))

        self.threads = [
            threading.Thread(
                target=self.play_audio, 
                args=[scene['main'], MAIN_INDEX]),
            threading.Thread(
                target=self.play_audio, 
                args=[scene['sub'], SUB_INDEX]),
            threading.Thread(
                target=launch_lxp, 
                args=[scene['lxp'], self.stop_signal])
        ]

        for t in self.threads:
            t.start()

        print('[play_scene] Waiting for stop/next signal.')
        self.next_signal.wait()

    def play_audio(self, wav, device_index):
        with soundfile.SoundFile(wav) as f:
            def callback(outdata, n_frames, time, status):
                view = f.read(n_frames, dtype=DTYPE, out=outdata)
                if view.size != outdata.size:
                    print('[%s] End of file.' % wav)
                    raise sounddevice.CallbackStop()
                if self.stop_signal.is_set():
                    print('[%s] Received stop signal!' % wav)
                    raise sounddevice.CallbackStop()
                
            with sounddevice.OutputStream(
                samplerate=f.samplerate, channels=f.channels, dtype=DTYPE,
                device=device_index, callback=callback) as stream:
                while stream.active:
                    time.sleep(0.1)

    def next(self):
        # Ensure that any pending alarm is cancelled, and re-initialize so it
        # can be started again by the nekxt scene.
        self.alarm.cancel()
        self.alarm = threading.Timer(TIMEOUT, self.next)

        # Tell all threads it's time to stop, then wait for them to clean up and
        # exit gracefully, before clearing the stop signal.
        print('[next] Ending scene; sending stop signal.')
        self.stop_signal.set()

        print('[next] Waiting for threads to terminate')
        for t in self.threads:
            t.join()

        print('[next] Clearing stop signal')
        self.stop_signal.clear()

        self.idx = (self.idx + 1) % len(self.scenes)
        self.next_signal.set()


if __name__ == "__main__":
    pd = PleasureComfort()
    try:
        pd.run()
    finally:
        print("GPIO CLEANUP")
        GPIO.cleanup()
