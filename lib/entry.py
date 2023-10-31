import argparse
import os
import platform as pf
import struct
import sys

import cv2
from PySide6.QtWidgets import QApplication

from gui.window import Window
from lib.cache import remove_cache
from lib.connection.internet import INet
from lib.dependency import install_requirements
from lib.logger import console


def is_win10_64bit_os() -> bool:
    return (
        pf.system() == "Windows"
        and pf.release() == "10"
        and struct.calcsize("P") * 8 == 64
    )


def preprocess(args: argparse.Namespace):
    if not os.path.exists(args.model):
        console.fatal(f"Model file {args.model} not found")

    if os.path.splitext(args.model)[1] != ".pt":
        console.fatal(f"Only PyTorch model files are supported")

    if args.clean:
        remove_cache(args.exclude if args.exclude else [])
        return False

    inet = INet()

    if args.install_required or args.install:
        if not inet.is_online():
            console.fatal("You are not connected to the internet.")
        install_requirements(
            reinstall=getattr(args, "reinstall", False),
            names=args.install if args.install else None,
        )
        return False
    return True


def run(**kwargs):
    cv2.setLogLevel(0)

    if not cv2.VideoCapture(0).isOpened():
        console.fatal("Failed to open camera. Please check your camera and try again.")

    if sys.version_info < (3, 9):
        console.fatal("This program requires Python 3.9 or later.")

    if not is_win10_64bit_os():
        console.fatal("This program is only compatible with Windows 10 64bit.")

    try:
        app = QApplication(sys.argv)
        window = Window(**kwargs)
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        console.fatal(f"Error occurred while running the program: {e}")
