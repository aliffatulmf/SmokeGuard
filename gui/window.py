import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QCloseEvent, QIcon
from PySide6.QtWidgets import QMainWindow, QMenuBar

from gui import proxy
from gui.layout.camera import CameraLayout
from gui.layout.parameter import ParameterLayout
from gui.snapshot import SnapshotWindow


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1360, 768)
        self.init_ui()
        self.init_menu_bar()

        self.snapshotWindow = SnapshotWindow()

        self.mainCamera = CameraLayout(self)
        if not self.mainCamera.is_running():
            self.mainCamera.init()
            proxy.proxy(self.mainCamera.signal(), self.snapshotWindow.slot_image)
            self.mainCamera.start()
        
        self.parameterLayout = ParameterLayout(self)
        self.parameterLayout.set_thread(self.mainCamera)
        self.parameterLayout.show()
        self.mainCamera.show()

    def show_snapshot_window(self):
        self.snapshotWindow.show()

    def init_menu_bar(self):
        menubar = QMenuBar(self)

        def stop_and_exit():
            if hasattr(self, "mainCamera"):
                if self.mainCamera.is_running():
                    self.mainCamera.safe_stop()  # safely stop the camera thread
            self.close()

        # Quit action
        quit_action = QAction("Quit", self)
        quit_action.setShortcut("Ctrl+Q")
        quit_action.triggered.connect(stop_and_exit)

        snapshot_action = QAction("Snapshots", self)
        snapshot_action.triggered.connect(self.show_snapshot_window)

        # File Menu
        file_menu = menubar.addMenu("File")
        file_menu.addAction(quit_action)

        view_menu = menubar.addMenu("View")
        view_menu.addAction(snapshot_action)

    def init_ui(self):
        self.init_window_icon("assets/icon/icon.png")
        self.setWindowTitle("SmokeGuard: YOLO Smoking Activity Monitor")
        self.init_background(Qt.GlobalColor.white)

    def init_window_icon(self, icon: str):
        if os.path.exists(icon):
            self.setWindowIcon(QIcon(icon))
        else:
            raise FileNotFoundError("Icon not found.")

    def init_background(self, color: Qt.GlobalColor):
        palette = self.palette()
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)

    def closeEvent(self, event: QCloseEvent) -> None:
        if hasattr(self, "snapshotWindow") and self.snapshotWindow is not None:
            if self.snapshotWindow.isVisible():
                self.snapshotWindow.close()

        if hasattr(self, "mainCamera"):
            if self.mainCamera.is_running():
                self.mainCamera.safe_stop()

        super().closeEvent(event)
