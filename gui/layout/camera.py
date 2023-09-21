from PySide6.QtCore import Qt, Slot
from PySide6.QtWidgets import QGroupBox, QLabel, QVBoxLayout, QFrame, QMainWindow, QWidget
from PySide6.QtGui import QPixmap, QImage

from threads.camera import CameraThread


class InactiveThreadError(Exception):
    def __init__(self, message):
        super().__init__("Thread error:", message)

ThreadInactiveError = InactiveThreadError("Thread is not running")

class CameraLayout(QWidget):
    X = 250
    Y = 40
    WIDTH = 640
    HEIGHT = 640

    def __init__(self, parent: QMainWindow = None):
        super().__init__()
        self.parent = parent
        self.ct = None

        self.frame = QFrame()
        self.frame.setGeometry(self.X, self.Y, self.WIDTH, self.HEIGHT)

        self.groupbox = QGroupBox()
        self.groupbox.setTitle("Camera")
        self.groupbox.setFixedSize(self.WIDTH, self.HEIGHT)

        self.vbox = QVBoxLayout(self.groupbox)
        self.vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.video = QLabel(self.groupbox)
        self.video.setText("No Camera Detected")
        self.video.setFixedSize(self.WIDTH, self.HEIGHT)
        self.video.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.frame.setParent(self.parent)
        self.groupbox.setParent(self.frame)
        self.vbox.setParent(self.groupbox)

    def show(self):
        if not self.ct:
            raise InactiveThreadError("Thread is not running")

        self.video.setParent(self.groupbox)

    def init(self):
        self.ct = CameraThread(self.groupbox)
        self.ct.ImageSignal.connect(self.frame_signal)

    def start(self):
        self.ct.finished.connect(self.ct.deleteLater)
        self.ct.start()

    def restart(self):
        if self.is_running():
            self.safe_stop()
        self.start()
        
    def stop_without_exit(self):
        if not self.is_running():
            raise ThreadInactiveError
        else:
            self.ct.stopThread(False, False)

    def safe_stop(self):
        if not self.is_running():
            raise ThreadInactiveError
        else:
            self.ct.stopThread()

    def unsafe_stop(self):
        if not self.is_running():
            raise ThreadInactiveError
        else:
            self.ct.stopThread(False)

    def is_running(self):
        if self.ct:
            return self.ct.isRunning()
        return False

    def signal(self):
        if not self.ct:
            raise ThreadInactiveError
        return self.ct.ImageTypeSignal

    @Slot(QImage)
    def frame_signal(self, image: QImage):
        pixmap = QPixmap.fromImage(image)

        self.video.setPixmap(pixmap)
