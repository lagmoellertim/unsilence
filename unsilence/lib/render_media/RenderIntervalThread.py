import pathlib
import queue
import subprocess
import threading
from types import SimpleNamespace

from unsilence.lib.intervals.Interval import Interval


class RenderIntervalThread(threading.Thread):
    """
    Worker thread that can render/process intervals based on defined options
    """

    def __init__(self, thread_id, input_file: pathlib.Path, render_options: SimpleNamespace, task_queue: queue.Queue,
                 thread_lock: threading.Lock, **kwargs):
        """
        Initializes a new Worker (is run in daemon mode)
        :param thread_id: ID of this thread
        :param input_file: The file the worker should work on
        :param render_options: The parameters on how the video should be processed, more details below
        :param task_queue: A queue object where the worker can get more tasks
        :param thread_lock: A thread lock object to acquire and release thread locks
        :param kwargs: Keyword Args, see below for more information
        """
        super().__init__()
        self.daemon = True
        self.thread_id = thread_id
        self.task_queue = task_queue
        self.thread_lock = thread_lock
        self.__should_exit = False
        self.__input_file = input_file
        self.__on_task_completed = kwargs.get("on_task_completed", None)
        self.__render_options = render_options

    def run(self):
        """
        Start the worker. Worker runs until stop() is called. It runs in a loop, takes a new task if available, and
        processes it
        :return: None
        """
        while not self.__should_exit:
            self.thread_lock.acquire()

            if not self.task_queue.empty():
                task: SimpleNamespace = self.task_queue.get()
                self.thread_lock.release()

                completed = self.__render_interval(
                    task.interval_output_file,
                    task.interval,
                    drop_corrupted_intervals=self.__render_options.drop_corrupted_intervals
                )

                if self.__on_task_completed is not None:
                    self.__on_task_completed(task, not completed)
            else:
                self.thread_lock.release()

    def stop(self):
        """
        Stops the worker after its current task is finished
        :return:
        """
        self.__should_exit = True

    def __render_interval(self, interval_output_file: pathlib.Path, interval: Interval,
                          apply_filter=True, drop_corrupted_intervals=False):
        """
        Renders an interval with the given render options
        :param interval_output_file: Where the current output file should be saved
        :param interval: The current Interval that should be processed
        :param apply_filter: Whether the AV-Filter should be applied or if the media interval should be left untouched
        :param drop_corrupted_intervals: Whether to remove corrupted frames from the video or keep them in unedited
        :return: Whether it is corrupted or not
        """

        command = self.__generate_command(interval_output_file, interval, apply_filter)

        console_output = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        if "Conversion failed!" in str(console_output.stdout).splitlines()[-1]:
            if drop_corrupted_intervals:
                return False
            if apply_filter:
                self.__render_interval(
                    interval_output_file,
                    interval,
                    apply_filter=False,
                    drop_corrupted_intervals=drop_corrupted_intervals
                )
            else:
                raise IOError(f"Input file is corrupted between {interval.start} and {interval.end} (in seconds)")

        if "Error initializing complex filter" in str(console_output.stdout):
            raise ValueError("Invalid render options")

        return True

    def __generate_command(self, interval_output_file: pathlib.Path, interval: Interval, apply_filter: bool):
        """
        Generates the ffmpeg command to process the video
        :param interval_output_file: Where the media interval should be saved
        :param interval: The current interval
        :param apply_filter: Whether a filter should be applied or not
        :return: ffmpeg console command
        """
        command = [
            "ffmpeg",
            "-ss", f"{interval.start}",
            "-to", f"{interval.end}",
            "-i", f"{self.__input_file}",
            "-vsync", "1",
            "-async", "1",
            "-safe", "0",
            "-ignore_unknown", "-y",
        ]

        if apply_filter:
            complex_filter = []

            if interval.is_silent:
                current_speed = self.__render_options.silent_speed
                current_volume = self.__render_options.silent_volume
            else:
                current_speed = self.__render_options.audible_speed
                current_volume = self.__render_options.audible_volume

            if not self.__render_options.audio_only:
                complex_filter.extend([
                    f"[0:v]setpts={round(1 / current_speed, 4)}*PTS[v]",
                ])

            complex_filter.extend([
                f"[0:a]atempo={round(current_speed, 4)},volume={current_volume}[a]",
            ])

            command.extend(
                ["-filter_complex", ";".join(complex_filter)]
            )

            if not self.__render_options.audio_only:
                command.extend(["-map", "[v]"])

            command.extend(["-map", "[a]"])
        else:
            if self.__render_options.audio_only:
                command.append("-vn")

        command.append(str(interval_output_file))

        return command
