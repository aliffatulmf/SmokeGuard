"""
Main Window
"""

import logging

from PySide6.QtCore import Qt, Slot
from PySide6.QtGui import QCloseEvent, QFont, QIcon
from PySide6.QtWidgets import (QGroupBox, QLabel, QMainWindow, QMenuBar,
                               QMessageBox)

from layout.parameter import Parameter
from layout.snapshot import SnapshotWindow
from meta.thread import ThreadManager
from threads.inference import Inference


class Window(QMainWindow):
    def __init__(self, **kwargs):
        super().__init__()

        font = QFont()
        font.setPointSize(11)
        self.setFont(font)
        self.setMinimumWidth(1366)
        self.setMinimumHeight(768)
        self.setWindowTitle("Aplikasi Pendeteksi Rokok")
        self.set_app_icon("assets/icon/icon.png")
        self.set_app_background(Qt.GlobalColor.white)
        self.camera_layout()

        mb = self.menu_bar()

        self.parameter = Parameter(self)
        self.inference = Inference(kwargs["weights"], kwargs["source"])
        self.snapshot = SnapshotWindow(kwargs["maxlim"])
        mb.addAction("Snapshots", self.snapshot.showMaximized)

        self.inference.CAMERA_SIG.connect(self.camera_signal_receiver)
        self.inference.PARAMETER_SIG.connect(self.parameter.signal_receiver)
        self.inference.SNAPSHOT_SIG.connect(self.snapshot.signal_receiver)

        self.thread_manager = ThreadManager(self.inference)
        self.thread_manager.start()

    def menu_bar(self):
        menu_bar = QMenuBar(self)
        menu_bar.setStyleSheet("border-width: 0;")
        menu_bar.setMinimumWidth(1360)
        menu_bar.setMinimumHeight(40)
        return menu_bar

    def camera_layout(self):
        x, y, width, height = 350, 55, 963, 540
        camera_box = QGroupBox(self)
        camera_box.setGeometry(x, y, width, height)
        camera_box.setFixedSize(width, height)
        camera_box.setStyleSheet("border: 3px solid #dee2e6; border-radius: 3px;")

        self.video = QLabel(camera_box)
        self.video.setFixedSize(width, height)
        self.video.setAlignment(Qt.AlignmentFlag.AlignBottom)

    @Slot()
    def camera_signal_receiver(self, pixmap):
        self.video.setPixmap(pixmap)

    def set_app_icon(self, icon):
        app_icon = QIcon(icon)
        self.setWindowIcon(app_icon)

    def set_app_background(self, c):
        p = self.palette()
        p.setColor(self.backgroundRole(), c)
        self.setPalette(p)

    def closeEvent(self, event: QCloseEvent):
        msg_box = QMessageBox()
        msg_box.setWindowIcon(QIcon("assets/icon/icon.png"))
        msg_box.setWindowTitle("Exit Confirmation")
        msg_box.setIcon(QMessageBox.Icon.Question)
        msg_box.setText("Are you sure you want to exit?\nAny unsaved changes will be lost.")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)

        if msg_box.exec() == QMessageBox.StandardButton.No:
            logging.info("Shutdown aborted")
            event.ignore()
            return

        if hasattr(self, "thread_manager"):
            self.thread_manager.stop()

        print("Shutting down...")
        event.accept()


def main_window_exec(params):
    from PySide6.QtWidgets import QApplication

    app = QApplication([])
    window = Window(**params)
    window.show()
    app.exec()