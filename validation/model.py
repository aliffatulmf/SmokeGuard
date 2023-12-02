import os

SUPPORTED_FORMATS = [
    [".pt", "PyTorch"],
]


def validate_file_extension(file_path, SUPPORTED_FORMATS=SUPPORTED_FORMATS):
    """
    Validates if the file's extension is in the supported formats.

    Args:
        file_path (str): The path to the file.
        SUPPORTED_FORMATS (list): A list of supported file extensions.

    Raises:
        ValueError: If the file's extension is not in the supported formats.
    """
    _, file_extension = os.path.splitext(file_path)
    if file_extension not in SUPPORTED_FORMATS:
        raise ValueError(
            f"Unsupported file extension. Supported formats are {SUPPORTED_FORMATS}"
        )
