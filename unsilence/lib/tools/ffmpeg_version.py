import re
import subprocess


def get_ffmpeg_version():
    try:
        console_output = subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        ).stdout
    except FileNotFoundError:
        return None

    regex = r"ffmpeg version \D?(\d+(?:\.\d+)*)"
    match = re.search(regex, str(console_output))

    groups = match.groups()
    version = groups[0].split(".")

    return [int(version_part) for version_part in version]
