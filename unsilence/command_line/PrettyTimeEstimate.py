import datetime

from rich.table import Table


def format_timedelta(seconds):
    """
    Generates a pretty time representation for seconds (format: hour:minute:second)
    :param seconds: Amount of seconds (can be negative)
    :return: String representation
    """
    if seconds < 0:
        return f"-{datetime.timedelta(seconds=-seconds)}"
    else:
        return str(datetime.timedelta(seconds=seconds))


def pretty_time_estimate(time_data: dict):
    """
    Generates a rich.table.Table object from the time_data dict (from lib.Intervals.TimeCalculations.calculate_time)
    :param time_data: time_data dict (from lib.Intervals.TimeCalculations.calculate_time)
    :return: rich.table.Table object
    """
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Type")
    table.add_column("Before")
    table.add_column("After")
    table.add_column("Difference")

    reorderer_time_data = {"all": {}, "audible": {}, "silent": {}}
    for column, row_with_values in time_data.items():
        for row, values in row_with_values.items():
            time_delta = format_timedelta(round(values[0]))
            reorderer_time_data[row][column] = f"{time_delta} ([cyan]{round(values[1] * 100, 1)}%[/cyan])"

    table.add_row(
        "Combined",
        reorderer_time_data["all"]["before"],
        reorderer_time_data["all"]["after"],
        reorderer_time_data["all"]["delta"]
    )

    table.add_row(
        "Audible",
        reorderer_time_data["audible"]["before"],
        reorderer_time_data["audible"]["after"],
        reorderer_time_data["audible"]["delta"]
    )

    table.add_row(
        "Silent",
        reorderer_time_data["silent"]["before"],
        reorderer_time_data["silent"]["after"],
        reorderer_time_data["silent"]["delta"]
    )

    return table
