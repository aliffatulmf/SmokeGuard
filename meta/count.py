import time
from collections import deque


class MeterError(Exception):
    """A custom exception used to report errors in use of FPSMaster class"""


class FPSMaster:
    def __init__(self, maxlen=50):
        self._start_time = None
        self._times = deque(maxlen=maxlen)
        self._frame_count = 0

    def start_fps(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise MeterError(f"Meter is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop_fps(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise MeterError(f"Meter is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._times.append(elapsed_time)
        self._start_time = None
        print(f"Elapsed time: {elapsed_time:0.4f} milliseconds")

    def stats_fps(self):
        """Return the min, max, avg time, and FPS"""
        total_time = sum(self._times)
        fps = self._frame_count / total_time if total_time > 0 else 0
        return [min(self._times), max(self._times), sum(self._times)/len(self._times), fps]

    def realtime_stats(self):
        """Return the real-time min, max, avg time, and FPS"""
        elapsed_time = time.perf_counter() - self._start_time if self._start_time is not None else 0
        total_time = sum(self._times) + elapsed_time
        fps = self._frame_count / total_time if total_time > 0 else 0
        return [min(self._times), max(self._times), sum(self._times)/len(self._times), fps]

    def extend_fps(self, other_meter):
        """Extend the times with the times from another meter"""
        if not isinstance(other_meter, FPSMaster):
            raise ValueError("Can only extend with another FPSMaster instance")
        self._times.extend(other_meter._times)

    def inc_fps(self):
        """Increment the frame count"""
        self._frame_count += 1


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""


class InferenceTimer:
    def __init__(self, maxlen=50):
        self._start_time = None
        self._times = deque(maxlen=maxlen)

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._times.append(elapsed_time)
        self._start_time = None
        # print(f"Elapsed time: {elapsed_time:0.4f} milliseconds")

    def stats(self):
        """Return the min, max, and avg time"""
        return [min(self._times), max(self._times), sum(self._times)/len(self._times), self._times[-1]]

    def extend(self, other_timer):
        """Extend the times with the times from another timer"""
        if not isinstance(other_timer, InferenceTimer):
            raise ValueError(
                "Can only extend with another InferenceTimer instance")
        self._times.extend(other_timer._times)
