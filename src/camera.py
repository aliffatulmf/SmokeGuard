from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGroupBox, QLabel


class VideoFeedDisplay:
  def __init__(self, parent, x=350, y=40, width=963, height=540):
      groupbox = QGroupBox(parent)
      groupbox.setGeometry(x, y, width, height)
      groupbox.setFixedSize(width, height)
      groupbox.setStyleSheet("border: 3px solid #dee2e6; border-radius: 3px;")

      self._video = QLabel(groupbox)
      self._video.setFixedSize(width, height)
      self._video.setAlignment(Qt.AlignmentFlag.AlignBottom)

  @Slot(QPixmap)
  def signal_receiver(self, pixmap):
      self._video.setPixmap(pixmap)