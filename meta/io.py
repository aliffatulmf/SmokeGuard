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
        self.values: dict = self.read_file(name)

    def read_file(self, name):
        with open(name, "r", CFG_BUFFER_SIZE, CFG_ENCODING) as f:
            return json.load(f)

    def write_file(self, name, values):
        with open(name, "w", CFG_BUFFER_SIZE, CFG_ENCODING) as f:
            json.dump(values, f, indent=4)

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
        return self.values.get(key, None) if key else self.values

    def reads(self, keys=None):
        return {key: self.values.get(key, None) for key in keys} if keys else self.values

    def write(self, key, value):
        if key not in self.values:
            raise KeyError(f"{key} is not a valid key")
        
        if not isinstance(value, type(self.values[key])):
            raise ValueError(f"Value must be of type {type(self.values[key])}")
        
        self.values[key] = value
        self.write_file(self.name, self.values)

    def writes(self, values):
        for key, value in values.items():
            if key not in self.values:
                raise KeyError(f"{key} is not a valid key")

            if not isinstance(value, type(self.values[key])):
                raise ValueError(f"Value must be of type {type(self.values[key])}")

        self.values.update(values)
        self.write_file(self.name, self.values)
