import datetime
import time

import cv2
import torch
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage

from classtype import ImageType
from config.parameter import ConfigManager
from libs.hardware import get_device
from libs.logger import console
from libs.records.save import VideoRecord
from utility.color import ColorLabel

color = ColorLabel()


class GeneralQThread(QThread):
    def __init__(self):
        super().__init__()

    def safe_stop(self):
        """Attempts to stop the thread safely.

        This method will try to stop the thread up to three times, waiting one second between each attempt.
        If the thread is successfully stopped, it returns True. If the thread is still running after three attempts,
        it raises an exception.

        Raises:
            Exception: If the thread could not be stopped after three attempts.

        Returns:
            bool: True if the thread was successfully stopped, False otherwise.
        """
        attempts = 0
        while attempts < 3:
            if attempts > 0:
                time.sleep(1)

            is_running = self.isRunning()
            if is_running:
                self.quit()
                self.wait()

            if not is_running:
                return True
            attempts += 1
        raise Exception("Unable to stop thread")

    def force_stop(self):
        """Forcefully terminates the thread.

        This method logs a warning message, enables termination, and then terminates the thread.
        It then checks if the thread is still running. If it's not, it returns True. If it is, it returns False.

        Returns:
            bool: True if the thread was successfully terminated, False otherwise.
        """
        console.warning("Forcefully terminating the thread")
        self.setTerminationEnabled(True)
        self.terminate()

        if not self.isRunning():
            return True
        return False


class CameraThread(GeneralQThread):
    ImageSignal = Signal(QImage)
    SnapshotSignal = Signal(ImageType)
    EOD = Signal(bool)

    def __init__(self, **kwargs) -> None:
        super().__init__()

        # Configuration and state variables
        self.config_manager = ConfigManager()
        self.kwargs = kwargs
        self.stop_requested = False

        # Video and image processing variables
        self.font = cv2.FONT_HERSHEY_COMPLEX_SMALL
        self.record = VideoRecord()

        # Model and quiet mode variables
        self.model_name = self.kwargs.get("model")
        self.quiet = self.kwargs.get("quiet")

    def stop_thread(self, safe: bool = True):
        try:
            self.stop_requested = True
            self.record.end()
            if self.safe_stop():
                console.info("Thread stopped successfully")
                return True
        except Exception as e:
            console.fatal(f"Error occurred while stopping the thread: {e}")
            return False

    def run(self) -> None:
        cap = cv2.VideoCapture(self.kwargs.get("source"))
        model = torch.hub.load(
            "cache/yolov5",
            "custom",
            path=str(self.model_name),
            source="local",
            trust_repo=True,
            verbose=False,
        )
        config_getter = self.config_manager.get
        params = {
            "conf": config_getter("confidence_threshold") / 100,
            "iou": config_getter("iou_threshold") / 100,
            "agnostic_nms": config_getter("use_agnostic_nms"),
            "augment": config_getter("enable_augmentation"),
        }
        model.__dict__.update(params)

        device = self.kwargs.get("device")
        device = device if device == "cpu" else get_device(verbose=not self.quiet)
        try:
            model.to(device)
        except Exception as e:
            console.warning(f"Unable to transfer model to {device} due to error: {e}")
            model.to("cpu")

        console.info(f"Transferring model to {device.upper()}")
        while cap.isOpened() and not self.stop_requested:
            frame_retreive, frame = cap.read()

            if frame_retreive:
                prediction = model(frame, size=768)
                # rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # (height, width, channel) = rgb_frame.shape
                frame_height, frame_width, _ = frame.shape
                bytes_per_line = 3 * frame_width

                qimage = QImage(
                    frame.data,
                    frame_width,
                    frame_height,
                    bytes_per_line,
                    QImage.Format.Format_RGB888,
                )

                self.draw_predictions(frame, prediction, qimage=qimage)
            else:
                self.EOD.emit(True)
                self.record.end()
                break
            self.record.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            self.ImageSignal.emit(qimage)

        cap.release()
        cv2.destroyAllWindows()

    def draw_predictions(
        self,
        frame: torch.Tensor,
        predictions,  # yolov5 model.common.Detections
        **kwargs,
    ):
        for prediction_frame in predictions.pandas().xyxy:
            for detection in prediction_frame.to_numpy():
                x_min, y_min, x_max, y_max, confidence, _, detected_object = detection
                x_min, y_min, x_max, y_max = map(int, [x_min, y_min, x_max, y_max])

                if detected_object == "smoking":
                    detected_object = "rokok"

                # round confidence to 2 decimal places
                confidence = round(confidence, 2)

                self.draw_label(
                    frame, x_min, y_min, x_max, y_max, detected_object, confidence
                )

                image_type = ImageType(
                    image=kwargs["qimage"],
                    name=detected_object,
                    confidence=confidence,
                    timestamp=datetime.datetime.now().__str__(),
                )

                # self.ImageSignal.emit(qimage)
                self.SnapshotSignal.emit(image_type)

    def draw_label(self, frame, x_min, y_min, x_max, y_max, name, confidence):
        text = f"{name} {confidence}"
        text_size, _ = cv2.getTextSize(text, self.font, 0.7, 1)
        text_width = text_size[0] + 10
        text_height = text_size[1] + 10

        bg_color, text_color = color.get_color(name)
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), bg_color, 2)
        cv2.rectangle(
            frame,
            (x_min - 1, y_min),
            (x_min + text_width, y_min - text_height),
            bg_color,
            -1,
        )

        org = (x_min + 5, y_min - 5)
        cv2.putText(frame, text, org, self.font, 0.7, text_color, 1, cv2.LINE_AA)
