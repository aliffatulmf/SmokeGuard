import logging

import cv2

from meta import CONFIG_READ
from meta.counter.fps import FPS
from meta.counter.general import CounterInt
from meta.counter.inference_time import InferenceTime
from meta.device.cuda import GetDevice
from meta.image.manipulation import FrameToPixmap, ResizeFrame
from meta.io import ConfigIO, LoadSource, ModelHub, ProfileColors
from meta.model.path import ModelPath
from meta.signal import ParameterNamespace, SignalEmitter, SnapshotNamespace
from meta.thread import StopControl


class Inference(StopControl):
    def __init__(self, **kwargs):
        super().__init__()

        # Retrieve device and setup configurations
        self.device, self.hw_brand = GetDevice(kwargs["device"], verbose=kwargs["verbose"])
        self.verbose = kwargs["verbose"]
        self.source = kwargs["source"]
        self.single = kwargs["single"]
        self.half = kwargs["half"]

        # Define models paths
        self.models = [
            ModelPath("weights/model.pt"),
            ModelPath("weights/general.pt")
        ]

        # Initialize components
        self.emitter = SignalEmitter()
        self.model_hub = ModelHub()
        self.config = CONFIG_READ
        self.loaded_models = []

        # Define model specific configurations
        single_model_kwgs = {"names": ["rokok"]}
        multiple_model_kwgs = {
            "confidence": 0.60,
            "iou": 0.45,
            "agnostic": False,
            "max_det": 1000,
            "multi_label": True,
            "augment": False,
            "amp": True,
        }

        # Load models with their specific configurations
        if self.verbose:
            if self.single:
                logging.info("Loading single model")
            else:
                logging.info("Loading multiple models")
        
        self.loaded_models = [
            self.model_hub.load_model(model, self.device, self.half, **(single_model_kwgs if i != 1 else multiple_model_kwgs))
            for i, model in enumerate(self.models) if not self.single or i == 0
        ]
                
    def run(self):
        capture = LoadSource(self.source, self.verbose)

        if capture is None:
            raise ValueError("Failed to load source")

        frames_per_second = FPS()
        inference_time = InferenceTime()
        frame_counter = CounterInt()

        # Check model precision
        fp = ModelHub.check_model_precision(self.loaded_models[0])
        while capture.isOpened() and not self.stop_requested:
            snapshot_checkpoint = []
            
            object_detected = 0
            frames_per_second.start()
            retrieval_successful, frame = capture.read()

            if not retrieval_successful:
                break

            frame_counter.tap()
            
            for model in self.loaded_models:
                inference_time.start()
                predictions = model(frame).pandas().xyxy
                inference_time.stop()

                for prediction in predictions:
                    if prediction.empty:
                        continue

                    for objects in prediction.to_numpy():
                        if objects[6] not in ["rokok", "person"]:
                            continue
                        object_detected += 1
                        
                        x_min, y_min, x_max, y_max, confidence, _, name = objects
                        x_min, y_min, x_max, y_max = map(int, [x_min, y_min, x_max, y_max])
                        
                        detection_text = f"{name} {round(confidence * 100)}%"
                        text_size, _ = cv2.getTextSize(detection_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 1)
                        text_width, text_height = text_size[0] + 15, text_size[1] + 25

                        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), ProfileColors(name), 3)
                        cv2.rectangle(frame, (x_min - 2, y_min), (x_min + text_width, y_min - text_height), ProfileColors(name), -1)
                        cv2.putText(frame, detection_text, (x_min + 10, y_min - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                        
                        pixmap = FrameToPixmap(ResizeFrame(frame, scale=0.4))
                        snapshot = SnapshotNamespace(
                            confidence=confidence,
                            inference_time=inference_time.stats,
                            pixmap=pixmap,
                        )
                        snapshot_checkpoint.append(snapshot)

            frames_per_second.stop()
            
            # Updating snapshot attribute values
            for snapshot in snapshot_checkpoint:
                snapshot.fps = frames_per_second.stats  # Set fps
                snapshot.confidence_threshold = self.config[ConfigIO.CONFIDENCE] # Set confidence threshold
                snapshot.iou_threshold = self.config[ConfigIO.IOU] # Set iou threshold
                snapshot.accelerator = "CUDA" if "cuda" in self.device else "CPU" # Set accelerator
                snapshot.hw_brand = self.hw_brand # Set hardware brand
                snapshot.floating_point = fp # Set floating point

                # Emit the snapshot signal
                self.emitter.emit_snapshot_signal(snapshot_checkpoint.pop(0))

            # Convert resized frame to pixmap and emit camera signal
            pixmap = FrameToPixmap(ResizeFrame(frame, scale=0.5))
            self.emitter.emit_camera_signal(pixmap)

            # Parameters Setup
            parameters = ParameterNamespace(
                frames=frame_counter.size(), # Frame count
                fps=frames_per_second.stats, # Frames per second
                inference=inference_time.stats, # Inference statistics
                total_object=object_detected, # Total objects detected
            )

            # Emit parameter signal
            self.emitter.emit_parameter_signal(parameters)