import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent, QIcon
from PySide6.QtWidgets import QMainWindow, QMenuBar, QMessageBox

from gui import proxy
from gui.layout.camera import CameraLayout
from gui.layout.parameter import ParameterLayout
from gui.snapshot import SnapshotWindow
from gui.vars import APP_NAME, about_notification_box
from threads.camera import CameraThread


class Window(QMainWindow):
    def __init__(self, **kwargs) -> None:
        super().__init__()

        self.kwargs = kwargs
        self.setup_functions()
        self.setup_ui()
        self.setup_menubar()

    def setup_ui(self) -> None:
        self.setFixedSize(1360, 768)
        self.set_application_icon("assets/icon/icon.png")
        self.setWindowTitle(APP_NAME)
        self.set_application_background(Qt.GlobalColor.white)

    def setup_functions(self):
        self.camera_thread = CameraThread(**self.kwargs)
        self.snapshot_window = SnapshotWindow()
        camera_layout = self.load_camera_layout(self.snapshot_window)
        self.parameter_layout = self.load_parameter_layout(camera_layout)

    def setup_menubar(self) -> None:
        menu_layout: QMenuBar = QMenuBar(self)
        menu_layout.setMinimumWidth(1360)
        menu_layout.addAction("Snapshots", self.snapshot_window.show)
        menu_layout.addAction("About", about_notification_box)

    def load_camera_layout(self, snapshot_window: SnapshotWindow) -> CameraLayout:
        cameraLayout = CameraLayout(
            self,
            self.camera_thread,
            **self.kwargs,
        )

        if not self.camera_thread.isRunning():
            cameraLayout.init()
            proxy.better_proxy(
                self.camera_thread.ImageTypeSignal, snapshot_window.slot_image
            )
            cameraLayout.start()

    def load_parameter_layout(self, camera: CameraLayout) -> ParameterLayout:
        """
        Initializes the parameter layout.
        """
        parameter_layout: ParameterLayout = ParameterLayout(self)
        parameter_layout.show()
        return parameter_layout

    def set_application_icon(self, icon: str) -> None:
        """
        Sets the window icon if it exists. Throws a FileNotFoundError otherwise.
        """
        if os.path.exists(icon):
            self.setWindowIcon(QIcon(icon))
        else:
            raise FileNotFoundError("Icon not found.")

    def set_application_background(self, color: Qt.GlobalColor) -> None:
        """
        Sets the background color.
        """
        palette = self.palette()
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)

    def exit_application(self) -> None:
        if getattr(self, "snapshot_window", None) and self.snapshot_window.isVisible():
            self.safe_stop_camera()
            self.snapshot_window.close()

    def safe_stop_camera(self) -> None:
        if self.camera_thread.isRunning():
            self.camera_thread.stop_thread()

    def confirm_close_popup(self):
        return QMessageBox.question(
            self,
            "Confirm Close",
            "Are you sure you want to exit SmokeGuard?",
            QMessageBox.Yes | QMessageBox.No,
        )

    def closeEvent(self, event: QCloseEvent):
        if self.confirm_close_popup() == QMessageBox.Yes:
            if self.camera_thread.isRunning():
                self.camera_thread.stop_thread()

            if self.snapshot_window.close():
                event.accept()
        else:
            event.ignore()
