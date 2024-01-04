from PySide6.QtCore import QThread


class StopControl(QThread):
    def __init__(self):
        super().__init__()
        self.stop_requested = False

    def request_stop(self):
        self.stop_requested = True

    def terminate_thread(self):
        self.terminate()

    def stop_thread(self):
        self.request_stop()
        for _ in range(3):
            if not self.isRunning():
                return
            QThread.msleep(100)
        self.terminate_thread()

    def restart_thread(self):
        if self.isRunning():
            self.stop_thread()
        self.start()
