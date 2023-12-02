import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent, QIcon
from PySide6.QtWidgets import QMainWindow, QMenuBar, QMessageBox

from gui.layout.camera import CameraLayout
from gui.layout.parameter import ConfigLayout
from gui.snapshot import SnapshotWindow
from gui.vars import APP_NAME, about_notification_box
from libs.logger import console
from threads.camera import CameraThread


def eod_notification_box():
    return QMessageBox.information(
        None,
        "Thread",
        "End Of Detection",
        QMessageBox.Ok,
    )


class Window(QMainWindow):
    def __init__(self, **kwargs) -> None:
        super().__init__()

        ConfigLayout(self).show()

        self.kwargs = kwargs

        self.camera_thread = CameraThread(**self.kwargs)

        self.setup_functions()
        self.setup_ui()
        self.setup_menubar()

        if hasattr(self, "camera_thread"):

            def eod_handler(x: bool):
                if x:
                    eod_notification_box()
                    self.close()

            self.camera_thread.EOD.connect(lambda x: eod_handler(x))
            self.camera_thread.ImageSignal.connect(self.camera_layout.slot_image)
            self.camera_thread.SnapshotSignal.connect(self.snapshot_window.slot_image)
            self.camera_thread.start()
        else:
            console.fatal("Camera thread not found.")

    def setup_ui(self) -> None:
        self.setFixedSize(1200, 690)
        self.set_application_icon("assets/icon/icon.png")
        self.setWindowTitle(APP_NAME)
        self.set_application_background(Qt.GlobalColor.white)

    def setup_functions(self):
        self.snapshot_window = SnapshotWindow()
        self.camera_layout = CameraLayout(self, self.camera_thread, **self.kwargs)

    def setup_menubar(self) -> None:
        menu_layout: QMenuBar = QMenuBar(self)
        menu_layout.setMinimumWidth(1360)
        menu_layout.addAction("Snapshots", self.snapshot_window.show)
        menu_layout.addAction("About", about_notification_box)

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
        if (
            self.confirm_close_popup() == QMessageBox.Yes
            and self.snapshot_window.close()
            and self.camera_thread.stop_thread()
        ):
            event.accept()
        else:
            event.ignore()
