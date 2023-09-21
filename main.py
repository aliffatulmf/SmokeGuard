import sys
import platform as pf
import struct
import cv2

from PySide6.QtWidgets import QApplication
from gui.window import Window

def is_windows_64bit():
    return (
        pf.system() == "Windows" and
        pf.release() == "10" and
        struct.calcsize("P") * 8 == 64
    )

def run_application():
    if sys.version_info < (3, 9):
        print("This program requires Python 3.9 or later.")
        exit(1)

    if not is_windows_64bit():
        print("This program is only compatible with Windows 64 bit.")
        exit(1)

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        cap.release()
    else:
        print("No camera detected")
        exit(1)
    
    run_application()
