from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGroupBox, QLabel


class VideoFeedDisplay:
  def __init__(self, parent, x=350, y=40, width=960, height=560):
      # GroupBox for Camera
      groupbox = QGroupBox(parent)
      groupbox.setTitle("Camera")
      groupbox.setGeometry(x, y, width, height)
      groupbox.setFixedSize(width, height)

      # Label for displaying video feed
      self._video = QLabel(groupbox)
      self._video.setFixedSize(width, height)
      self._video.setAlignment(Qt.AlignmentFlag.AlignBottom)

  @Slot(QPixmap)
  def signal_receiver(self, pixmap):
      self._video.setPixmap(pixmap)