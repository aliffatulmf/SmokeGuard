from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QFrame, QGroupBox, QLabel, QVBoxLayout, QWidget

from threads.camera import CameraThread


class InactiveThreadError(Exception):
    def __init__(self, message):
        super().__init__("Thread error:", message)


ThreadInactiveError = InactiveThreadError("Thread is not running")


class CameraLayout(QWidget):
    X = 260
    Y = 45
    WIDTH = 650
    HEIGHT = 580

    def __init__(self, parent: QWidget, camera_thread: CameraThread, **kwargs):
        super().__init__(parent)
        self.kwargs = kwargs
        self.parent: QWidget = parent
        self.camera_thread = camera_thread

        self.frame = self.create_frame()
        self.groupbox = self.create_groupbox()
        self.vbox = self.create_vbox()
        self.video = self.create_video()

        self.frame.setParent(self.parent)
        self.groupbox.setParent(self.frame)
        self.vbox.setParent(self.groupbox)

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

    def show(self):
        if not self.camera_thread:
            raise InactiveThreadError("Thread is not running")

        self.video.setParent(self.groupbox)

    @Slot(QImage)
    def slot_image(self, image: QImage):
        pixmap = QPixmap.fromImage(image)
        scaled = pixmap.scaled(
            self.WIDTH - 40,
            self.HEIGHT - 60,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.video.setPixmap(scaled)
