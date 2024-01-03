from PySide6.QtCore import QThread


class StoppableThread(QThread):
    def __init__(self):
        super().__init__()
        self._stop_requested = False

    def request_stop(self):
        self._stop_requested = True

    def force_stop(self):
        self.terminate()

    def stop(self):
        self.request_stop()
        for _ in range(3):
            if not self.isRunning():
                return
            QThread.msleep(100)
        self.force_stop()

    def restart(self):
        if self.isRunning():
            self.stop()
        self.start()
