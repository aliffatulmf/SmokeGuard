import cv2
from PySide6.QtGui import QImage, QPixmap


def ResizeFrame(frame, scale=1):
    # Get the dimensions of the frame
    height, width = frame.shape[:2]

    # Calculate the new dimensions
    new_width = int(width * scale)
    new_height = int(height * scale)

    # Resize the frame
    resized_frame = cv2.resize(
        frame, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    return resized_frame


def FrameToPixmap(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    qimg = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qimg)
    return pixmap
