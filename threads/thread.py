import logging

from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage

from classtype.metadata import ImageMetadata


class General(QThread):
    def __init__(self):
        super().__init__()
        self.stop_detection_requested = False

    def stop_thread(self):
        self.stop_detection_requested = True

        logging.info("Stopping thread...")
        self.wait(3000)


class CameraSignal:
    ImageSignal = Signal(QImage)
    SnapshotSignal = Signal(ImageMetadata)
    EndOfDetection = Signal(bool)

    def __init__(self):
        super(CameraSignal, self).__init__()

    def send(self, to: str, *args):
        try:
            signal = getattr(self, to)
        except AttributeError:
            raise ValueError(f"No signal named '{to}' exists in this class.")

        if isinstance(signal, Signal):
            signal.emit(*args)
        else:
            raise ValueError(f"Attribute '{to}' is not a Signal object.")
