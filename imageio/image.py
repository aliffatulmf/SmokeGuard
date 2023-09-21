import json
import os

import cv2

class ImageInfo:
    name: str
    filename: str
    timestamp: int

    # parameter: dict{
    #     confidence: float,
    #     iou: float,
    #     hardware: string,
    #     agnostic_nms: boolean,
    #     augment: boolean,
    # }
    parameter: dict

    def __dict__(self):
        return {
            "name": self.name,
            "filename": self.filename,
            "timestamp": self.timestamp,
            "parameter": self.parameter
        }


class ImageIO:
    path = "images/images.json"

    def __init__(self, info: ImageInfo = None):
        self._info = info
        self._load: dict = self._read()

    def setPath(self, path: str):
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} not found")

        self.path = path

    def storeInfo(self, info: ImageInfo, overwrite: bool = True):
        """this will overwrite the existing info.use `overwire=False` to prevent overwriting"""

        if info is None:
            raise ValueError("info cannot be None")

        if not overwrite:
            if self._info is not None:
                raise ValueError("info already exists")

        self._info = info

    def _read(self) -> dict:
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as image_json:
                return json.load(image_json)
        else:
            raise FileNotFoundError(f"{self.path} not found")

    def read(self) -> dict:
        return self._load

    def write(self) -> None:
        if self._info is not None:
            self._load["images"].append(self._info.__dict__())

            with open(self.path, "w+", encoding="utf-8") as image_json:
                json.dump(self._load, image_json, indent=4)

def image_write(frame):
   cv2.imwrite("")