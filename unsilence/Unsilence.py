import atexit
import shutil
from pathlib import Path

from unsilence.lib.detect_silence.DetectSilence import detect_silence
from unsilence.lib.intervals.Intervals import Intervals
from unsilence.lib.intervals.TimeCalculations import calculate_time
from unsilence.lib.render_media.MediaRenderer import MediaRenderer


class Unsilence:
    """
    Unsilence Class to remove (or isolate or many other use cases) silence from audible video parts
    """

    def __init__(self, input_file: Path, temp_dir: Path = Path(".tmp")):
        """
        Initializes a new Unsilence Object
        :param input_file: The file that should be processed
        :param temp_dir: The temp dir where temporary files can be saved
        """
        self.__input_file = Path(input_file)
        self.__temp_dir = Path(temp_dir)
        self.__intervals: Intervals = None
        atexit.register(self.cleanup)

    def detect_silence(self, **kwargs):
        """
        Detects silence of the file (Options can be specified in kwargs)
        :param kwargs: Keyword Args, more information below
        :return: A generated Intervals object

        kwargs:
            silence_level: Threshold of what should be classified as silent/audible (default -35) (in dB)
            silence_time_threshold: Resolution of the ffmpeg detection algorithm (default 0.5) (in seconds)
            short_interval_threshold : The shortest allowed interval length (default: 0.3) (in seconds)
            stretch_time: Time the interval should be enlarged/shrunken (default 0.25) (in seconds)
            on_silence_detect_progress_update: Function that should be called on progress update
                (called like: func(current, total))
        """
        self.__intervals = detect_silence(self.__input_file, **kwargs)
        return self.__intervals

    def set_intervals(self, intervals: Intervals):
        """
        Set the intervals so that they do not need to be re-detected
        :param intervals: Intervals collection
        :return: None
        """
        self.__intervals = intervals

    def get_intervals(self):
        """
        Get the current Intervals so they can be reused if wanted
        :return: Intervals collection
        """
        return self.__intervals

    def estimate_time(self, audible_speed: float = 6, silent_speed: float = 1):
        """
        Estimates the time (savings) when the current options are applied to the intervals
        :param audible_speed: The speed at which the audible intervals get played back at
        :param silent_speed: The speed at which the silent intervals get played back at
        :return: Dictionary of time information
        :exception: ValueError if silence detection was never run
        """
        if self.__intervals is None:
            raise ValueError("Silence detection was not yet run and no intervals where given manually!")

        return calculate_time(self.__intervals, audible_speed, silent_speed)

    def render_media(self, output_file: Path, **kwargs):
        """
        Renders the current intervals with options specified in the kwargs
        :param output_file: Where the final file should be saved at
        :param kwargs: Keyword args, more information below
        :return: None

        kwargs:
            audio_only: Whether the output should be audio only (bool)
            audible_speed: The speed at which the audible intervals get played back at (float)
            silent_speed: The speed at which the silent intervals get played back at (float)
            audible_volume: The volume at which the audible intervals get played back at (float)
            silent_volume: The volume at which the silent intervals get played back at (float)
            drop_corrupted_intervals: Whether corrupted video intervals should be discarded or tried to recover (bool)
            threads: Number of threads to render simultaneously (int > 0)
            on_render_progress_update: Function that should be called on render progress update
                (called like: func(current, total))
            on_concat_progress_update: Function that should be called on concat progress update
                (called like: func(current, total))
        """
        if self.__intervals is None:
            raise ValueError("Silence detection was not yet run and no intervals where given manually!")

        renderer = MediaRenderer(self.__temp_dir)
        renderer.render(self.__input_file, output_file, self.__intervals, **kwargs)

    def cleanup(self):
        """
        Cleans up the temporary directories, called automatically when the program ends
        :return:
        """
        if self.__temp_dir.exists():
            shutil.rmtree(self.__temp_dir)
