import cv2
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap


class FrameMeta:
    def __init__(self, frame):
        self.__frame = frame
        self.height, self.width, self.channel = self.__frame.shape
        self.depth = self.__frame.dtype.itemsize * 8

    def convert(self, color=cv2.COLOR_BGR2RGB):
        self.__frame = cv2.cvtColor(self.__frame, color)

    def frame(self):
        return self.__frame

    def image(self):
        return QImage(
            self.__frame.data,
            self.width,
            self.height,
            self.__frame.strides[0],
            QImage.Format.Format_RGB888
        )

    def pixmap(self):
        return QPixmap.fromImage(self.image(), Qt.ImageConversionFlag.AutoColor)


class Wrapper:
    def __init__(self, meta: FrameMeta):
        self.__meta = meta
        
    def meta(self):
        return self.__meta        
    
    def set(self, key, value):
        if not hasattr(self, key):
            setattr(self, key, value)
        else:
            raise AttributeError(f"Attribute {key} already exists")
    
    def set_kwargs(self, **kwargs):
        for key, value in kwargs.items():
            self.set(key, value)
        