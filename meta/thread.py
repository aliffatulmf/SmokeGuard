"""
Meta Thread

This module contains the ThreadManager class for handling the lifecycle of a worker object's thread.
"""

from PySide6.QtCore import QThread


class ThreadManager:
    """
    ThreadManager handles the lifecycle of a worker object's thread.

    This class is responsible for starting, monitoring, and stopping a QThread
    for a given worker object. It ensures that the worker is executed in a
    separate thread and provides methods to safely start and stop the thread.

    Attributes:
        worker: The worker object that will be run in a separate thread.
        thread (QThread): The QThread object that the worker will run in.
        running (bool): A flag indicating whether the thread is currently running.

    Example:
        >>> from PySide6.QtCore import QObject, QThread, Signal
        >>>
        >>> class Worker(QObject):
        >>>     finished = Signal()
        >>>
        >>>     def run(self):
        >>>         print("Worker is running")
        >>>         self.finished.emit()
        >>>
        >>> worker = Worker()
        >>> manager = ThreadManager(worker)
        >>> manager.start()
        >>> # Assuming the worker finishes or is stopped elsewhere
        >>> manager.stop()
    """

    def __init__(self, worker):
        assert worker is not None, "Worker cannot be None"
        assert hasattr(worker, "run"), "Worker must have a run method"
        assert callable(getattr(worker, "run")), "Worker's run method must be callable"

        self.worker = worker
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.running = False

    def start(self):
        """
        Starts the worker in its separate thread if not already running.

        Raises:
            RuntimeError: If the thread is already running.
        """
        if not self.running:
            self.thread.start()
            self.running = True
        else:
            raise RuntimeError("Thread is already running")

    def stop(self):
        """
        Safely stops the worker's thread if it is running.

        This method ensures the thread is properly terminated and the resources
        are released.

        Raises:
            RuntimeError: If the thread is not currently running or if stopping the worker's loop fails.

        Example:
            >>> worker = Worker()
            >>> thread_manager = ThreadManager(worker)
            >>> # perform some operations
            >>> worker.start()
            >>> # perform some more operations
            >>> try:
            >>>     worker.stop()
            >>> except:
            >>>     # handle exceptions
            >>>     pass
        """
        if self.running:
            if not self.worker.stop_loop():
                raise RuntimeError("Failed to stop worker's loop")

            self.thread.quit()
            if self.thread.wait(3000):
                return

            if self.thread.isRunning():
                self.thread.terminate()

            self.running = False
        else:
            raise RuntimeError("Thread is not running")

    @property
    def is_running(self):
        return self.running
