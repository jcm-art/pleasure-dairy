
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import os
import json
from scipy.io import wavfile
import scipy.signal



class SoundAnalysisResults:
    
    def __init__(self, sound_file_path) -> None:
        # Store 
        self.sound_file_path = sound_file_path
        temp_name = pathlib.Path(self.sound_file_path).name.split(".")
        self.file_name = temp_name[0]

        # Create dictionary for storing sound analysis results
        self.sound_analysis_dict = {
            'sample_rate': None,
            'audio_length_seconds': None,
            'highest_amplitude': None,
            'lowest_amplitude': None,
            'num_channels': None,
        }

        # Store wave value for audio
        self.audio_value = None

    def set_audio_data(self, audio_value):
        self.audio_value = audio_value

    def set_num_channels(self, num_channels):
        self.sound_analysis_dict['num_channels'] = num_channels

    def set_sampling_rate(self, fs):
        self.sound_analysis_dict['sample_rate'] = fs

    def set_audio_length_seconds(self, audio_length_seconds):
        self.sound_analysis_dict['audio_length_seconds'] = audio_length_seconds
    
    def set_highest_amplitude(self, highest_amplitude):
        self.sound_analysis_dict['highest_amplitude'] = highest_amplitude

    def set_lowest_amplitude(self, lowest_amplitude):
        self.sound_analysis_dict['lowest_amplitude'] = lowest_amplitude



class PleasureComfortSoundAnalyzer:

    def __init__(self, sound_file_directory_path) -> None:
        self.sound_file_directory = pathlib.Path(sound_file_directory_path)
        self.sound_file_paths = []
        self.sound_file_dict = {}
        self.sound_file_analysis_results = []
        self.allowed_audio_files = ['.wav'] # '.mp3', '.ogg', '.flac', '.m4a', '.wma', '.aiff', '.au', '.raw']


    def get_sound_file_paths(self) -> list:
        print("Getting sound file paths...")
        for root, dirs, files in os.walk(self.sound_file_directory):
            for file in files:
                candidate_path = pathlib.PurePath(root, file)
                candidate_extension = candidate_path.suffix
                if candidate_extension in self.allowed_audio_files:
                    self.sound_file_paths.append(candidate_path)
        print(f"Retrived sound paths: {self.sound_file_paths}")

    def analyze_sound_files(self) -> list:
        print("Analyzing sound files...")
        for path in self.sound_file_paths:
            # Creat new audio analysis class
            audio_analysis = SoundAnalysisResults(path.name)

            # Read in audio file
            fs, wave = scipy.io.wavfile.read(path)
            audio_analysis.set_audio_data(wave)

            # Get audio analysis parameters
            self._analyze_sounds(audio_analysis, fs, wave)

            # Add audio analysis results to list
            self.sound_file_analysis_results.append(audio_analysis)


    def _analyze_sounds(self, audio_analysis, fs, wave) -> SoundAnalysisResults:
        
        # Set audio analysis parameters
        audio_analysis.set_sampling_rate(fs)
        audio_analysis.set_audio_length_seconds(len(wave)/fs)
        if wave.shape[1] is None:
            num_channels = 1
        else:
            num_channels = wave.shape[1]
        audio_analysis.set_num_channels(num_channels)
        audio_analysis.set_highest_amplitude(float(np.max(wave)))
        audio_analysis.set_lowest_amplitude(float(np.min(wave)))
        
        return audio_analysis
    
    def create_sound_plots(self):
        # Make output directory
        plot_output_directory = self.sound_file_directory/"plots/"
        plot_output_directory.mkdir(parents=True, exist_ok=True)

        # Create and save plots
        for sound_object in self.sound_file_analysis_results:
            # Get sound data
            sound_data = sound_object.audio_value

            # Get number of frames and sample rate
            num_frames = sound_data.shape[0]
            frames = np.arange(num_frames)   # x-axis
            fs = sound_object.sound_analysis_dict['sample_rate']
            num_channels = sound_object.sound_analysis_dict['num_channels']

            # Create plot
            fig, (axs_wav, axs_fourier) = plt.subplots(1,2, figsize=(12, 4))

            for i in range(0, num_channels):
                axs_wav.plot(frames, sound_data[:,i])
                axs_wav.set_xticks(np.arange(0, num_frames, num_frames/500000*fs), np.arange(0, num_frames/fs, num_frames/500000).astype("float16"))

                # TODO move to fourier transform
                fftresult = abs(scipy.fft(sound_data[:,i])/num_frames)
                freqs = np.arange(num_frames)*fs/num_frames
                half_size = int(num_frames/2)
                axs_fourier.plot(freqs[:half_size], fftresult[:half_size])



            # Label graphs
            axs_wav.set_title(f"Sound Waveform for {sound_object.file_name}")
            axs_wav.set_xlabel("Time (seconds)")          
            axs_wav.set_ylabel("Amplitude of sound wave")   

            axs_fourier.set_title(f"Sound Waveform for {sound_object.file_name}")
            axs_fourier.set_xlabel("Time (seconds)")          
            axs_fourier.set_ylabel("Amplitude of sound wave")   

            # Save plot       
            fig.savefig(plot_output_directory/f"wave_plot_{sound_object.file_name}.png")         
            plt.close(fig)             


    def _save_sound_analysis_result(self) -> None:
        output_json = self._build_full_dict()

        # Save analysis results to json file
        with open(self.sound_file_directory/"audio_analysis.json", "w") as outfile:
            outfile.write(output_json)

    def print_audio_analysis_results(self) -> None:
        output_json = self._build_full_dict()

        # Json formateed print
        print(output_json)

    def _build_full_dict(self):
        output_dict = {}
        
        # Get analysis dictionaries and assembly
        for result in self.sound_file_analysis_results:
            output_dict[result.sound_file_path] = result.sound_analysis_dict

        return json.dumps(output_dict, indent=4, sort_keys=True)


if __name__ == '__main__':
    pcsa = PleasureComfortSoundAnalyzer(sound_file_directory_path='./tmp/sounds')
    pcsa.get_sound_file_paths()
    pcsa.analyze_sound_files()
    pcsa.create_sound_plots()
    pcsa.print_audio_analysis_results()