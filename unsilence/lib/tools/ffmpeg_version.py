import re
import subprocess
from pkg_resources import parse_version


def is_ffmpeg_usable():
    try:
        console_output = subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        ).stdout
    except FileNotFoundError:
        return "not_detected"

    console_output = str(console_output)

    regex = r"libavutil\s*((?:\d+\.\s*){2}\d+)"
    match = re.search(regex, str(console_output))

    if match:
        groups = match.groups()
        version_string = "".join(groups[0].split())

        # Version 56.31.100 is the libavutil version used in the ffmpeg release 4.2.4 "Ada"
        if parse_version(version_string) >= parse_version("56.31.100"):
            return "usable"

        else:
            return "requirements_unsatisfied"

    return "unknown_version"
