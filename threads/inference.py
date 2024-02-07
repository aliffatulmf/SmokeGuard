"""
Meta Inference

This module contains the Inference class, which is a QObject that handles the inference process for a given model.
"""
import os
from queue import Queue

import cv2
import torch
from models.common import DetectMultiBackend
from PySide6.QtCore import QObject, Signal
from ultralytics.utils.plotting import Annotator, colors
from utils.dataloaders import LoadImages, LoadStreams
from utils.general import (Profile, check_img_size, check_imshow,
                           non_max_suppression, scale_boxes)

from meta import CONFIG_JSON
from meta.cuda import get_cuda_devices
from meta.fps import FPS, FPSStats
from meta.frame import image_to_qpixmap, resize_scale
from meta.inference import InferenceTime, InferenceTimeStats
from meta.io import ConfigIO
from meta.schema import PARAMETER_SCHEMA, SNAPSHOT_SCHEMA


class Inference(QObject):
    """
    The Inference class is a QObject that handles the inference process for a given model.

    Attributes:
        CAMERA_SIG (Signal): Signal to emit the camera frame.
        SNAPSHOT_SIG (Signal): Signal to emit the snapshot data.
        PARAMETER_SIG (Signal): Signal to emit the parameter data.

    Methods:
        __init__(weights, source, half, floating_point, limit, **kwargs): Initializes the Inference object with the given parameters.
    """

    CAMERA_SIG = Signal(object)
    SNAPSHOT_SIG = Signal(object)
    PARAMETER_SIG = Signal(object)

    def __init__(self,
                 weights,
                 source,
                 half=False,
                 floating_point=torch.float32,
                 limit=100,
                 **kwargs):
        """
        Initializes the Inference object with the given parameters.

        Args:
            weights (str): The path to the weights file for the model.
            source (str): The source of the input data (file path or camera device).
            half (bool, optional): Whether to use half precision. Defaults to False.
            floating_point (torch.dtype, optional): The floating point precision to use for the model. Defaults to torch.float32.
            limit (int, optional): The maximum size of the snapshot queue. Defaults to 100.
        """
        super().__init__()

        # Hardware and device configuration
        self.device = get_cuda_devices()
        self.fp = floating_point

        # Statistics
        self.__inference_stats = InferenceTimeStats()
        self.__fps_stats = FPSStats()
        self.__snapshot_queue = Queue(limit)

        # Model and source configuration
        self.source = source
        self.__model = DetectMultiBackend(weights, self.device, fp16=half)
        self.__model.names = ["rokok"]

        # Runtime control
        self.__stop_flag = False

    def stop_loop(self):
        """
        Stops the loop by setting the stop flag to True and returns the updated stop flag.
        """
        self.__stop_flag = True
        return self.__stop_flag

    def run(self):
        """
        Run the inference process on the input data and emit signals with the inference results.
        """
        global annotator, det

        stride, names, pt = self.__model.stride, self.__model.names, self.__model.pt
        imgsz = check_img_size((640, 640))  # check img_size

        batch_size = 1
        if self.source.isdigit():
            check_imshow(warn=True)
            dataset = LoadStreams(self.source, img_size=imgsz, stride=stride, auto=pt)
            batch_size = len(dataset)
        elif os.path.isfile(self.source):
            dataset = LoadImages(self.source, img_size=imgsz, stride=stride, auto=pt)

        self.__model.warmup(imgsz=(1 if pt else batch_size, 3, *imgsz))
        seen, dt = 0, (Profile(device=self.device), Profile(device=self.device), Profile(device=self.device))

        for _, im, im0s, _, s in dataset:
            if self.__stop_flag:
                return

            # start counting
            fps, inf = FPS(), InferenceTime()
            fps.start(), inf.start()

            with dt[0]:
                im = torch.from_numpy(im).to(self.device)
                im = im.float()  # fp32
                im /= 255
                if len(im.shape) == 3:
                    im = im[None]

            with dt[1]:
                pred = self.__model(im, augment=CONFIG_JSON[ConfigIO.AUGMENT])

            with dt[2]:
                pred = non_max_suppression(prediction=pred,
                                           conf_thres=CONFIG_JSON[ConfigIO.CONFIDENCE],
                                           iou_thres=CONFIG_JSON[ConfigIO.IOU],
                                           agnostic=CONFIG_JSON[ConfigIO.AGNOSTIC],
                                           max_det=CONFIG_JSON[ConfigIO.MAX_DET])

            # stop counting inference time
            inf.stop()
            self.__inference_stats.add_time(inf.elapsed)  # add inference time to stats

            for i, det in enumerate(pred):
                seen += 1  # object detected

                if self.source == "0":
                    im0 = im0s[i].copy()
                else:
                    im0 = im0s.copy()

                s += "%gx%g " % im.shape[2:]
                annotator = Annotator(im0, line_width=4, font_size=50, pil=True, example=str(names))

                if len(det):
                    det[:, :4] = scale_boxes(im.shape[2:], det[:, :4], im0.shape).round()

                    conf_sum = sum(det[:, 4].float())
                    conf_avg = (conf_sum / len(det)).item()  # average confidence

                    for *xyxy, conf, cls in reversed(det):
                        c = int(cls)
                        label = f"{names[c]} {round(conf.item() * 100)}%"
                        annotator.box_label(xyxy, label, color=colors(c, True))

                    frame = cv2.cvtColor(annotator.result(), cv2.COLOR_BGR2RGB)
                    resized = resize_scale(frame, 0.6)
                    pixmap = image_to_qpixmap(resized)

                    snapshot = SNAPSHOT_SCHEMA.copy()
                    snapshot["confidence"] = conf_avg
                    snapshot["threshold"]["confidence"] = CONFIG_JSON[ConfigIO.CONFIDENCE]
                    snapshot["threshold"]["iou"] = CONFIG_JSON[ConfigIO.IOU]
                    snapshot["inference"]["min"] = self.__inference_stats.min_time
                    snapshot["inference"]["max"] = self.__inference_stats.max_time
                    snapshot["inference"]["avg"] = self.__inference_stats.avg_time
                    snapshot["image"]["qpixmap"] = pixmap
                    snapshot["floating_point"] = self.fp
                    snapshot["hardware"] = "NVIDIA RTX 4090"
                    self.__snapshot_queue.put(snapshot)

            fps.update()
            self.__fps_stats.add_fps(fps.frame_rate)

            frame = cv2.cvtColor(annotator.result(), cv2.COLOR_BGR2RGB)
            resized = resize_scale(frame, 0.5)
            self.CAMERA_SIG.emit(image_to_qpixmap(resized))

            parameter = PARAMETER_SCHEMA.copy()
            parameter["frames"] = seen
            parameter["fps"]["current"] = fps.frame_rate
            parameter["fps"]["min"] = self.__fps_stats.min_fps
            parameter["fps"]["max"] = self.__fps_stats.max_fps
            parameter["fps"]["avg"] = self.__fps_stats.avg_fps
            parameter["inference"]["current"] = inf.elapsed
            parameter["inference"]["min"] = self.__inference_stats.min_time
            parameter["inference"]["max"] = self.__inference_stats.max_time
            parameter["inference"]["avg"] = self.__inference_stats.avg_time
            parameter["total_object"] = len(det)
            self.PARAMETER_SIG.emit(parameter)

            if not self.__snapshot_queue.empty():
                snapshot = self.__snapshot_queue.get()
                snapshot["fps"]["min"] = self.__fps_stats.min_fps
                snapshot["fps"]["max"] = self.__fps_stats.max_fps
                snapshot["fps"]["avg"] = self.__fps_stats.avg_fps
                self.SNAPSHOT_SIG.emit(snapshot)
