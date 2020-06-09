import argparse
from pathlib import Path


def convert_to_path(should_exist=True, should_parents_exist=True):
    """
    Sets options for the nested class
    :param should_exist: If the file needs to exists
    :param should_parents_exist: If the files parents need to exist
    :return: Nested Handle Function
    """

    def handle(s):
        """
        Checks whether the string s fulfils the options set earlier
        :param s: Input string
        :return: Path Object or None
        """
        path = Path(s).absolute()
        if not path.exists() and should_exist:
            raise FileNotFoundError("File does not exist")

        if not path.parent.exists() and should_parents_exist:
            raise IOError("Parent directory not found")

        return path

    return handle


def number_bigger_than_zero(s):
    """
    Returns the Number representation of s if it is bigger than zero, else an error occurs
    :param s: Input string
    :return: Integer or None
    """
    i = int(s)

    if i <= 0:
        raise ValueError("Value must be larger than 0")

    return i


def parse_arguments():
    """
    Parses console arguments for the Unsilence Console Interface
    :return: List of Console Line Arguments
    """
    parser = argparse.ArgumentParser(
        description="Remove silence from media files",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("input_file", type=convert_to_path(should_exist=True),
                        help="Path to the file that contains silence")
    parser.add_argument("output_file", type=convert_to_path(should_exist=False, should_parents_exist=True),
                        help="Path to where the finished media file should be")

    parser.add_argument("-ao", "--audio-only", action="store_true",
                        help="Whether the output should not contain a video channel")

    parser.add_argument("-as", "--audible-speed", type=float, default=1,
                        help="The speed at which audible parts should be played back at")
    parser.add_argument("-ss", "--silent-speed", type=float, default=6,
                        help="The speed at which silent parts should be played back at")
    parser.add_argument("-av", "--audible-volume", type=float, default=1,
                        help="The volume at which audible parts should be played back at")
    parser.add_argument("-sv", "--silent-volume", type=float, default=0.5,
                        help="The volume at which silent parts should be played back at")
    parser.add_argument("-dci", "--drop-corrupted-intervals", action="store_true",
                        help="Whether corrupted video intervals should be discarded or tried to recover")

    parser.add_argument("-t", "--threads", type=number_bigger_than_zero, default=2,
                        help="Number of threads to be used while rendering")
    parser.add_argument("-sl", "--silence-level", type=float, default=-35,
                        help="Minimum volume in decibel to be classified as audible")
    parser.add_argument("-stt", "--silence-time-threshold", type=float, default=0.5,
                        help="Resolution of the silence detection (seconds)")
    parser.add_argument("-sit", "--short-interval-threshold", type=float, default=0.3,
                        help="Intervals smaller than this value (seconds) get combined into a larger interval")
    parser.add_argument("-st", "--stretch-time", type=float, default=0.25,
                        help="Time (seconds) that should be added to audible intervals and removed from silent "
                             "intervals")

    parser.add_argument("-y", "--non-interactive-mode", action="store_true",
                        help="Always answers yes if a dialog would show up")

    parser.add_argument("-d", "--debug", action="store_true",
                        help="Enable debug output (StackTrace)")

    return parser.parse_args()
