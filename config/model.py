import torch

from config.parameter import ConfigManager

cm = ConfigManager()


class ModelConfig:
    weights: str = cm.get("weights")
    device: str = torch.device("cpu")
    imgsz: tuple = cm.get("imgsz")
    confidence_threshold: float = cm.get("confidence_threshold") / 100
    iou_threshold: float = cm.get("iou_threshold") / 100
    use_agnostic_nms: bool = cm.get("use_agnostic_nms")
    enable_augmentation: bool = cm.get("enable_augmentation")
    hide_labels_enabled: bool = cm.get("hide_labels_enabled")
    hide_confidence_enabled: bool = cm.get("hide_confidence_enabled")
    line_thickness_value: int = cm.get("line_thickness_value")
    max_detection_count: int = cm.get("max_detection_count")
    video_stride: int = cm.get("video_stride")
    max_detection_count: int = cm.get("max_detection_count")
