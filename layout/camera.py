from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGroupBox, QLabel


class Camera:
    def __init__(self, parent, x=350, y=40, width=963, height=540):
        group_box = QGroupBox(parent)
        group_box.setGeometry(x, y, width, height)
        group_box.setFixedSize(width, height)
        group_box.setStyleSheet("border: 3px solid #dee2e6; border-radius: 3px;")

        self._video = QLabel(group_box)
        self._video.setFixedSize(width, height)
        self._video.setAlignment(Qt.AlignmentFlag.AlignBottom)

    @Slot(QPixmap)
    def signal_receiver(self, pixmap):
        self._video.setPixmap(pixmap)
