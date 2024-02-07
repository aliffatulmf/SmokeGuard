"""
Meta Frame

This module contains utility functions for working with image frames.
"""
import cv2
import numpy as np
from PySide6.QtGui import QImage, QPixmap


def resize_target(frame, target_size=(720, 1280)):
    """
    Resizes the input frame to a target size while maintaining the aspect ratio.

    Parameters:
        frame (numpy.ndarray): The frame to be resized.
        target_size (tuple): The target size for resizing. It should contain two integers representing the width and height respectively. Default is (720, 1280).

    Returns:
        numpy.ndarray: The resized frame.

    Example:
        >>> import cv2
        >>> frame = cv2.imread('path/to/image.jpg')
        >>> resized_frame = resize_target(frame, (500, 300))
    """
    assert isinstance(frame, np.ndarray), "Frame must be a numpy array."
    assert isinstance(target_size, tuple) and len(target_size) == 2 and all(isinstance(i, int) for i in target_size), "Target size must be a tuple containing two integers."

    # Get the aspect ratio from the target size
    aspect_ratio = target_size[1] / target_size[0]

    # Calculate new dimensions based on aspect ratio
    new_width = int(target_size[0] * aspect_ratio)
    new_height = target_size[0]

    # Resize the frame
    resized_frame = cv2.resize(frame, (new_width, new_height))

    return resized_frame


def resize_scale(image, scale):
    """
    Resizes the input image by a given scale while maintaining the aspect ratio.

    Parameters:
        image: The image to be resized, as a numpy array.
        scale: The scale factor for resizing, as a float.

    Returns:
        Resized image as a numpy array.

    Raises:
        ValueError: If the scale is such that it would change the aspect ratio of the image.

    Example:
        >>> import cv2
        >>> image = cv2.imread('path/to/image.jpg')
        >>> resized_image = resize_scale(image, 0.5)
    """
    assert isinstance(image, np.ndarray), "Image must be a numpy array."
    assert isinstance(scale, (int, float)), "Scale must be an int or a float."
    assert len(image.shape) >= 3, "Image must be at least 3-dimensional."
    assert 0 < scale <= 1, "Scale must be a positive number less than or equal to 1."

    # Get the original dimensions of the image
    h, w = image.shape[:2]

    # Calculate the new size based on scale
    new_w = int(w * scale)
    new_h = int(h * scale)

    # Ensure the scale does not change the aspect ratio
    if new_w / new_h != w / h:
        raise ValueError("Scale is not valid, it will change the aspect ratio of the image.")

    try:
        resized_image = cv2.resize(image, (new_w, new_h))
    except cv2.error as e:
        raise RuntimeError("Error occurred while resizing the image: " + str(e))
    return resized_image


# WARNING: EXPERIMENTAL
# def validate_base(base):
#     if isinstance(base, int):
#         return True
#     elif isinstance(base, tuple) and len(base) == 2:
#         return True
#     else:
#         return False
#
#
# def correct_aspect_ratio(original, base):
#     if isinstance(base, int):
#         closest = round(base / original, 2)
#     elif isinstance(base, tuple):
#         closest = min(base, key=lambda x: abs(x - original))
#     return closest
#
#
# def resize_base(frame, base, autocorrect=True):
#     """
#     Resizes the input frame based on a given base size while maintaining the aspect ratio.
#
#     Parameters:
#         frame (numpy.ndarray): The frame to be resized.
#         base (int or tuple): The base size for resizing. If an integer is provided, it is used as the width and the height is adjusted based on the aspect ratio. If a tuple is provided, it should contain two integers representing the width and height respectively.
#         autocorrect (bool): If True, the function will automatically adjust the base size to maintain the aspect ratio if the provided base size would change it. If False, the function will raise a ValueError if the provided base size would change the aspect ratio. Default is True.
#
#     Returns:
#         numpy.ndarray: The resized frame.
#
#     Raises:
#         ValueError: If the aspect ratio of the frame does not match with the base or if the base is not valid.
#
#     Example:
#         >>> import cv2
#         >>> frame = cv2.imread('path/to/image.jpg')
#         >>> resized_frame = resize_base(frame, 500)
#         >>> resized_frame = resize_base(frame, (500, 300))
#     """
#     if not validate_base(base):
#         raise ValueError("Base must be an int or a tuple with 2 integer elements.")
#
#     if isinstance(base, int):
#         # Find the aspect ratio value that is close to base and base as width
#         # Then adjust height based on aspect ratio
#         original = int(frame.shape[1] / frame.shape[0])
#         adjusted = int(base / frame.shape[0])
#
#         if not np.isclose(original, adjusted) and not autocorrect:
#             raise ValueError("The aspect ratio of the frame does not match with the base.")
#         elif autocorrect:
#             base = correct_aspect_ratio(original, base)
#
#         resized_frame = cv2.resize(frame, (base, int(frame.shape[0] * adjusted)), interpolation=cv2.INTER_NEAREST)
#         return resized_frame
#     elif isinstance(base, tuple):
#         # Create a private function to validate the contents of the base whether it is in accordance with the aspect ratio or not
#         # If it passes, resize based on the value close to base
#         _, resized_frame = cv2.resize(frame, base, interpolation=cv2.INTER_NEAREST)
#         return resized_frame


def image_to_qimage(image):
    """
    Converts a frame (binary data) into a QImage object.

    Parameters:
        image: Bytes-like object or bytearray containing the frame data.

    Returns:
        QImage object representing the frame.

    Example:
        >>> frame_data = cv2.imread('path/to/image.jpg')
        >>> qimage = image_to_qimage(frame_data)
    """
    assert isinstance(image, (bytes, bytearray, np.ndarray)), "Frame must be a bytes-like object or a numpy array."
    assert isinstance(image, np.ndarray), "Frame must be a numpy array."

    if len(image.shape) == 3 and image.shape[2] == 4:  # Alpha channel
        img = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format.Format_RGBA8888)
    elif len(image.shape) == 3 and image.shape[2] == 3:  # No alpha channel
        img = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format.Format_RGB888)
    else:
        raise ValueError("Image must be in RGB or RGBA format.")

    return img.copy()


def image_to_qpixmap(image):
    """
    Converts a frame (binary data) into a QPixmap object.

    Parameters:
        image: Bytes-like object or bytearray containing the frame data.

    Returns:
        QPixmap object representing the frame.

    Example:
        >>> frame_data = cv2.imread('path/to/image.jpg')
        >>> qpixmap = image_to_qpixmap(frame_data)
    """
    img = image_to_qimage(image)
    return QPixmap.fromImage(img)


def qimage_to_qpixmap(qimage):
    """
    Converts a QImage object to a QPixmap object, which can then be used for GUI display.

    Parameters:
        qimage: QImage object to convert.

    Returns:
        QPixmap object representing the QImage.

    Example:
        >>> qimage = QImage('path/to/image.png')
        >>> qpixmap = qimage_to_qpixmap(qimage)
    """
    assert isinstance(qimage, QImage), "Input must be a QImage object."
    assert not qimage.isNull(), "Input QImage object is null."

    return QPixmap.fromImage(qimage)
