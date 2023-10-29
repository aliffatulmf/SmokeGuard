import platform as pf
import struct
import sys

import cv2
from PySide6.QtWidgets import QApplication

from gui.window import Window
from lib.log import log_error


def is_win10_64bit_os() -> bool:
    return (
        pf.system() == "Windows"
        and pf.release() == "10"
        and struct.calcsize("P") * 8 == 64
    )


def run_gui():
    # Disable Log
    cv2.setLogLevel(0)

    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        cap.release()
    else:
        log_error(
            "[red]Failed to open camera. Please check your camera and try again.[/red]"
        )

    try:
        if sys.version_info < (3, 9):
            print("This program requires Python 3.9 or later.")
            exit(1)

        if not is_win10_64bit_os():
            print("This program is only compatible with Windows 10 64bit.")
            exit(1)

        app = QApplication(sys.argv)
        window = Window()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"An error occurred: {e}")
        exit(1)
