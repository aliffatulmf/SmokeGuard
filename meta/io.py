import json
import logging
import os

import cv2
import torch


class ConfigKeyError(Exception):
    """A custom exception used to report errors in use of ConfigIO class"""


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
        self.filename = filename
        if not os.path.exists(self.filename):
            self.write_config(self.default_config())

    def default_config(self):
        return {
            self.CONFIDENCE: 0.5,
            self.IOU: 0.5,
            self.AGNOSTIC: False,
            self.MAX_DET: 1000,
            self.AMP: False,
            self.MULTI_LABEL: False,
            self.AUGMENT: False,
            self.DEVICE: "cpu"
        }

    def read_config(self, keys=None):
        with open(self.filename, "r") as f:
            config = json.load(f)
        if keys is None:
            return config
        else:
            return {key: config.get(key, None) for key in keys}

    def write_config(self, config):
        with open(self.filename, "w") as f:
            json.dump(config, f, indent=4)

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

CONFIG_READ = ConfigIO().read_config()

class ModelHub:
    def __init__(self, config=CONFIG_READ):
        self.config = config
    
    def load_model(self, path, device, **kwargs):
        model = torch.hub.load("cache/yolov5", "custom", path=path, source="local", force_reload=True)
        model.conf = kwargs.get(ConfigIO.CONFIDENCE, self.config[ConfigIO.CONFIDENCE])
        model.iou = kwargs.get(ConfigIO.IOU, self.config[ConfigIO.IOU])
        model.max_det = kwargs.get(ConfigIO.MAX_DET, self.config[ConfigIO.MAX_DET])
        model.agnostic = kwargs.get(ConfigIO.AGNOSTIC, self.config[ConfigIO.AGNOSTIC])
        model.multi_label = kwargs.get(ConfigIO.MULTI_LABEL, self.config[ConfigIO.MULTI_LABEL])
        model.amp = kwargs.get(ConfigIO.AMP, self.config[ConfigIO.AMP])
        model.to(device)
        if kwargs.get("names") is not None:
            model.names = kwargs.get("names")
        return model


def load_source(source, verbose=False):
    cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        if verbose:
            logging.error(f"Failed to load source: {source}")
        return None

    if verbose:
        logging.info(f"Successfully loaded source: {source}")
    return cap
