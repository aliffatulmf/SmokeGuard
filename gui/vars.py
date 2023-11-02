import PySide6
import torch
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QMessageBox

APP_NAME = "SmokeGuard: YOLO Smoking Activity Monitor"
APP_VERSION = "v1.0.0"
APP_AUTHOR = "Alif Fatul"
APP_WEBSITE = "https://github.com/aliffatul/SmokeGuard"
APP_PYSIDE_VERSION = PySide6.__version__


def about_notification_box():
    text = f"""
        {APP_NAME}
        Version: {APP_VERSION}
        Author: {APP_AUTHOR}
        Website: {APP_WEBSITE}
        PySide version: {APP_PYSIDE_VERSION}
        CUDA support: {'Yes' if torch.cuda.is_available() else 'No'}
        """
    about = QMessageBox()
    about.setWindowIcon(QIcon("assets/icon/icon.png"))
    about.setWindowTitle("About")
    about.setText(text)
    about.exec()
