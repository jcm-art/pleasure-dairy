
import pathlib


class PleasureComfortSoundAnalyzer:

    def __init__(self, sound_file_directory_path) -> None:
        self.sound_file_directory = pathlib.Path(sound_file_directory_path)

    def get_sound_file_paths(self) -> list:
        pass

    def analyze_sound_files(self) -> list:
        pass

    def _analyze_sound(self, sound_file_path: str) -> dict:
        pass

    def _save_sound_analysis_result(self) -> None:
        pass


if __name__ == '__main__':
    pcsa = PleasureComfortSoundAnalyzer(sound_file_directory_path='./tmp/sounds')
    pcsa.get_sound_file_paths()
    pcsa.analyze_sound_files()