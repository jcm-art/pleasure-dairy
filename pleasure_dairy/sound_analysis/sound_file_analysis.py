
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import os
import json
from scipy.io import wavfile
import scipy.signal
from scipy.fft import fft



class SoundAnalysisResults:
    
    def __init__(self, sound_file_path, num_top_frequencies=3, freq_peak_threshold_fraction=0.01) -> None:
        # Store file path and name
        self.sound_file_path = sound_file_path
        temp_name = pathlib.Path(self.sound_file_path).name.split(".")
        self.file_name = temp_name[0]

        # Define top_n frequency value
        self.top_freq_n = num_top_frequencies
        self.freq_peak_threshold_fraction = freq_peak_threshold_fraction
        self.mask_size = None

        # Create dictionary for storing sound analysis results
        self.sound_analysis_dict = {
            'sample_rate': None,
            'audio_length_seconds': None,
            'highest_amplitude': None,
            'lowest_amplitude': None,
            'num_channels': None,
            'num_frames': None,
            'top_frequencies': {},
            'top_frequencies_amplitudes': {},
        }

        # Store wave value for audio
        self.audio_value = None

        # Add space for FFT results
        self.fft_results = []
        self.fft_frequencies = []

    def set_audio_data(self, audio_value):
        self.audio_value = audio_value

    def set_num_channels(self, num_channels):
        self.sound_analysis_dict['num_channels'] = num_channels

        for i in range(1,num_channels+1):
            self.sound_analysis_dict['top_frequencies'][i]=[]
            self.sound_analysis_dict['top_frequencies_amplitudes'][i]=[]

    def set_num_frames(self, num_frames):
        self.sound_analysis_dict['num_frames'] = num_frames
        self.mask_size = int(self.freq_peak_threshold_fraction * num_frames)


    def set_sampling_rate(self, fs):
        self.sound_analysis_dict['sample_rate'] = fs

    def set_audio_length_seconds(self, audio_length_seconds):
        self.sound_analysis_dict['audio_length_seconds'] = audio_length_seconds
    
    def set_highest_amplitude(self, highest_amplitude):
        self.sound_analysis_dict['highest_amplitude'] = highest_amplitude

    def set_lowest_amplitude(self, lowest_amplitude):
        self.sound_analysis_dict['lowest_amplitude'] = lowest_amplitude

    def append_fft_result(self, fft_result, fft_frequency):
        self.fft_results.append(fft_result)
        self.fft_frequencies.append(fft_frequency)

        channel_num = len(self.fft_results)

        # TODO - move to analyzer, use this for storage only
        for i in range(0, self.top_freq_n):
            # Get top n frequency
            max_fft_index = np.argmax(fft_result)
            print(f"{i} Max FFT index: {max_fft_index} vs. num_frames = {len(fft_result)}")
            self.sound_analysis_dict['top_frequencies'][channel_num].append(fft_frequency[max_fft_index])
            self.sound_analysis_dict['top_frequencies_amplitudes'][channel_num].append(fft_result[max_fft_index])

            # Remove top n frequency from list
            mask = np.ones(len(fft_result), dtype=bool)
            mask_start = max_fft_index - self.mask_size if max_fft_index - self.mask_size >0 else 0
            mask_end = max_fft_index + self.mask_size if max_fft_index + self.mask_size < len(fft_result) else len(fft_result)
            mask[mask_start:mask_end] = False
            fft_result = fft_result[mask]
            fft_frequency = fft_frequency[mask]


    def get_fft_result(self, index):
        return self.fft_results[index], self.fft_frequencies[index]

    def get_top_n_frequencies(self, channel_num):
        return self.sound_analysis_dict['top_frequencies'][channel_num], self.sound_analysis_dict['top_frequencies_amplitudes'][channel_num]


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
        print("Retreived sound paths")

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
            self._generate_and_store_fft(audio_analysis, fs, wave)

            # Add audio analysis results to list
            self.sound_file_analysis_results.append(audio_analysis)

        print("Sound files analyzed....")


    def _analyze_sounds(self, audio_analysis, fs, wave) -> SoundAnalysisResults:
        audio_analysis.set_sampling_rate(fs)
        audio_analysis.set_audio_length_seconds(len(wave)/fs)
        if wave.shape[1] is None:
            num_channels = 1
        else:
            num_channels = wave.shape[1]
        audio_analysis.set_num_channels(num_channels)
        audio_analysis.set_num_frames(wave.shape[0])
        audio_analysis.set_highest_amplitude(float(np.max(wave)))
        audio_analysis.set_lowest_amplitude(float(np.min(wave)))
        
        return audio_analysis
    
    def _generate_and_store_fft(self, audio_analysis, fs, wave):
        # Get sound data
        sound_data = audio_analysis.audio_value
        fs = audio_analysis.sound_analysis_dict['sample_rate']
        num_frames = sound_data.shape[0]
        num_channels = audio_analysis.sound_analysis_dict['num_channels']
        

        # Calculate and store FFTs
        for i in range(0, num_channels):
            fftresult = abs(fft(sound_data[:,i])/num_frames)
            freqs = np.arange(num_frames)*fs/num_frames

            # Save results
            half_size = int(np.floor(num_frames/2))
            audio_analysis.append_fft_result(fftresult[:half_size], freqs[:half_size])
    
    def create_sound_plots(self):
        print("Creating sound and frequnecy plots...")

        # Make output directory
        plot_output_directory = self.sound_file_directory/"plots/"
        plot_output_directory.mkdir(parents=True, exist_ok=True)

        # Set colors
        plot_colors = ['b', 'r']
        top_n_colors = ['k','g']

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
                axs_wav.plot(frames, sound_data[:,i], label=f"Channel {i+1}", color=plot_colors[i])
                axs_wav.set_xticks(np.arange(0, num_frames, num_frames/500000*fs), np.arange(0, num_frames/fs, num_frames/500000).astype("float16"))

                fftresult, freqs = sound_object.get_fft_result(i)
                axs_fourier.plot(freqs, fftresult, label=f"Channel {i+1}",color=plot_colors[i])

                # Label top points
                # TODO - combine channel frequencies
                if i==0:
                    top_n_freq, top_n_amplitudes = sound_object.get_top_n_frequencies(i+1)
                    axs_fourier.scatter(top_n_freq,top_n_amplitudes,marker="x", label=f"Top {sound_object.top_freq_n} frequency (channel {i+1})",color=top_n_colors[i])
                    for i in range(len(top_n_freq)):
                        axs_fourier.annotate(f"f={round(top_n_freq[i],1)}", (top_n_freq[i], top_n_amplitudes[i]))


            # Label graphs
            axs_wav.set_title(f"Sound Waveform for {sound_object.file_name}")
            axs_wav.set_xlabel("Time (seconds)")          
            axs_wav.set_ylabel("Amplitude of sound wave")   
            axs_wav.legend(loc="lower right")

            axs_fourier.set_title(f"FFT for {sound_object.file_name}")
            axs_fourier.set_xlabel("Frequency")          
            axs_fourier.set_ylabel("Intensity of Frequency Response") 
            axs_fourier.legend(loc="best")  
            

            # Save plot       
            fig.savefig(plot_output_directory/f"wave_plot_{sound_object.file_name}.png")         
            plt.close(fig)             

        print("Plots completed...")

    def _save_sound_analysis_result(self) -> None:
        print("Saving output...")
        output_json = self._build_full_dict()

        # Save analysis results to json file
        with open(self.sound_file_directory/"audio_analysis.json", "w") as outfile:
            outfile.write(output_json)

        print("Output saved.")

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
    # pcsa.print_audio_analysis_results()