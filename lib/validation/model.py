import os

SUPPORTED_FORMATS = [
    [".pt", "PyTorch"],
]


def validation_model_file(path: str):
    _, ext = os.path.splitext(path)
    for format in SUPPORTED_FORMATS:
        if ext == format[0]:
            return True
    return False
