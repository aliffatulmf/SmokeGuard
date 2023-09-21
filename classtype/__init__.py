from datetime import datetime

from PySide6.QtGui import QImage, QPixmap


class ImageType:
    """
    `ImageType` is a type hint for the `addImage()` method of the `SnapshotWindow` class. It represents a dictionary with the following keys:

    Attributes
    ----------
    `image`: QImage
        A QImage object representing the image to be displayed.
    `name`: str
        A string representing the name of the image.
    `confidence`: float
        A float representing the confidence level associated with the image.
    """

    def __init__(self, image: QImage = None, name: str = None, confidence: float = None, timestamp: str = None):
        self.image = image
        self.name = name
        self.confidence = confidence
        self.timestamp = timestamp

    def get(self, key: str):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise AttributeError("key not found")
