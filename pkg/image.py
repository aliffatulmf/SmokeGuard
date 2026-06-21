import cv2
from PySide6.QtGui import QImage


class ImageFrame:
    def __init__(self, frame, color = cv2.COLOR_BGR2RGB):
        self.frame = cv2.cvtColor(frame, color)
        self.height, self.width, self.channel = self.frame.shape
        self.bytes_per_line = 3 * self.width

def FQImage(imframe: ImageFrame):
    data = imframe.frame.copy()
    return QImage(
        data.data,
        imframe.width,
        imframe.height,
        imframe.bytes_per_line,
        QImage.Format.Format_RGB888,
    )
