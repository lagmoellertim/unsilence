class Interval:
    """
    Represents a section in time where the media file is either silent or audible
    """

    def __init__(self, start=0, end=0, is_silent=False):
        """
        Initializes an Interval object
        :param start: Start time of the interval in seconds
        :param end: End time of the interval in seconds
        :param is_silent: Whether the interval is silent or not
        """
        self.__start = start
        self.__end = end
        self.__duration = self.__end - self.__start
        self.is_silent = is_silent

    @property
    def start(self):
        """
        Get the start time
        :return: start time in seconds
        """
        return self.__start

    @start.setter
    def start(self, new_start):
        """
        Sets the new start time and updates the duration
        :param new_start: start time in seconds
        :return: None
        """
        self.__start = new_start
        self.__duration = self.__end - self.__start

    @property
    def end(self):
        """
        Get the end time
        :return: end time in seconds
        """
        return self.__end

    @end.setter
    def end(self, new_end):
        """
        Sets the new end time and updates the duration
        :param new_end: start time in seconds
        :return: None
        """
        self.__end = new_end
        self.__duration = self.__end - self.__start

    @property
    def duration(self):
        """
        Returns the duration of the interval
        :return: Duration of the interval
        """
        return self.__duration

    def enlarge_audible_interval(self, stretch_time, is_start_interval=False, is_end_interval=False):
        """
        Enlarges/Shrinks the audio interval, based on if it is silent or not
        :param stretch_time: Time the interval should be enlarged/shrunken
        :param is_start_interval: Whether the current interval is at the start (should not enlarge/shrink)
        :param is_end_interval: Whether the current interval is at the end (should not enlarge/shrink)
        :return: None
        """
        if stretch_time >= self.duration:
            raise Exception("Stretch time to large, please choose smaller size")

        stretch_time_part = (-1 if self.is_silent else 1) * stretch_time / 2

        if not is_start_interval:
            self.start -= stretch_time_part

        if not is_end_interval:
            self.end += stretch_time_part

    def copy(self):
        """
        Creates a deep copy of this Interval
        :return: Interval deepcopy
        """
        return Interval(self.start, self.end, self.is_silent)

    def serialize(self):
        """
        Serializes the current interval into a dict format
        :return: serialized dict
        """
        return {"start": self.start, "end": self.end, "is_silent": self.is_silent}

    @staticmethod
    def deserialize(serialized_obj: dict):
        """
        Deserializes a previously serializes Interval and generates a new Interval with this data
        :param serialized_obj: previously serializes Interval (type dict)
        :return: Interval
        """
        return Interval(serialized_obj["start"], serialized_obj["end"], serialized_obj["is_silent"])

    def __repr__(self):
        """
        String representation
        :return: String representation
        """
        return f"<Interval start={self.start} end={self.end} duration={self.duration} is_silent={self.is_silent}>"
