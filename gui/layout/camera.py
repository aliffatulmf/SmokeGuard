from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QFrame, QGroupBox, QLabel, QVBoxLayout, QWidget

from lib.log import *
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

    def __init__(self, parent: QWidget, camera_thread: CameraThread, **kwargs):
        super().__init__(parent)
        self.kwargs = kwargs
        self.console = Logger()
        self.parent: QWidget = parent
        self.ct = camera_thread

        self.setup_ui()

    def setup_ui(self):
        self.frame = self.create_frame()
        self.groupbox = self.create_groupbox()
        self.vbox = self.create_vbox()
        self.video = self.create_video()

        self.arrange_ui()

    def create_frame(self):
        frame = QFrame(self)
        frame.setGeometry(self.X, self.Y, self.WIDTH, self.HEIGHT)
        return frame

    def create_groupbox(self):
        groupbox = QGroupBox(self.frame)
        groupbox.setTitle("Camera")
        groupbox.setFixedSize(self.WIDTH, self.HEIGHT)
        return groupbox

    def create_vbox(self):
        vbox = QVBoxLayout(self.groupbox)
        vbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return vbox

    def create_video(self):
        video = QLabel(self.groupbox)
        video.setText("No Camera Detected")
        video.setFixedSize(self.WIDTH, self.HEIGHT)
        video.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return video

    def arrange_ui(self):
        self.frame.setParent(self.parent)
        self.groupbox.setParent(self.frame)
        self.vbox.setParent(self.groupbox)

    def show(self):
        if not self.ct:
            raise InactiveThreadError("Thread is not running")

        self.video.setParent(self.groupbox)

    def getGroupBox(self) -> QGroupBox:
        return self.groupbox

    def init(self):
        self.ct.ImageSignal.connect(self.frame_signal)

    @Slot(QImage)
    def frame_signal(self, image: QImage):
        pixmap = QPixmap.fromImage(image)
        self.video.setPixmap(pixmap)

    def is_running(self):
        if self.ct:
            return self.ct.isRunning()
        return False

    def restart(self):
        if self.is_running():
            self.safe_stop()
        else:
            self.start()

    def signal(self):
        if not self.ct:
            raise ThreadInactiveError
        return self.ct.ImageTypeSignal

    def start(self):
        if self.ct:
            self.ct.finished.connect(self.ct.deleteLater)
            self.ct.start()

    def safe_stop(self):
        if not self.is_running():
            raise ThreadInactiveError
        else:
            if self.ct != None:
                self.ct.stopThread()
