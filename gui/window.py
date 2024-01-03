import logging
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent, QIcon
from PySide6.QtWidgets import QMainWindow, QMenuBar, QMessageBox

from gui.dialog import APP_NAME, show_about_dialog
from gui.layout.camera import VideoFeedDisplay
# from gui.layout.parameter import SettingsLayout
from gui.layout.parameter import ParametersLayout
from gui.snapshot import SnapshotWindow
from meta.io import ConfigIO
# from threads.camera import CameraThread
from threads.inference import Inference


def detect_end_notify(x):
    if x:
        QMessageBox.information(
            None,
            "Notification",
            "END OF DETECTION",
            QMessageBox.StandardButton.Ok,
        )

class Window(QMainWindow):
    def __init__(self, **kwargs):
        super().__init__()

        self.config_io = ConfigIO()

        # Window settings
        self.setMinimumWidth(1400)
        self.setMinimumHeight(690)
        self.set_application_icon("assets/icon/icon.png")
        self.setWindowTitle(APP_NAME)
        self.set_application_background(Qt.GlobalColor.white)

        # Layouts
        self.parameter_frame = ParametersLayout(self)

        # Camera
        self.snapshot = SnapshotWindow()
        self.inference = Inference(**kwargs)
        self.video_feed_display = VideoFeedDisplay(self)

        # Menu bar
        menu_layout: QMenuBar = QMenuBar(self)
        menu_layout.setMinimumWidth(1360)
        menu_layout.addAction("Snapshots", self.snapshot.showMaximized)
        menu_layout.addAction("About", show_about_dialog)

        # Signals
        self.inference.emitter.connect_camera_signal(self.video_feed_display.signal_receiver)
        self.inference.emitter.connect_snapshot_signal(self.snapshot.signal_receiver)
        self.inference.emitter.connect_parameter_signal(self.parameter_frame.signal_receiver)
        
        self.inference.start()

    def set_application_icon(self, icon):
        if os.path.exists(icon):
            self.setWindowIcon(QIcon(icon))
        else:
            raise FileNotFoundError("Icon not found.")

    def set_application_background(self, color: Qt.GlobalColor):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)

    def exit_application(self):
        if getattr(self, "snapshot", None) and self.snapshot.isVisible():
            self.safe_stop_camera()
            self.snapshot.close()

    def safe_stop_camera(self):
        if self.inference.isRunning():
            self.inference.stop()

    def closeEvent(self, event: QCloseEvent):
        exit_confirm = QMessageBox()
        exit_confirm.setWindowIcon(QIcon("assets/icon/icon.png"))
        exit_confirm.setWindowTitle("Exit Confirmation")
        exit_confirm.setIcon(QMessageBox.Question)
        exit_confirm.setText("Are you sure you want to exit?\nAny unsaved changes will be lost.")
        exit_confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        exit_confirm.setDefaultButton(QMessageBox.No)

        if exit_confirm.exec() == QMessageBox.Yes:
            if self.snapshot.isVisible():
                logging.info("Closing snapshot window...")
                self.snapshot.close()
            
            if self.inference.isRunning():
                self.inference.stop()
            
            logging.info("Exiting application...")
            event.accept()
        else:
            event.ignore()
