import logging
import os

import cv2


def check_compatibility():
    import sys

    required_version = (3, 8, 0)
    current_version = sys.version_info

    if current_version < required_version:
        raise Exception(
            f"This script requires Python {'.'.join(map(str, required_version))} or higher. Current version is {'.'.join(map(str, current_version[:3]))}.")
    logging.info("Python version is compatible.")


def is_source_available(source):
    if source is None:
        raise ValueError("Source is not specified")
    
    if isinstance(source, str):
        if source.isdigit():
            source = int(source)
        elif not os.path.isfile(source):
            raise ValueError(f"Invalid source: {source}")

    elif not isinstance(source, int) or source < 0:
        raise ValueError(f"Invalid source: {source}")

    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        raise ValueError(f"Unable to open source: {source}")
    cap.release()
