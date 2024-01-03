import time
from collections import deque


class InferenceTime:
    def __init__(self, lim=None):
        self._start_ns = None
        self.stats = [0.0, 0.0, 0.0, 0.0]   # [last, min, max, avg]
        self.stack = deque(maxlen=lim)

    def start(self):
        """Start the timer."""
        if self._start_ns is not None:
            raise RuntimeError("InferenceTime already started. Call stop before starting again.")
        self._start_ns = time.perf_counter_ns()

    def stop(self):
        """Stop the timer and update the statistics."""
        if self._start_ns is None:
            raise RuntimeError("InferenceTime not started. Call start before stopping.")
        duration = (time.perf_counter_ns() - self._start_ns) / 1e6
        self.stack.append(duration)
        self.stats = [duration, min(self.stack), max(self.stack), sum(self.stack) / len(self.stack)]
        self._start_ns = None

    def reset(self):
        """Reset the statistics and stack."""
        self._start_ns = None
        self.stats = [0.0, 0.0, 0.0, 0.0]
        self.stack.clear()