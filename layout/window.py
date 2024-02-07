"""
Main Window
"""

import logging

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent, QFont, QIcon
from PySide6.QtWidgets import QMainWindow, QMenuBar, QMessageBox

from layout.camera import Camera
from layout.parameter import Parameter
from layout.snapshot import SnapshotWindow
from meta.thread import ThreadManager
from threads.inference import Inference


class Window(QMainWindow):
    """
    The main window of the application.
    """

    def __init__(self, **kwargs):
        """
        Constructor for initializing the application with the given parameters.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        super().__init__()

        font = QFont()
        font.setPointSize(11)
        self.setFont(font)
        self.setMinimumWidth(1366)
        self.setMinimumHeight(768)
        self.set_app_icon("assets/icon/icon.png")
        self.setWindowTitle("Aplikasi Pendeteksi Rokok")
        self.set_app_background(Qt.GlobalColor.white)

        self._parameter = Parameter(self)
        self._inference = Inference(kwargs["models"], kwargs["source"])
        self._camera = Camera(self, y=55)
        self._snapshot = SnapshotWindow(kwargs["maxlim"])
        
        self._inference.CAMERA_SIG.connect(self._camera.signal_receiver)
        self._inference.PARAMETER_SIG.connect(self._parameter.signal_receiver)
        self._inference.SNAPSHOT_SIG.connect(self._snapshot.signal_receiver)

        menu_bar = QMenuBar(self)
        menu_bar.setStyleSheet("border-width: 0;")
        menu_bar.setMinimumWidth(1360)
        menu_bar.setMinimumHeight(40)
        menu_bar.addAction("Snapshots", self._snapshot.showMaximized)

        self._thread_manager = ThreadManager(self._inference)
        self._thread_manager.start()

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
        
        if hasattr(self, "_thread_manager"):
            self._thread_manager.stop()

        print("Shutting down...")
        event.accept()
