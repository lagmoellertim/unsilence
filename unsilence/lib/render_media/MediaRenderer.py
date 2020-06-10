import queue
import shutil
import subprocess
import threading
import time
import uuid
from pathlib import Path
from types import SimpleNamespace

from unsilence.lib.intervals.Intervals import Intervals
from unsilence.lib.render_media.RenderIntervalThread import RenderIntervalThread


class MediaRenderer:
    """
    The Media Renderer handles the rendering of Intervals objects, so it processes the complete video and concatenates
    the different intervals at the end
    """

    def __init__(self, temp_path: Path):
        """
        Initializes a new MediaRenderer Object
        :param temp_path: The temp path where all temporary files should be stored
        """
        self.__temp_path = Path(temp_path).absolute()

    def render(self, input_file: Path, output_file: Path, intervals: Intervals, **kwargs):
        """
        Renders an input_file and writes the final output to output_file
        :param input_file: The file that should be processed
        :param output_file: Where the processed file should be saved
        :param intervals: The Intervals that should be processed
        :param kwargs: Keyword Args, see below
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
        input_file = Path(input_file).absolute()
        output_file = Path(output_file).absolute()

        if not input_file.exists():
            raise FileNotFoundError(f"Input file {input_file} does not exist!")

        render_options = SimpleNamespace(
            audio_only=kwargs.get("audio_only", False),
            audible_speed=kwargs.get("audible_speed", 1),
            silent_speed=kwargs.get("silent_speed", 6),
            audible_volume=kwargs.get("audible_volume", 1),
            silent_volume=kwargs.get("silent_volume", 0.5),
            drop_corrupted_intervals=kwargs.get("drop_corrupted_intervals", False)
        )

        video_temp_path = self.__temp_path / str(uuid.uuid4())
        video_temp_path.mkdir(parents=True)

        concat_file = video_temp_path / "concat_list.txt"
        final_output = video_temp_path / f"out_final{output_file.suffix}"

        file_list = []

        thread_lock = threading.Lock()
        task_queue = queue.Queue()
        thread_list = []
        completed_tasks = []
        corrupted_intervals = []

        def handle_thread_completed_task(completed_task, corrupted):
            """
            Nested function that is called when a thread completes it current task
            :param completed_task: The completed task
            :param corrupted: If the task contained a corrupted media part
            :return: None
            """
            func = kwargs.get("on_render_progress_update", None)

            thread_lock.acquire()

            if not corrupted:
                completed_tasks.append(completed_task)
                if func is not None:
                    func(len(completed_tasks), len(intervals.intervals))
            else:
                corrupted_intervals.append(completed_task)

            thread_lock.release()

        for i in range(kwargs.get("threads", 2)):
            thread = RenderIntervalThread(i, input_file, render_options, task_queue, thread_lock,
                                          on_task_completed=handle_thread_completed_task)
            thread.start()
            thread_list.append(thread)

        for i, interval in enumerate(intervals.intervals):
            current_file_name = f"out_{i}{output_file.suffix}"
            current_path = video_temp_path / current_file_name

            file_list.append(current_path)

            task = SimpleNamespace(task_id=i, interval_output_file=current_path, interval=interval)

            thread_lock.acquire()
            task_queue.put(task)
            thread_lock.release()

        while len(completed_tasks) < (len(intervals.intervals) - len(corrupted_intervals)):
            time.sleep(0.5)

        for thread in thread_list:
            thread.stop()

        completed_file_list = [task.interval_output_file for task in sorted(completed_tasks, key=lambda x: x.task_id)]

        MediaRenderer.__concat_intervals(
            completed_file_list,
            concat_file,
            final_output,
            kwargs.get("on_concat_progress_update", None)
        )

        shutil.move(final_output, output_file)
        shutil.rmtree(video_temp_path)

    @staticmethod
    def __concat_intervals(file_list: list, concat_file: Path, output_file: Path, update_concat_progress):
        """
        Concatenates all interval files to create a finished file
        :param file_list: List of interval files
        :param concat_file: Where the ffmpeg concat filter file should be saved
        :param output_file: Where the final output file should be saved
        :param update_concat_progress: A function that is called when a step is finished
            (called like function(current, total))
        :return: None
        """
        total_files = len(file_list)

        with open(str(concat_file), "w+") as file:
            lines = [f"file {interval_file}\n" for interval_file in file_list]
            file.writelines(lines)

        command = [
            "ffmpeg",
            "-f", "concat",
            "-safe", "0",
            "-i", f"{concat_file}",
            "-c", "copy",
            "-y",
            "-loglevel", "verbose",
            f"{output_file}"
        ]

        console_output = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )

        current_file = 0
        for line in console_output.stdout:
            if "Auto-inserting" in line:
                if update_concat_progress is not None:
                    current_file += 1
                    update_concat_progress(current_file, total_files)
