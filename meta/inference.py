"""
Meta Inference

This module contains the meta inference functions for the model.
"""

import time


class InferenceTime:
    """
    A class for measuring the time taken by a section of code, including the ability
    to pause and resume the timer.

    This class allows for timing operations such as model inference, accounting for
    periods where timing should be paused.

    Example:
        >>> inference_timer = InferenceTimer()
        >>> inference_timer.start()
        >>> # Run some lengthy operation
        >>> inference_timer.pause()
        >>> # Run operations that shouldn't be timed
        >>> inference_timer.resume()
        >>> # Continue with timed operations
        >>> inference_timer.stop()
        >>> print(f"Elapsed time: {inference_timer.elapsed} seconds")
    """

    class Status:
        """Enum for the status of the timer."""
        NOT_STARTED = "Not started"
        PAUSED = "Paused"
        RUNNING = "Running"
        ENDED = "Ended"

    def __init__(self):
        """Initialize the timer with start, end, total paused time and the paused state."""
        self._start_time = None
        self._end_time = None
        self._total_paused_time = 0
        self._is_paused = False

    def start(self):
        """Start the timer unless it's already been started."""
        if self._start_time is None:
            self._start_time = time.time()
        else:
            raise RuntimeError("Start has already been called.")

    def stop(self):
        """Stop the timer unless it hasn't been started or is paused."""
        if self._start_time is not None and not self._is_paused:
            self._end_time = time.time()
        else:
            raise RuntimeError(
                "End cannot be called without starting or without resuming after pausing.")

    def pause(self):
        """Pause the timer unless it hasn't been started or is already paused."""
        if self._start_time is not None and not self._is_paused:
            self._total_paused_time += time.time() - self._start_time
            self._is_paused = True
        else:
            raise RuntimeError(
                "Pause cannot be called without starting or without resuming after pausing.")

    def resume(self):
        """Resume the timer unless it hasn't been started or isn't paused."""
        if self._start_time is not None and self._is_paused:
            self._start_time = time.time()
            self._is_paused = False
        else:
            raise RuntimeError(
                "Resume cannot be called without starting or without pausing.")

    @property
    def status(self):
        """Return the status of the timer."""
        if self._start_time is None:
            return self.Status.NOT_STARTED
        elif self._is_paused:
            return self.Status.PAUSED
        elif self._end_time is not None:
            return self.Status.ENDED
        else:
            return self.Status.RUNNING

    @property
    def elapsed(self):
        """
        Calculate and return the elapsed time excluding any paused duration.

        Raises:
            RuntimeError: If called without ever starting the timer.
        """
        if self._start_time is None:
            raise RuntimeError(
                "Elapsed time cannot be calculated without starting.")
        elif self._is_paused:
            return self._total_paused_time
        else:
            return time.time() - self._start_time - self._total_paused_time


class InferenceTimeStats:
    """
    A class for collecting and calculating statistics about inference times.

    This class allows for the collection of individual inference times and provides
    methods to calculate the maximum, minimum, and average inference times.

    Attributes:
        times: A list of inference times.

    Example:
        >>> stats = InferenceTimeStats()
        >>> stats.add_time(1.23)
        >>> stats.add_time(2.34)
        >>> stats.add_time(3.45)
        >>> print(f"Max time: {stats.max_time} seconds")
        >>> print(f"Min time: {stats.min_time} seconds")
        >>> print(f"Avg time: {stats.avg_time} seconds")
        >>> print(stats.values)
        >>> stats.clear()
    """

    def __init__(self):
        """
        Initialize the InferenceTimeStats with an empty list of times.
        """
        self.times = []

    def add_time(self, time):
        """
        Add an inference time to the list of times.

        Args:
            time: The inference time to add.
        """
        assert isinstance(time, (int, float)), "Time must be an int or a float."
        assert time >= 0, "Time must be a positive number."
        self.times.append(time)

    def clear(self):
        """
        Clear the list of times.
        """
        self.times.clear()

    @property
    def max_time(self):
        """
        Calculate and return the maximum inference time.

        Returns:
            The maximum inference time, or None if no times have been added.
        """
        return max(self.times) if self.times else None

    @property
    def min_time(self):
        """
        Calculate and return the minimum inference time.

        Returns:
            The minimum inference time, or None if no times have been added.
        """
        return min(self.times) if self.times else None

    @property
    def avg_time(self):
        """
        Calculate and return the average inference time.

        Returns:
            The average inference time, or None if no times have been added.
        """
        return sum(self.times) / len(self.times) if self.times else None

    @property
    def values(self):
        """
        Return a dictionary of the max, min, and average inference times.

        Returns:
            A dictionary with keys 'max_time', 'min_time', and 'avg_time', and values
            corresponding to the maximum, minimum, and average inference times, respectively.
        """
        return {
            "max_time": self.max_time,
            "min_time": self.min_time,
            "avg_time": self.avg_time,
        }
