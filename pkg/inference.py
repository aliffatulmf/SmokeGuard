import logging
import os

import cv2
import torch

from pkg.cfg import ConfigValues
from pkg.cuda import get_device


def load_model(path, device, **kwargs):
    logging.info("Loading model...")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model not found: {path}")

    cfg = ConfigValues()

    m = torch.hub.load("cache/yolov5", "custom", path=path,
                       source="local", trust_repo=False, force_reload=True, **kwargs)
    m.conf = cfg.get("conf")
    m.iou = cfg.get("iou")
    m.agnostic = cfg.get("agnostic") == "Enable"
    m.multi_label = cfg.get("multi_label") == "Enable"
    m.max_det = cfg.get("max_det")
    m.amp = cfg.get("amp") == "Enable"
    m.to(device if device == "cpu" else get_device())

    if kwargs.get("verbose", False):
        logging.info("Parameters:")
        logging.info(f"    Confidence: {m.conf}")
        logging.info(f"    IoU: {m.iou}")
        logging.info(f"    Agnostic: {m.agnostic}")
        logging.info(f"    Multi-label: {m.multi_label}")
        logging.info(f"    Augmentation: {cfg.get('augment') == 'Enable'}")
        logging.info(f"    Max detections: {m.max_det}")
        logging.info(f"    AMP: {m.amp}")
        logging.info(f"    Device: {device.upper()}")

    return m


def capture(source):
    # Capture from a directory source
    if os.path.isdir(source):
        frames = []
        for img in os.listdir(source):
            # Capture from image files within directory
            if img.endswith(("jpg", "jpeg", "png", "webp")):
                frame = cv2.imread(os.path.join(source, img))
                if frame is not None:
                    frames.append(frame)
        if not frames:
            raise ValueError("Directory is empty or contains no valid images")
        return frames

    # Capture from a single image file
    elif os.path.isfile(source) and source.endswith(("jpg", "jpeg", "png", "webp")):
        frame = cv2.imread(source)
        if frame is None:
            raise ValueError("File is not a valid image")
        return [frame]

    # Capture from a video file or webcam
    elif os.path.isfile(source) or source.isdigit():
        cap = cv2.VideoCapture(int(source) if source.isdigit() else source)
        if not cap.isOpened():
            raise ValueError("Unable to open source with VideoCapture")
        return cap

    else:
        # Raise error for invalid source
        raise ValueError("Invalid source")


def draw(frame, xmin, ymin, xmax, ymax, obj, conf):
    format = f"{obj} {conf}"
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    aa = cv2.LINE_AA

    txt_sz, _ = cv2.getTextSize(format, font, 0.7, 1)
    txt_w = txt_sz[0] + 10
    txt_h = txt_sz[1] + 10

    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (66, 66, 255), 2)
    cv2.rectangle(frame, (xmin - 1, ymin),
                  (xmin + txt_w, ymin - txt_h), (66, 66, 255), -1)

    org = (xmin + 5, ymin - 5)
    cv2.putText(frame, format, org, font, 0.7, (255, 255, 255), 1, aa)
