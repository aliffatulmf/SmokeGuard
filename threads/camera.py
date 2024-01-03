import logging
import os
import time
from collections import deque

import cv2

import meta.general as general
from meta.count import FPSMaster, InferenceTimer
from meta.signal import SignalEmitter
from meta.thread import StoppableThread
from pkg.cfg import ConfigValues
from pkg.inference import capture, load_model
from threads.threader import CameraSignal, General


class CameraThread(StoppableThread, FPSMaster, InferenceTimer, SignalEmitter):
    def __init__(self, device, outdir, source=0, verbose=False, **kwargs) -> None:
        super().__init__()
        self.source = source
        self.device = device
        self.outdir = outdir
        self.verbose = verbose
        self.single = kwargs["single"]
        self.cfg = ConfigValues()
        # self.prev_frame_time = time.time()
        # self.fps_deque = deque(general.DEQUE_MAXLEN)
        self.infertime_deque = deque(general.DEQUE_MAXLEN)
        

    def run(self):
        cig = self.load_model(os.path.join("weights", "model.pt"))
        if not self.single:
            gen = self.load_model(os.path.join("weights", "yolov5s6.pt"))
            gen.conf = 0.6
        cap = capture(self.source)

        if isinstance(cap, cv2.VideoCapture):
            self.process_video_capture(cap, [cig] if self.single else [cig, gen])
            cap.release()

    def load_model(self, weight, **kwargs):
        model = load_model(weight, self.device, **kwargs)
        if self.verbose:
            logging.info(f"Weights: {self.weights} loaded into model on device: {self.device}")
        return model

    def process_video_capture(self, cap, models):
        while cap.isOpened() and not self._stop_requested:
            retrieve, frame = cap.read()

            if retrieve:
                self.start_fps()
                self.process_frame(frame, models)
                self.stop_fps()
            else:
                break

    def process_frame_sequence(self, cap, model):
        for frame in cap:
            if self.stop_detection_requested:
                return
            self.process_frame(frame, model)
            time.sleep(.3)
        self.EOD.emit(True)
    
    def resize_frame(self, frame, scale=1):
        # Get the dimensions of the frame
        height, width = frame.shape[:2]
        
        # Calculate the new dimensions
        new_width = int(width * scale)
        new_height = int(height * scale)
        
        # Resize the frame
        resized_frame = cv2.resize(frame, (new_width, new_height), interpolation = cv2.INTER_LINEAR)
        return resized_frame
            
    def draw(self, frame, xmin, ymin, xmax, ymax, obj, conf, color=(66, 66, 255)):
        # Define text format and font properties
        text = f"{obj} {conf}"
        font = cv2.FONT_HERSHEY_COMPLEX
        line_type = cv2.LINE_AA

        # Calculate text size and dimensions
        text_size, _ = cv2.getTextSize(text, font, 1, 1)
        text_width, text_height = text_size[0] + 10, text_size[1] + 10

        # Draw bounding box
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 3)

        # Draw background rectangle for text
        cv2.rectangle(frame, (xmin - 1, ymin), (xmin + text_width, ymin - text_height), color, -1)

        # Draw text
        cv2.putText(frame, text, (xmin + 5, ymin - 5), font, 1, (255, 255, 255), 1, line_type)

    def process_frame(self, frame, models):
        # Initialize variables
        augment = self.cfg.get("augment") == "Enable"
        start_time = time.time()
        obj_dets = 0

        # Perform inference on each model
        predicts = [model(frame, augment=augment, size=1280).pandas().xyxy for model in models]

        # Calculate inference time
        end_time = time.time()
        infer_time = (end_time - start_time) * 1000
        self.infertime_deque.append(infer_time)
        min_infertime = min(self.infertime_deque) if self.infertime_deque else 0
        max_infertime = max(self.infertime_deque) if self.infertime_deque else 0
        avg_infertime = sum(self.infertime_deque) / len(self.infertime_deque) if self.infertime_deque else 0
        infer_stats = {"min": min_infertime, "max": max_infertime, "avg": avg_infertime, "current": infer_time}

        # Calculate frames per second (FPS)
        # fps = 1 / (start_time - self.prev_frame_time)
        # self.prev_frame_time = start_time
        # self.fps_deque.append(fps)
        # min_fps = min(self.fps_deque) if self.fps_deque else 0
        # max_fps = max(self.fps_deque) if self.fps_deque else 0
        # avg_fps = sum(self.fps_deque) / len(self.fps_deque) if self.fps_deque else 0
        # fps_stats = {"min": min_fps, "max": max_fps, "avg": avg_fps, "current": fps}

        # Process predictions
        if len(models) > 1:
            # Process predictions from multiple models
            for cig, gen in zip(*predicts):
                for data in cig.to_numpy():
                    obj_dets += 1
                    xmin, ymin, xmax, ymax, conf, _, cls_name = data
                    axs_norm = map(int, [xmin, ymin, xmax, ymax])
                    self.draw(frame, *axs_norm, cls_name, round(conf, 2))
                for data in gen.to_numpy():
                    if data[6] != "person":
                        continue
                    obj_dets += 1
                    xmin, ymin, xmax, ymax, _, _, _ = data
                    axs_norm = map(int, [xmin, ymin, xmax, ymax])
                    self.draw(frame, *axs_norm, data[6], round(data[4], 2), (95, 41, 1))
        else:
            # Process predictions from a single model
            for pred in predicts[0]:
                if not pred.empty:
                    for data in pred.to_numpy():
                        obj_dets += 1
                        xmin, ymin, xmax, ymax, conf, _, cls_name = data
                        axs_norm = map(int, [xmin, ymin, xmax, ymax])
                        self.draw(frame, *axs_norm, cls_name, round(conf, 2))

        # Emit signals and parameters
        for pred in predicts[0]:
            if not pred.empty:
                self.snapshot_signal_emit({
                    "frame": self.resize_frame(frame, scale=0.5),
                    "conf": conf,
                    "cls_name": cls_name,
                    "inference_time": infer_stats,
                    "fps": fps_stats,
                    "obj_detected": obj_dets,
                })
        
        self.camera_signal_emit(self.resize_frame(frame, scale=0.5))
        self.parameter_signal.emit({
            "inference_time": infer_stats,
            "fps": fps_stats,
            "obj_detected": obj_dets,
        })
