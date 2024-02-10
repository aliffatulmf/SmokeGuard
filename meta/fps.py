"""
Meta FPS

This module contains the meta FPS class for measuring the frames per second of a video stream.
"""

import time


class FPS:
    """
    A class for measuring the frames per second (FPS) of a video stream.

    This class allows for the start, update, pause, and resume of FPS measurement. It also provides
    a method to get the current FPS.

    Attributes:
        __start_time: The time when the FPS measurement started.
        __frame_count: The number of frames counted since the start of the measurement.
        __fps: The calculated frames per second.
        __min_time: The minimum time between frames, in seconds.

    Example:
        >>> fps = FPS()
        >>> fps.start()
        >>> # for each frame in the video stream
        >>> fps.update()
        >>> print(f"Current FPS: {fps.frame_rate}")
    """

    def __init__(self, min_time=0.01):
        """
        Initialize the FPS with the start time as None, frame count as 0, and fps as 0.
        """
        self.__last_update_time = None
        self.__frame_count = 0
        self.__fps = 0
        self.__min_time = min_time

    def start(self):
        """
        Start the FPS measurement by setting the start time to the current time.
        """
        self.__last_update_time = time.time()

    def update(self):
        """
        Update the FPS measurement by incrementing the frame count, calculating the elapsed time
        since the last update, and updating the FPS value if enough time has passed.
        """
        self.__frame_count += 1
        duration = time.time() - self.__last_update_time
        if duration >=  self.__min_time:
            self.__fps = self.__frame_count / duration
            self.__last_update_time = time.time()

    @property
    def frame_rate(self):
        """
        Get the current frames per second.

        Returns:
            The current frames per second.
        """
        return self.__fps


class FPSStats:
    """
    A class for collecting and calculating statistics about frames per second (FPS).

    This class allows for the collection of individual FPS values and provides
    methods to calculate the maximum, minimum, and average FPS.

    Attributes:
        fps_values: A list of FPS values.

    Example:
        >>> stats = FPSStats()
        >>> stats.add_fps(30)
        >>> stats.add_fps(60)
        >>> stats.add_fps(45)
        >>> print(f"Max FPS: {stats.max_fps}")
        >>> print(f"Min FPS: {stats.min_fps}")
        >>> print(f"Avg FPS: {stats.avg_fps}")
        >>> stats.clear()
    """

    def __init__(self):
        """
        Initialize the FPSStats with an empty list of fps_values.
        """
        self.fps_values = []

    def add_fps(self, fps):
        """
        Add an FPS value to the list of fps_values.

        Args:
            fps: The FPS value to add.
        """
        assert isinstance(fps, (int, float)), "FPS must be an int or a float."
        assert fps >= 0, "FPS must be a positive number."
        self.fps_values.append(fps)

    def clear(self):
        """
        Clear the list of fps_values.
        """
        self.fps_values.clear()

    @property
    def max_fps(self):
        """
        Calculate and return the maximum FPS value.

        Returns:
            The maximum FPS value, or None if no FPS values have been added.
        """
        return max(self.fps_values) if self.fps_values else None

    @property
    def min_fps(self):
        """
        Calculate and return the minimum FPS value.

        Returns:
            The minimum FPS value, or None if no FPS values have been added.
        """
        return min(self.fps_values) if self.fps_values else None

    @property
    def avg_fps(self):
        """
        Calculate and return the average FPS value.

        Returns:
            The average FPS value, or None if no FPS values have been added.
        """
        if not self.fps_values:
            return 0
        return sum(self.fps_values) / len(self.fps_values) if self.fps_values else None
