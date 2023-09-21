# this file is used for saving image into local disk

import numpy as np
import cv2

def save_image(image: np.ndarray):
    """save image to disk"""
    filename = f"image_{int(time.timestamp())}.jpg"
    cv2.imwrite(filename, image)
    