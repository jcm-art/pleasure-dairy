
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import os
import json
from scipy.io import wavfile
import scipy.signal



class SoundAnalysisResults:
    
    def __init__(self, sound_file_path) -> None:
        self.sound_file_path = sound_file_path
        self.sound_analysis_dict = {
            'sample_rate': None,
            'audio_length_seconds': None,
            'highest_amplitude': None,
            'lowest_amplitude': None,
        }

    def set_sampling_rate(self, fs):
        self.sound_analysis_dict['sample_rate'] = fs

    def set_audio_length_seconds(self, audio_length_seconds):
        self.sound_analysis_dict['audio_length_seconds'] = audio_length_seconds
    
    def set_highest_amplitude(self, highest_amplitude):
        self.sound_analysis_dict['highest_amplitude'] = highest_amplitude

    def set_loest_amplitude(self, lowest_amplitude):
        self.sound_analysis_dict['lowest_amplitude'] = lowest_amplitude



class PleasureComfortSoundAnalyzer:

    def __init__(self, sound_file_directory_path) -> None:
        self.sound_file_directory = pathlib.Path(sound_file_directory_path)
        self.sound_file_paths = []
        self.sound_file_dict = {}
        self.sound_file_analysis_results = []


    def get_sound_file_paths(self) -> list:
        print("Getting sound file paths...")
        for root, dirs, files in os.walk(self.sound_file_directory):
            for file in files:
                self.sound_file_paths.append(pathlib.PurePath(root, file))
        print(f"Retrived sound paths: {self.sound_file_paths}")

    def analyze_sound_files(self) -> list:
        print("Analyzing sound files...")
        for path in self.sound_file_paths:
            # Creat new audio analysis class
            audio_analysis = SoundAnalysisResults(path.name)

            # Read in audio file
            fs, wave = scipy.io.wavfile.read(path)

            # Get audio analysis parameters
            self._analyze_sounds(audio_analysis, fs, wave)


            self.sound_file_analysis_results.append(audio_analysis)


    def _analyze_sounds(self, audio_analysis, fs, wave) -> SoundAnalysisResults:
        
        # Set audio analysis parameters
        audio_analysis.set_sampling_rate(fs)
        audio_analysis.set_audio_length_seconds(len(wave)/fs)
        audio_analysis.set_highest_amplitude(float(np.max(wave)))
        audio_analysis.set_loest_amplitude(float(np.min(wave)))
        
        return audio_analysis


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
    pcsa.print_audio_analysis_results()