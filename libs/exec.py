import platform as pf
import struct
import sys

import cv2
from PySide6.QtWidgets import QApplication

from gui.window import Window
from libs.logger import console
from libs.validation.environment import (
    Architecture,
    System,
    WindowsRelease,
    os_version,
    python_version,
)


def is_win10_64bit_os() -> bool:
    return (
        pf.system() == "Windows"
        and pf.release() == "10"
        and struct.calcsize("P") * 8 == 64
    )


def check_camera(source):
    if source.isdigit():
        console.info("Checking camera...")
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            console.fatal(
                "Failed to open camera. Please check your camera and try again."
            )
        cap.release()


def run(**kwargs):
    # check os version
    try:
        console.info("Checking OS version...")
        os_version(System.WINDOWS, WindowsRelease.WINDOWS_10, Architecture.X86_64)

        console.info("Checking Python version...")
        python_version(3, 9, 0)
    except Exception as e:
        console.fatal(e)

    # disable OpenCV logging
    cv2.setLogLevel(0)

    source = kwargs.get("source")
    source = check_camera(int(source)) if source.isdigit() else source

    try:
        app = QApplication(sys.argv)
        window = Window(**kwargs)
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        console.fatal(f"Error occurred while running the program: {e}")
