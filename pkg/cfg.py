import json
from dataclasses import dataclass


@dataclass
class Values:
    conf: float = 0.0               # confidence threshold
    iou: float = 0.0                # IoU threshold
    agnostic: bool = True           # agnostic NMS
    # aug: bool = True              # augmentation
    # hide_lbls: bool = False       # hide labels
    # hide_confs: bool = False      # hide confidences
    max_det: int = 1000             # maximum detections
    amp: bool = True                # automatic mixed precision


class ConfigValues:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.values = Values()

        with open(self.config_file, "r") as file:
            config = json.load(file)
            self.values.__dict__.update(**config)

    def save(self):
        try:
            with open(self.config_file, "w") as file:
                json.dump(self.values.__dict__, file, indent=4)
            return True
        except Exception as e:
            print(f"An error occurred while saving the configuration: {e}")
            return False

    def get(self, key):
        for k, v in self.values.__dict__.items():
            if k == key:
                if isinstance(v, int):
                    return v/100 if key in ["conf", "iou"] else v
                return v

    def update(self, config={}, **kwargs):
        config = {**config, **kwargs}  # Merge config and kwargs

        for key, value in config.items():
            if isinstance(value, int):
                if 0 <= value >= 100:
                    raise ValueError(f"Value of {key} must be between 0 and 100")
                
                config[key] = value/100 if key in ["conf", "iou"] else value

        self.values.__dict__.update(**config)

    def __str__(self):
        return str(self.values)
