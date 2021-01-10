import sys

from rich.console import Console
from rich.progress import Progress

from unsilence.Unsilence import Unsilence
from unsilence.command_line.ChoiceDialog import choice_dialog
from unsilence.command_line.ParseArguments import parse_arguments
from unsilence.command_line.PrettyTimeEstimate import pretty_time_estimate, pretty_time_estimate_sla
from unsilence.command_line.TerminalSupport import repair_console


def main():
    """
    Entry Point if this script is run as a script instead of a library
    :return: None
    """
    try:
        repair_console()
        run()
    except KeyboardInterrupt:
        print("\nInterrupted")

    repair_console()
    sys.exit(0)


def run(sla=False):
    """
    Run the Console Interface for Unsilence
    optional argument :sla: -  True if the user wishes to rerun with sla on after finding output to be same as input.
    :return: None
    """
    sys.tracebacklimit = 0

    args = parse_arguments()
    console = Console()

    if args.debug:
        sys.tracebacklimit = 1000

    if args.output_file.exists() and not args.non_interactive_mode and not sla: # Don't ask whether want to overwrite second time when ran with SLA.
        if not choice_dialog(console, "File already exists. Overwrite?", default=False):
            return

    args_dict = vars(args)

    argument_list_for_silence_detect = [
        "silence_level", "silence_time_threshold", "short_interval_threshold", "stretch_time"
    ]

    argument_dict_for_silence_detect = {
        key: args_dict[key] for key in argument_list_for_silence_detect if key in args_dict.keys()
    }

    argument_list_for_renderer = [
        "audio_only", "audible_speed", "silent_speed", "audible_volume", "silent_volume",
        "drop_corrupted_intervals", "threads"
    ]

    argument_dict_for_renderer = {
        key: args_dict[key] for key in argument_list_for_renderer if key in args_dict.keys()
    }

    progress = Progress()

    continual = Unsilence(args.input_file)

    with progress:
        def update_task(current_task):
            def handler(current_val, total):
                progress.update(current_task, total=total, completed=current_val)
                
            return handler

        if sla:   #If user wishes to rerun with SLA on
            args.silence_level_analysis = "normal"
        if args.silence_level_analysis:
            argument_dict_for_sla = argument_dict_for_silence_detect.copy()
            estimated_times = {}

            sla_levels = {'low': range(-60, -35, 5),  # -60 to -40
                          'normal': range(-45, -20, 5),  # -45 to -25
                          'high': range(-35, -10, 5),  # -35 to -15
                          'full': range(-60, -5, 5)}  # -60 to -10

            for silence_level in sla_levels[args.silence_level_analysis]:
                progress.start()
                sla_subtask = progress.add_task("SLA for silence level " + str(silence_level), total=1)
                argument_dict_for_sla['silence_level'] = silence_level
                continual.detect_silence(on_silence_detect_progress_update=update_task(sla_subtask), **argument_dict_for_sla)
                estimated_times['silence_level_'+str(silence_level)] = continual.estimate_time(args.audible_speed, args.silent_speed)
                progress.stop()
                progress.remove_task(sla_subtask)

            console.print(pretty_time_estimate_sla(estimated_times))
            if not args.non_interactive_mode:
                if not choice_dialog(console, "Silence level analysis finished. Continue with original silence level?", default=True):
                    while True:
                        try:
                            new_silence_level = float(console.input("Enter a new silence level value: "))
                            break
                        except ValueError:
                            console.print("Please enter a valid value (float)")
                    argument_dict_for_silence_detect['silence_level'] = new_silence_level

        progress.start()
        silence_detect_task = progress.add_task("Calculating Intervals...", total=1)

        continual.detect_silence(
            on_silence_detect_progress_update=update_task(silence_detect_task),
            **argument_dict_for_silence_detect
        )

        progress.stop()
        progress.remove_task(silence_detect_task)

        print()

        estimated_time = continual.estimate_time(args.audible_speed, args.silent_speed)
        console.print(pretty_time_estimate(estimated_time))

        if not args.non_interactive_mode:
            if estimated_time['delta']['all'][0] == 0 and estimated_time['delta']['audible'][0] == 0 and estimated_time['delta']['silent'][0] == 0:
                console.print("There is no change with the current parameters.")
                if choice_dialog(console, "Run silence level analysis (sla) to find silence levels? Press n to continue instead anyway.", default="True"):
                    run(sla=True)
                    return

            elif not choice_dialog(console, "Continue with these options?", default=True):
                return

        progress.start()
        rendering_task = progress.add_task("Rendering Intervals...", total=1)
        concat_task = progress.add_task("Combining Intervals...", total=1)

        continual.render_media(
            args.output_file,
            on_render_progress_update=update_task(rendering_task),
            on_concat_progress_update=update_task(concat_task),
            **argument_dict_for_renderer
        )

        progress.stop()

    console.print("\n[green]Finished![/green] :tada:")
    print()
