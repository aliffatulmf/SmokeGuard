import logging
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent, QIcon
from PySide6.QtWidgets import QMainWindow, QMenuBar, QMessageBox

from gui.dialog import APP_NAME, show_about_dialog
from gui.layout.camera import CameraLayout
from gui.layout.parameter import SettingsLayout
from gui.snapshot import SnapshotWindow
from threads.camera import CameraThread


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

        # Window settings
        self.setFixedSize(1200, 690)
        self.set_application_icon("assets/icon/icon.png")
        self.setWindowTitle(APP_NAME)
        self.set_application_background(Qt.GlobalColor.white)

        # Layouts
        try:
            cfg_layout = SettingsLayout(self)
            cfg_layout.show()
        except Exception as e:
            logging.critical(f"Error from SettingsLayout: {e}")
            exit(1)
       
        # Camera 
        self.snapshot_window = SnapshotWindow()
        self.camera_thread = CameraThread(**kwargs)
        self.camera_layout = CameraLayout(self, self.camera_thread, **kwargs)
        self.camera_layout.show()

        # Menu bar
        menu_layout: QMenuBar = QMenuBar(self)
        menu_layout.setMinimumWidth(1360)
        menu_layout.addAction("Snapshots", self.snapshot_window.show)
        menu_layout.addAction("About", show_about_dialog)
       
        # Signals 
        self.camera_thread.EndOfDetection.connect(detect_end_notify)
        self.camera_thread.ImageSignal.connect(self.camera_layout.slot_image)
        self.camera_thread.SnapshotSignal.connect(self.snapshot_window.slot_image)
        self.camera_thread.start()

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
        if getattr(self, "snapshot_window", None) and self.snapshot_window.isVisible():
            self.safe_stop_camera()
            self.snapshot_window.close()

    def safe_stop_camera(self):
        if self.camera_thread.isRunning():
            self.camera_thread.stop_thread()

    def closeEvent(self, event: QCloseEvent):
        exit_confirm = QMessageBox()
        exit_confirm.setWindowIcon(QIcon("assets/icon/icon.png"))
        exit_confirm.setWindowTitle("Exit Confirmation")
        exit_confirm.setIcon(QMessageBox.Question)
        exit_confirm.setText("Are you sure you want to exit?\nAny unsaved changes will be lost.")
        exit_confirm.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        exit_confirm.setDefaultButton(QMessageBox.No)

        if exit_confirm.exec() == QMessageBox.Yes:
            if self.snapshot_window.isVisible():
                logging.info("Closing snapshot window...")
                self.snapshot_window.close()
            
            if self.camera_thread.isRunning():
                self.camera_thread.stop_thread()
            
            logging.info("Exiting application...")
            event.accept()
        else:
            event.ignore()
