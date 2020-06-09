import re
import subprocess
from pathlib import Path

from unsilence.lib.intervals.Intervals import Intervals, Interval


def detect_silence(input_file: Path, **kwargs):
    """
    Detects silence in a file and outputs the intervals (silent/not silent) as a lib.Intervals.Intervals object
    :param input_file: File where silence should be detected
    :param kwargs: Various Parameters, see below
    :return: lib.Intervals.Intervals object

    kwargs:
        silence_level: Threshold of what should be classified as silent/audible (default -35) (in dB)
        silence_time_threshold: Resolution of the ffmpeg detection algorithm (default 0.5) (in seconds)
        short_interval_threshold : The shortest allowed interval length (default: 0.3) (in seconds)
        stretch_time: Time the interval should be enlarged/shrunken (default 0.25) (in seconds)
        on_silence_detect_progress_update: Function that should be called on progress update
            (called like: func(current, total))
    """
    input_file = Path(input_file).absolute()

    if not input_file.exists():
        raise FileNotFoundError(f"Input file {input_file} does not exist!")

    silent_detect_progress_update = kwargs.get("on_silence_detect_progress_update", None)

    command = [
        "ffmpeg",
        "-i", str(input_file),
        "-af",
        f"silencedetect=noise={kwargs.get('silence_level', -35)}dB:d={kwargs.get('silence_time_threshold', 0.5)}",
        "-f", "null",
        "-"
    ]

    console_output = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    ).stdout

    intervals = Intervals()
    current_interval = Interval(start=0, end=0, is_silent=False)
    media_duration = None

    for line in console_output:
        if "[silencedetect" in line:
            capture = re.search("\\[silencedetect @ [0-9xa-f]+] silence_([a-z]+): (-?[0-9]+.?[0-9]*[e-]*[0-9]*)",
                                line)

            event = capture[1]
            time = float(capture[2])

            if silent_detect_progress_update is not None:
                silent_detect_progress_update(time, media_duration)

            if event == "start":
                if current_interval.start != time:
                    current_interval.end = time
                    intervals.add_interval(current_interval)
                current_interval = Interval(start=time, is_silent=True)

            if event == "end":
                current_interval.end = time
                intervals.add_interval(current_interval)
                current_interval = Interval(start=time, is_silent=False)

        elif "Duration" in line:
            capture = re.search("Duration: ([0-9:]+.?[0-9]*)", line)
            hour, minute, second_millisecond = capture[1].split(":")
            second, millisecond = second_millisecond.split(".")
            media_duration = float(str(int(second) + 60 * (int(minute) + 60 * int(hour))) + "." + millisecond)

    current_interval.end = media_duration
    intervals.add_interval(current_interval)

    if silent_detect_progress_update is not None:
        silent_detect_progress_update(media_duration, media_duration)

    intervals.optimize(
        kwargs.get('short_interval_threshold', 0.3),
        kwargs.get('stretch_time', 0.25)
    )

    return intervals
