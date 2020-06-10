import os


def repair_console():
    if os.name == "posix":
        os.system("stty sane > /dev/null 2>&1")
