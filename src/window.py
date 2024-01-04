import logging
import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QCloseEvent, QIcon, QPalette, QPixmap
from PySide6.QtWidgets import QMainWindow, QMenuBar, QMessageBox

from src.camera import VideoFeedDisplay
from src.parameter import ParametersLayout
from src.snapshot import SnapshotWindow
from threads.inference import Inference


class Window(QMainWindow):
    def __init__(self, **kwargs):
      super().__init__()
      self.verbose = kwargs["verbose"]
      self.setMinimumWidth(1400)
      self.setMinimumHeight(690)
      self.set_application_icon("assets/icon/icon.png")
      self.setWindowTitle("Aplikasi Pendeteksi Rokok")
      self.set_application_background(Qt.GlobalColor.white)
      self.parameter_frame = ParametersLayout(self, **kwargs)
      self.snapshot = SnapshotWindow()
      self.inference = Inference(**kwargs)
      self.video_feed_display = VideoFeedDisplay(self)
      menu_layout = QMenuBar(self)
      menu_layout.setMinimumWidth(1360)
      menu_layout.addAction("Snapshots", self.snapshot.showMaximized)
      self.inference.emitter.connect_camera_signal(self.video_feed_display.signal_receiver)
      self.inference.emitter.connect_snapshot_signal(self.snapshot.signal_receiver)
      self.inference.emitter.connect_parameter_signal(self.parameter_frame.signal_receiver)
      self.inference.start()
    
    def set_application_icon(self, icon):
        if not isinstance(icon, str):
            raise TypeError("Icon path must be a string.")
        if not icon:
            raise ValueError("Icon path must not be empty.")
        
        if os.path.exists(icon):
            app_icon = QIcon(icon)
            self.setWindowIcon(app_icon)
        else:
            raise FileNotFoundError(f"Icon not found at path: {icon}")

    def set_application_background(self, c):
       if isinstance(c, str):
           if os.path.exists(c):
               self.setAutoFillBackground(True)
               p = self.palette()
               p.setBrush(QPalette.Background, QBrush(QPixmap(c)))
               self.setPalette(p)
           else:
               self.setStyleSheet(f"background-color: {c};")
       elif isinstance(c, QPalette):
           self.setPalette(c)
       elif isinstance(c, Qt.GlobalColor):
           p = self.palette()
           p.setColor(self.backgroundRole(), c)
           self.setPalette(p)
       else:
           raise TypeError("Background must be a string (color or file path), a QPalette, or a Qt.GlobalColor.")

    def confirm_exit(self):
        reply = QMessageBox()
        reply.setWindowIcon(QIcon("assets/icon/icon.png"))
        reply.setWindowTitle("Exit Confirmation")
        reply.setIcon(QMessageBox.Question)
        reply.setText("Are you sure you want to exit?\nAny unsaved changes will be lost.")
        reply.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply.setDefaultButton(QMessageBox.No)
        return reply.exec() == QMessageBox.Yes

    def stop_snapshot(self):
        if self.snapshot.isVisible():
            if self.verbose: logging.info("Snapshot is visible. Closing snapshot.")
            self.snapshot.close()

    def stop_inference(self):
        if self.inference.isRunning():
            if self.verbose: logging.info("Inference is running. Stopping inference thread.")
            self.inference.stop_thread()

    def closeEvent(self, event: QCloseEvent):
        if self.confirm_exit():
            self.stop_snapshot()
            self.stop_inference()
            logging.info("Exit confirmed. Accepting event.")
            event.accept()
        else:
            logging.info("Exit canceled. Ignoring event.")
            event.ignore()