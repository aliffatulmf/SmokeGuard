import os

from typing import Callable, List, Optional
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QCloseEvent, QIcon
from PySide6.QtWidgets import QMainWindow, QMenuBar, QMenu, QWidget

from gui import proxy
from gui.layout.camera import CameraLayout
from gui.layout.parameter import ParameterLayout
from gui.snapshot import SnapshotWindow


class Window(QMainWindow):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.init_ui()
        self.init_menu_bar()

    def init_ui(self) -> None:
        """
        Initializes the user interface.
        """
        self.setFixedSize(1360, 768)
        self.init_window_icon("assets/icon/icon.png")
        self.setWindowTitle("SmokeGuard: YOLO Smoking Activity Monitor")
        self.init_background(Qt.GlobalColor.white)

        self.snapshotWindow: SnapshotWindow = SnapshotWindow()
        self.mainCamera: CameraLayout = self.init_camera(self.snapshotWindow)
        self.parameterLayout: ParameterLayout = self.init_parameter_layout(
            self.mainCamera)

    def init_menu_bar(self) -> None:
        """
        Initializes the menu bar.
        """
        menubar: QMenuBar = QMenuBar(self)
        self.create_menu(menubar, "File", [
            self.create_action("Quit", "Ctrl+Q", self.stop_and_exit)
        ])
        self.create_menu(menubar, "View", [self.create_action(
            "Snapshots", trigger_method=self.show_snapshot_window)
        ])

    def stop_and_exit(self) -> None:
        """
        Stops and exits the application.
        """
        self.stop_camera()
        self.close()

    def show_snapshot_window(self) -> None:
        """
        Displays the snapshot window.
        """
        self.snapshotWindow.show()

    def create_action(self, title: str, shortcut: Optional[str] = None, trigger_method: Callable = None) -> QAction:
        """
        Creates an action with the specified title, shortcut, and trigger method.
        """
        action: QAction = QAction(title, self)
        if shortcut:
            action.setShortcut(shortcut)
        if trigger_method:
            action.triggered.connect(trigger_method)
        return action

    def create_menu(self, menubar: QMenuBar, title: str, actions: List[QAction]) -> QMenu:
        """
        Creates a menu on the menu bar with the specified title and actions.
        """
        menu: QMenu = menubar.addMenu(title)
        for action in actions:
            menu.addAction(action)
        return menu

    def init_camera(self, snapshot_window: SnapshotWindow) -> CameraLayout:
        """
        Initializes the camera.
        """
        camera: CameraLayout = CameraLayout(self)
        if not camera.is_running():
            camera.init()
            proxy.better_proxy(camera.signal(), snapshot_window.slot_image)
            camera.start()
        return camera

    def init_parameter_layout(self, camera: CameraLayout) -> ParameterLayout:
        """
        Initializes the parameter layout.
        """
        parameter_layout: ParameterLayout = ParameterLayout(self)
        parameter_layout.set_thread(camera)
        parameter_layout.show()
        camera.show()
        return parameter_layout

    def init_window_icon(self, icon: str) -> None:
        """
        Sets the window icon if it exists. Throws a FileNotFoundError otherwise.
        """
        if os.path.exists(icon):
            self.setWindowIcon(QIcon(icon))
        else:
            raise FileNotFoundError("Icon not found.")

    def init_background(self, color: Qt.GlobalColor) -> None:
        """
        Sets the background color.
        """
        palette = self.palette()
        palette.setColor(self.backgroundRole(), color)
        self.setPalette(palette)

    def stop_camera(self) -> None:
        """
        Safely stops the camera if it is running.
        """
        if hasattr(self, "mainCamera") and self.mainCamera.is_running():
            self.mainCamera.safe_stop()

    def closeEvent(self, event: QCloseEvent) -> None:
        self.close_windows_if_exist()
        super().closeEvent(event)

    def close_windows_if_exist(self) -> None:
        """
        Closes the snapshot window if it exists and stops the camera.
        """
        if hasattr(self, "snapshotWindow") and self.snapshotWindow.isVisible():
            self.snapshotWindow.close()
        self.stop_camera()
