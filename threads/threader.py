import logging

import cv2
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage, QPixmap


class General(QThread):
    stop_detection_requested = False

    def __init__(self):
        super().__init__()

    def stop_thread(self):
        self.stop_detection_requested = True

        logging.info("Stopping thread...")
        self.quit()
        self.wait(3000)


class CameraSignal:
    camera_signal = Signal(QPixmap)
    snapshot_signal = Signal(dict)
    parameter_signal = Signal(dict)
    EOD = Signal(bool)

    def pixmap(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        qimg = QImage(
            frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        return QPixmap.fromImage(qimg)

    def camera_signal_emit(self, frame):
        pixmap = self.pixmap(frame)
        self.camera_signal.emit(pixmap)

    def snapshot_signal_emit(self, data):
        data["pixmap"] = self.pixmap(data["frame"])
        self.snapshot_signal.emit(data)
