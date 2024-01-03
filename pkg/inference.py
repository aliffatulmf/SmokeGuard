import logging
import os

import cv2
import torch

from pkg.cfg import ConfigValues
from pkg.cuda import get_device


def load_model(path, device, **kwargs):
    logging.info("Loading model...")
    # if not os.path.exists(path):
    #     raise FileNotFoundError(f"Model not found: {path}")

    cfg = ConfigValues()
    
    model = torch.hub.load("cache/yolov5", "custom", path=path, source="local", trust_repo=True, force_reload=True, **kwargs)
    # if kwargs.get("names"):
    #     model.names = kwargs.get("names")
    model.conf, model.iou, model.max_det = cfg.get("conf"), cfg.get("iou"), cfg.get("max_det")
    model.agnostic, model.multi_label, model.amp = cfg.get("agnostic") == "Enable", cfg.get("multi_label") == "Enable", cfg.get("amp") == "Enable"
    model.to(device if device == "cpu" else get_device())
    

    if kwargs.get("verbose", False):
        logging.info("Parameters:")
        logging.info(f"    Confidence: {model.conf}")
        logging.info(f"    IoU: {model.iou}")
        logging.info(f"    Agnostic: {model.agnostic}")
        logging.info(f"    Multi-label: {model.multi_label}")
        logging.info(f"    Augmentation: {cfg.get('augment') == 'Enable'}")
        logging.info(f"    Max detections: {model.max_det}")
        logging.info(f"    AMP: {model.amp}")
        logging.info(f"    Device: {device.upper()}")

    return model

VIDEO_FORMATS = ("avi", "mp4", "mpg", "webm", "mkv")
IMAGE_FORMATS = ("jpg", "jpeg", "png", "webp")

def capture(source):
    frames = []
    if os.path.isdir(source):
        for img in os.listdir(source):
            if img.endswith(IMAGE_FORMATS):
                frame = cv2.imread(os.path.join(source, img))
                if frame is not None:
                    frames.append(frame)
        if not frames:
            raise ValueError("Directory is empty or contains no valid images")
    elif source.isdigit() or os.path.isfile(source):
        if source.isdigit():
            cap = cv2.VideoCapture(int(source))
        elif source.endswith(VIDEO_FORMATS):  # check if source is a video file
            cap = cv2.VideoCapture(source)
            if not cap.isOpened():
                raise ValueError("Unable to open video source")
        else:
            if not source.endswith(("jpg", "jpeg", "png", "webp")):
                raise ValueError("File is not a valid image")
            frame = cv2.imread(source)
            if frame is None:
                raise ValueError("File is not a valid image")
            frames.append(frame)
    else:
        raise ValueError("Invalid source")
    return frames if frames else cap


def draw(frame, xmin, ymin, xmax, ymax, obj, conf):
    format = f"{obj} {conf}"
    font = cv2.FONT_HERSHEY_COMPLEX
    aa = cv2.LINE_AA

    txt_sz = cv2.getTextSize(format, font, 1, 1)[0]
    txt_w, txt_h = txt_sz[0] + 10, txt_sz[1] + 10

    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (66, 66, 255), 2)
    cv2.rectangle(frame, (xmin - 1, ymin), (xmin + txt_w, ymin - txt_h), (66, 66, 255), -1)
    cv2.putText(frame, format, (xmin + 5, ymin - 5), font, 1, (255, 255, 255), 1, aa)
    
# def process_frame(frame, model, cfg, snapshot_signal, image_signal):
#     res = model(frame, augment=cfg.get("augment") == "Enable", size=1280)
#     imf = ImageFrame(frame)

#     for pred in res.pandas().xyxy:
#         if pred.empty:
#             img_empty = ImageMetadata(FQImage(imf), None, None, None)
#             snapshot_signal.emit(img_empty)

#         for data in pred.to_numpy():
#             x_min, y_min, x_max, y_max, conf, _, obj = data
#             x_min = int(x_min)
#             y_min = int(y_min)
#             x_max = int(x_max)
#             y_max = int(y_max)
#             obj = "rokok" if obj == "smoking" else obj

#             draw(frame, x_min, y_min, x_max, y_max, obj, round(conf, 2))

#             imf = ImageFrame(frame)
#             timestamp = datetime.datetime.now()

#             img_meta = ImageMetadata(FQImage(imf), obj, round(conf, 4), timestamp)
#             snapshot_signal.emit(img_meta)

#         image_signal.emit(FQImage(imf))
        
        

