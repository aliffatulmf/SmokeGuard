import sys

from PySide6.QtWidgets import QApplication

from gui.window import Window
from pkg.checker import check_compatibility


def run(**kwargs):
    check_compatibility()

    app = QApplication(sys.argv)
    window = Window(**kwargs)
    window.show()
    exit(app.exec())
