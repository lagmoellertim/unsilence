from unsilence.lib.intervals.Intervals import Intervals


def calculate_time(intervals: Intervals, audible_speed: float, silent_speed: float):
    """
    Generates a time estimate on the time saved if the current speed settings get applied
    :param intervals: Intervals which should be estimated (lib.Intervals.Intervals)
    :param audible_speed: The speed at which audible intervals should be played back at
    :param silent_speed: The speed at which silent intervals should be played back at
    :return: Time calculation dict
    """
    time_data = {"before": {}, "after": {}, "delta": {}}
    audible = 0
    silent = 0
    for interval in intervals.intervals:
        if interval.is_silent:
            silent += interval.duration
        else:
            audible += interval.duration

    time_data["before"]["all"] = (audible + silent, 1)
    time_data["before"]["audible"] = (audible, audible / time_data["before"]["all"][0])
    time_data["before"]["silent"] = (silent, silent / time_data["before"]["all"][0])

    new_audible = audible / audible_speed
    new_silent = silent / silent_speed

    time_data["after"]["all"] = (new_audible + new_silent, (new_audible + new_silent) / time_data["before"]["all"][0])
    time_data["after"]["audible"] = (new_audible, new_audible / time_data["before"]["all"][0])
    time_data["after"]["silent"] = (new_silent, new_silent / time_data["before"]["all"][0])

    time_data["delta"]["all"] = (
        time_data["after"]["all"][0] - time_data["before"]["all"][0],
        time_data["after"]["all"][1] - time_data["before"]["all"][1]
    )

    time_data["delta"]["audible"] = (
        time_data["after"]["audible"][0] - time_data["before"]["audible"][0],
        time_data["after"]["audible"][1] - time_data["before"]["audible"][1]
    )

    time_data["delta"]["silent"] = (
        time_data["after"]["silent"][0] - time_data["before"]["silent"][0],
        time_data["after"]["silent"][1] - time_data["before"]["silent"][1]
    )

    # Timedelta not working like i want

    return time_data
