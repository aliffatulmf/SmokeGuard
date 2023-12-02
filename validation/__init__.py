import platform
import struct
import sys

import cv2

from libs.logger import console


def check_camera(source: int):
    """
    Checks if the camera at the given source can be opened.

    This function tries to open the camera at the given source using OpenCV's VideoCapture.
    If the camera cannot be opened, the function raises a fatal error.

    Args:
        source (int): The source of the camera to check.

    Returns:
        int: The source of the camera if it can be opened.

    Raises:
        Exception: If the camera cannot be opened.
    """
    console.info("checking camera...")
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        console.fatal(
            f"Failed to open camera at source {source}. Please check your camera and try again."
        )
    else:
        ret, frame = cap.read()
        if not ret or frame is None:
            console.fatal(
                f"Camera at source {source} is not providing frames. Please check your camera and try again."
            )
    cap.release()
    return source


def check_python_version():
    """
    Checks if the current Python version is 3.9 or higher.
    Raises an exception if the Python version does not meet the requirements.
    """
    if sys.version_info < (3, 9):
        raise Exception("This program requires Python 3.9 or higher.")


def check_source(source):
    """
    Checks the source and returns the appropriate value.
    """
    if source.isdigit():
        cv2.setLogLevel(0)
        return check_camera(int(source))
    return source


def check_system_compat():
    """
    Checks if the operating system is Windows 10 and 64-bit.
    Raises an exception if the OS does not meet the requirements.
    """
    required_name = "Windows"
    required_version = "10"
    required_arch = 64

    current_name = platform.system()
    current_version = platform.release()
    current_arch = struct.calcsize("P") * 8

    if current_name != required_name:
        raise ValueError(
            f"Invalid OS name. Required: {required_name}, Current: {current_name}"
        )

    if current_version != required_version:
        raise ValueError(
            f"Invalid OS version. Required: {required_version}, Current: {current_version}"
        )

    if current_arch != required_arch:
        raise ValueError(
            f"Invalid architecture. Required: {required_arch}, Current: {current_arch}"
        )

    return True
