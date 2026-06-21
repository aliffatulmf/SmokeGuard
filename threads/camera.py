import datetime
import logging
import os
import time

import cv2

from classtype.metadata import ImageMetadata
from pkg.cfg import ConfigValues
from pkg.image import FQImage, ImageFrame
from pkg.inference import capture, draw, load_model

from .thread import CameraSignal, General


class CameraThread(General, CameraSignal):
    FRAME_SIZE = (320, 320)

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.kwargs = kwargs
            
    def process_frame(self, frame, model, output_dir, i):
        cfg = ConfigValues()
        h_orig, w_orig = frame.shape[:2]
        resized = cv2.resize(frame, self.FRAME_SIZE)
        result = model(resized, augment=cfg.get("augment") == "Enable")
        imframe = ImageFrame(frame)

        scale_x = w_orig / self.FRAME_SIZE[0]
        scale_y = h_orig / self.FRAME_SIZE[1]

        for predict in result.pandas().xyxy:
            if predict.empty:
                continue

            for data in predict.to_numpy():
                xmin, ymin, xmax, ymax, conf, _, obj = data
                xmin = int(xmin * scale_x)
                ymin = int(ymin * scale_y)
                xmax = int(xmax * scale_x)
                ymax = int(ymax * scale_y)
                obj = "rokok" if obj == "smoking" else obj

                draw(frame, xmin, ymin, xmax, ymax, obj, round(conf, 2))

                imframe = ImageFrame(frame)
                timestamp = datetime.datetime.now()
                self.send("SnapshotSignal", ImageMetadata(FQImage(imframe), obj, conf, timestamp))

                cv2.imwrite(f"{output_dir}/images/{i}.jpg", frame)
                i += 1

        self.send("ImageSignal", FQImage(imframe))
        return i

    def run(self):
        opt_dir = self.kwargs.get("output", "output")
        if not os.path.exists(opt_dir):
            os.makedirs(opt_dir)
        if not os.path.exists(f"{opt_dir}/images"):
            os.makedirs(f"{opt_dir}/images")
            
        cap = capture(self.kwargs["source"])

        model_path = self.kwargs.get("model")
        if not model_path:
            logging.critical("Model path not specified")
            self.send("EndOfDetection", True)
            return

        try:
            model = load_model(model_path, device=self.kwargs["device"], verbose=True)
        except Exception as e:
            logging.critical(e)
            self.send("EndOfDetection", True)
            return
            
        i = 0
        if isinstance(cap, cv2.VideoCapture):
            while cap.isOpened() and not self.stop_detection_requested:
                retrieve, frame = cap.read()

                if retrieve:
                    i = self.process_frame(frame, model, opt_dir, i)
                else:
                    break
            cap.release()
        elif isinstance(cap, list):
            for frame in cap:
                if self.stop_detection_requested:
                    return

                i = self.process_frame(frame, model, opt_dir, i)
                time.sleep(.3)

            self.send("EndOfDetection", True)
