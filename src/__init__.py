from PySide6.QtWidgets import QApplication

from .window import Window


def CallMainWindow(**kwargs):
    app = QApplication([])
    window = Window(**kwargs)
    window.showMaximized()
    app.exec()