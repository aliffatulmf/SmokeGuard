import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QCloseEvent, QIcon, QKeySequence
from PySide6.QtWidgets import QMainWindow, QMenuBar

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
        self.mainCameraThread = CameraThread(**self.kwargs)
        self.snapshotWindow = SnapshotWindow()
        cameraLayout = self.loadCameraLayout(self.snapshotWindow)
        self.parameterLayout = self.load_parameter_layout(cameraLayout)

    def setup_menubar(self) -> None:
        menuLayout: QMenuBar = QMenuBar(self)
        menuLayout.setFixedWidth(300)

        fileMenu = menuLayout.addMenu("File")
        fileMenu.addAction("Quit", self.exit_application, QKeySequence("Ctrl+Q"))

        viewMenu = menuLayout.addMenu("View")
        viewMenu.addAction("Snapshots", self.snapshotWindow.show)

        helpMenu = menuLayout.addMenu("Help")
        helpMenu.addAction("About", about_notification_box)

    def exit_application(self) -> None:
        self.safe_stop_camera()
        self.close()

    def loadCameraLayout(self, snapshot_window: SnapshotWindow) -> CameraLayout:
        cameraLayout = CameraLayout(
            self,
            self.mainCameraThread,
            **self.kwargs,
        )

        if not self.mainCameraThread.isRunning():
            cameraLayout.init()
            proxy.better_proxy(
                self.mainCameraThread.ImageTypeSignal, snapshot_window.slot_image
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

    def safe_stop_camera(self) -> None:
        if self.mainCameraThread.isRunning():
            self.mainCameraThread.stopThread()

    def closeEvent(self, event: QCloseEvent):
        # confirm_before_exit = QMessageBox.question(
        #     self,
        #     "Confirm Close",
        #     "Are you sure you want to exit SmokeGuard?",
        #     QMessageBox.Yes | QMessageBox.No,
        # )

        # if confirm_before_exit == QMessageBox.Yes:
        if hasattr(self, "snapshotWindow") and self.snapshotWindow.isVisible():
            self.snapshotWindow.close()

        self.exit_application()
        super().closeEvent(event)
