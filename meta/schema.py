"""
Meta Schema

This is containing the schema of the metadata.
"""

SNAPSHOT_SCHEMA = {
    "confidence": 0.0,
    "threshold": {
        "confidence": 0.0,
        "iou": 0.0,
    },
    "inference": {
        "current": 0.0,
        "min": 0.0,
        "max": 0.0,
        "avg": 0.0,
    },
    "fps": {
        "current": 0.0,
        "min": 0.0,
        "max": 0.0,
        "avg": 0.0,
    },
    "image": {
        "ndarray": None,
        "qpixmap": None,
        "qimage": None,
    },
    "floating_point": None,
    "hardware": "",
}

PARAMETER_SCHEMA = {
    "frames": 0,
    "fps": {
        "current": 0.0,
        "min": 0.0,
        "max": 0.0,
        "avg": 0.0,
    },
    "inference": {
        "current": 0.0,
        "min": 0.0,
        "max": 0.0,
        "avg": 0.0,
    },
    "total_object": 0,
}

