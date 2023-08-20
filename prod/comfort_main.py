import glob
import os
import subprocess
import sounddevice
import soundfile
import threading


# Pi 3/4 have two built-in audio interfaces: 3.5mm and HDMI.  Extra USB audio
# interfaces are expected to show up in indices 2 & 3, though that may not be 
# stable.  Order of sub/main is arbitrary.
SUB_INDEX = 2
MAIN_INDEX = 3

# Data type for audio samples. 
DTYPE = "float32"

def LX(lxp):
    """ Returns the command line to run the provided lxp file w/ LX Headless.
    """
    return ['java', '-cp', 'lx-0.4.1-with-deps.jar:.', 'HeadlessMain'] + [lxp]

def load_scenes():
    """ Load audio and LXP files for each scene in the current directory.

    Any directory beginning with `scene` containing exactly one .lxp file and
    two .wav files will be interpreted as a scene.  The wav files are opened
    immediately and loaded into numpy arrays.
    """
    scenes = []

    for path in glob.glob('scene*'):
        if not os.path.isdir(path): continue

        lxp = glob.glob(os.path.join(path, '*.lxp'))
        main_wav = glob.glob(os.path.join(path, '*.main.wav'))
        sub_wav = glob.glob(os.path.join(path, '*.sub.wav'))

        if len(lxp) != 1 or len(main_wav) != 1 or len(sub_wav) != 1: 
            continue

        scenes.append(Scene(lxp[0], main_wav[0], sub_wav[0]))


    return scenes


def make_output(idx):
    """ Opens an audio interface at index `idx` for output and starts it.
    """
    dev = sounddevice.OutputStream(device=idx, dtype=DTYPE, channels=2)
    return dev

def play_audio(buf, dev, stop):
    dev.start()
    dev.write(buf)

    while not stop.is_set():
        pass

    dev.stop()


def launch_lxp(lxp, stop):
    lx = subprocess.Popen(LX(lxp))

    while not stop.is_set():
        pass

    # TODO: kill it
    lx.send_signal() 

        
class Scene:
    def __init__(self, lxp, main_wav, sub_wav):
        self.lxp = lxp
        self.main, _ = soundfile.read(main_wav, dtype=DTYPE)
        self.sub, _ = soundfile.read(sub_wav, dtype=DTYPE)


    def play(self, main_out, sub_out, stop):
        self.threads = [
            threading.Thread(target=play_audio, args=[self.main, main_out, stop]),
            threading.Thread(target=play_audio, args=[self.sub, sub_out, stop]),
            threading.Thread(target=launch_lxp, args=[self.lxp, stop])
        ]

        for t in self.threads:
            t.join()


if __name__ == "__main__":
    main_out = make_output(MAIN_INDEX)
    sub_out = make_output(SUB_INDEX)

    stop = threading.Signal()

    scenes = load_scenes()

    # TODO: main loop.  Unset stop signal, set timer & listen to button.
    # catch exception and set stop signal to join threads & stop devices.
    # Start next one.