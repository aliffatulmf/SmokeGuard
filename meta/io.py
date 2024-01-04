import json
import logging
import os

import cv2
import torch
from PySide6.QtGui import QFont

from .exceptions import ConfigKeyError


class ConfigIO:
    CONFIDENCE = "confidence"
    IOU = "iou"
    AGNOSTIC = "agnostic"
    MAX_DET = "max_det"
    AMP = "amp"
    MULTI_LABEL = "multi_label"
    AUGMENT = "augment"
    DEVICE = "device"

    def __init__(self, filename="config.json"):
        self.filename, default_config = filename, self.default_config
        if not os.path.exists(self.filename):
            self.write_config(default_config())

    def default_config(self):
        return {self.CONFIDENCE: 0.5, self.IOU: 0.5, self.AGNOSTIC: False, self.MAX_DET: 1000, self.AMP: False, self.MULTI_LABEL: False, self.AUGMENT: False, self.DEVICE: "cpu"}

    def read_config(self, keys=None):
        with open(self.filename, "r") as f: config = json.load(f)
        return {key: config.get(key, None) for key in keys} if keys else config

    def write_config(self, config):
        with open(self.filename, "w") as f: json.dump(config, f, indent=4)

    def update_config(self, key, value):
        config = self.read_config()
        if key not in config:
            raise ConfigKeyError(f"{key} is not a valid key")
        if isinstance(value, float):
            if not 0.0 <= value <= 1.0:
                raise ValueError("Float values must be between 0.0 and 1.0")
        if key == self.DEVICE and value not in ["cpu", "cuda"]:
            raise ValueError("Device must be either 'cpu' or 'cuda'")
        config[key] = value
        self.write_config(config)

class ModelHub:
    def __init__(self, config=ConfigIO().read_config()):
        self.config = config
    
    def load_model(self, path, device, half=False, verbose=False, **kwargs):
        logging.disable(logging.CRITICAL)
        model = torch.hub.load("hub", "custom", path=path, source="local", force_reload=True)
        parameters = [ConfigIO.CONFIDENCE, ConfigIO.IOU, ConfigIO.MAX_DET, ConfigIO.AGNOSTIC, ConfigIO.MULTI_LABEL, ConfigIO.AMP]
        for param in parameters:
            setattr(model, param, kwargs.get(param, self.config[param]))
        model.to(device)
        model.half() if half else model.float()
        if kwargs.get("names") is not None: model.names = kwargs.get("names")
        logging.disable(logging.NOTSET)
        return model
    
    @staticmethod
    def check_model_precision(model):
        return next(model.parameters()).dtype

def LoadSource(source, verbose=False):
    if not isinstance(source, str): raise ValueError("Argument 'source' must be a string.")
    if not isinstance(verbose, bool): raise ValueError("Argument 'verbose' must be a boolean.")
    cap = cv2.VideoCapture(source)
    if not cap.isOpened():
        if verbose: logging.error(f"Failed to load source: {source}")
        return None
    if verbose: logging.info(f"Successfully loaded source: {source}")
    return cap


def ProfileColors(label):
    colors = {
        "rokok": (66, 66, 255),
        "person": (95, 47, 5),
    }
    return colors.get(label, (0, 0, 0))

def Font(size=14, weight=QFont.Weight.Normal, antialias=False):
    font = QFont()
    font.setFamily("JetBrainsMono NF Medium")
    font.setPixelSize(size)
    font.setWeight(weight)
    if antialias:
        font.setStyleStrategy(QFont.StyleStrategy.PreferAntialias)
    return font
