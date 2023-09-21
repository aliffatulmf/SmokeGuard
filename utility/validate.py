import sys


class CompatibilityError(Exception):
    pass


class CameraError(Exception):
    pass


def check_compatibility() -> bool:
    """
    Checks if the program is compatible with the current system.
    :return: True if the program is compatible, raises an error otherwise.
    """
    if sys.platform != "win32":
        raise CompatibilityError(
            "This program is only compatible with Windows 64 bit.")
    elif sys.version_info < (3, 9):
        raise CompatibilityError("This program requires Python 3.9 or later.")
    else:
        return True


def check_camera() -> bool:
    """
    Checks if the camera is detected.
    :return: True if the camera is detected, raises an error otherwise.
    """
    import cv2
    if cv2.VideoCapture(0).isOpened() is False:
        raise CameraError('Camera not detected.')
    else:
        return True
