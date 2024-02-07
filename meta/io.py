"""
Meta IO

This module contains the IO functions for read and writing configuration file.
"""


import json

CFG_BUFFER_SIZE = 128
CFG_ENCODING = "utf-8"

class ConfigIO:
    CONFIDENCE = "confidence"
    IOU = "iou"
    AGNOSTIC = "agnostic"
    MAX_DET = "max_det"
    AMP = "amp"
    MULTI_LABEL = "multi_label"
    AUGMENT = "augment"

    def __init__(self, name="config.json"):
        self.name = name
        self.values: dict = self.__read(name)
        
    @property
    def default(self):
        return {
            # threshold for object detection
            self.CONFIDENCE: 0.5,
            # threshold for NMS
            self.IOU: 0.5,
            # whether to use class-agnostic detection
            self.AGNOSTIC: False,
            # maximum number of detections per image
            self.MAX_DET: 1000,
            # whether to use automatic mixed precision
            self.AMP: False,
            # whether to use multi-label detection
            self.MULTI_LABEL: False,
            # whether to use image augmentation
            self.AUGMENT: False,
        }

    def read(self, key=None):
        """
        Read a key from the configuration file.
        """
        return self.values.get(key, None) if key else self.values

    def reads(self, keys=None):
        """
        Read multiple keys from the configuration file.
        """
        return {key: self.values.get(key, None) for key in keys} if keys else self.values

    def write(self, key, value):
        """
        Write a key to the configuration file.
        """
        if key not in self.values:
            raise KeyError(f"{key} is not a valid key")

        self.values[key] = value
        self.__write(self.name, self.values)

    # WIP: DON'T CALL THIS FUNC
    def check(self):
        """
        Check any errors on the keys and value.
        """
        pairs = (
                {"key": self.CONFIDENCE, "type": float},
                {"key": self.IOU, "type": float},
                {"key": self.AGNOSTIC, "type": bool},
                {"key": self.MAX_DET, "type": int},
                {"key": self.AMP, "type": bool},
                {"key": self.MULTI_LABEL, "type": bool},
                {"key": self.AUGMENT, "type": bool},
                )
        
        reader = self.__read(self.name)

        for key in reader.keys():
            if key not in pairs:
                raise KeyError(f"{key} is required.")



    def writes(self, values):
        """
        Write multiple keys to the configuration file.
        """
        self.values.update(values)
        self.__write(self.name, self.values)

    @staticmethod
    def __read(name):
        with open(name, "r", CFG_BUFFER_SIZE, CFG_ENCODING) as f:
            return json.load(f)

    def __write(self, name, values):
        with open(name, "w", CFG_BUFFER_SIZE, CFG_ENCODING) as f:
            json.dump(values, f, indent=4)
 
