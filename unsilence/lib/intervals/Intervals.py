from unsilence.lib.intervals.Interval import Interval


class Intervals:
    """
    Collection of lib.Intervals.Interval
    """

    def __init__(self, interval_list: list = None):
        """
        Initializes a new Interval Collection
        :param interval_list: list of intervals, optional
        """
        if interval_list is None:
            interval_list = []

        self.__interval_list = interval_list

    def add_interval(self, interval):
        """
        Adds an interval to the collection
        :param interval: interval to be added
        :return: None
        """
        self.__interval_list.append(interval)

    @property
    def intervals(self):
        """
        Returns the list of intervals
        :return:
        """
        return self.__interval_list

    def optimize(self, short_interval_threshold=0.3, stretch_time=0.25):
        """
        Optimizes the Intervals to be a better fit for media cutting
        :param short_interval_threshold: The shortest allowed interval length (in seconds)
        :param stretch_time: The time that should be added/removed from a audible/silent interval
        :return: None
        """
        self.__combine_intervals(short_interval_threshold)
        self.__enlarge_audible_intervals(stretch_time)

    def __combine_intervals(self, short_interval_threshold):
        """
        Combines multiple intervals in order to remove intervals smaller than a threshold
        :param short_interval_threshold: Threshold for the shortest allowed interval
        :return: None
        """
        intervals = []
        current_interval = Interval(is_silent=None)

        for interval in self.__interval_list:
            if interval.duration <= short_interval_threshold or current_interval.is_silent == interval.is_silent:
                current_interval.end = interval.end

            else:
                if current_interval.is_silent is None:
                    current_interval.is_silent = interval.is_silent
                    current_interval.end = interval.end
                else:
                    intervals.append(current_interval)
                    current_interval = interval.copy()

        if current_interval.is_silent is None:
            current_interval.is_silent = False

        intervals.append(current_interval)

        self.__interval_list = intervals

    def __enlarge_audible_intervals(self, stretch_time):
        """
        Enlarges/Shrinks intervals based on if they are silent or audible
        :param stretch_time: Time the intervals should be enlarged/shrunken
        :return: None
        """
        for i, interval in enumerate(self.__interval_list):
            interval.enlarge_audible_interval(
                stretch_time,
                is_start_interval=(i == 0),
                is_end_interval=(i == len(self.__interval_list) - 1)
            )

    def copy(self):
        """
        Creates a deep copy
        :return: Deep copy of Intervals
        """
        new_interval_list = [interval.copy() for interval in self.__interval_list]

        return Intervals(new_interval_list)

    def serialize(self):
        """
        Serializes this collection
        :return: Serialized list
        """
        return [interval.serialize() for interval in self.__interval_list]

    @staticmethod
    def deserialize(serialized_obj):
        """
        Deserializes a previously serialized object and creates a new Instance from it
        :param serialized_obj: Serialized list
        :return: New instance of Intervals
        """
        interval_list = [Interval.deserialize(serialized_interval) for serialized_interval in serialized_obj]
        return Intervals(interval_list)

    def __repr__(self):
        """
        String representation
        :return: String representation
        """
        return str(self.__interval_list)
