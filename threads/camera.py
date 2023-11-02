import datetime
import time

import cv2
import torch
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage, QPixmap

from classtype import ImageType
from config.parameter import ConfigManager
from lib.hardware import get_device
from lib.logger import console
from utility.color import color_label


class CameraThread(QThread):
    ImageSignal = Signal(QImage)
    FPSSIgnal = Signal(str)
    ClassesSignal = Signal(str)
    ImageTypeSignal = Signal(ImageType)

    # TODO: DETECTION SIGNAL
    PixmapSignal = Signal(QPixmap)

    def __init__(self, **kwargs):
        super().__init__()

        self.kwargs = kwargs
        self.model_name = self.kwargs.get("model")
        self.quiet = self.kwargs.get("quiet")
        self.config_manager = ConfigManager()
        self.stop_requested = False

    def stop_thread(self, safe: bool = True):
        try:
            self.stop_requested = True
            if safe:
                while self.isRunning():
                    time.sleep(0.1)

                self.quit()
                self.wait()
                console.success("Thread stopped successfully")
            else:
                console.warning("Forcefully terminating the thread")
                self.setTerminationEnabled(True)
                self.terminate()
        except Exception as e:
            console.fatal(f"Error occurred while stopping the thread: {e}")

    def run(self):
        try:
            cap = self.open_camera()
            model = self.load_and_initialise_model()

            if not self.quiet:
                console.info("Starting detection")

            self.process_frames(cap, model)
        finally:
            cap.release()

    def load_and_initialise_model(self):
        loaded_model = self.load_torch_model()
        model_param = self.set_model_parameters(loaded_model)
        return self.transfer_model_to_device(model_param, self.kwargs.get("device"))

    def process_frames(self, video_capture, model):
        while video_capture.isOpened() and not self.stop_requested:
            frame_exists, frame = video_capture.read()
            if frame_exists:
                prediction = model(frame, size=768)
                self.draw_predictions(frame, prediction)

    def load_torch_model(self):
        return torch.hub.load(
            "cache/yolov5",
            "custom",
            path=str(self.model_name),
            source="local",
            trust_repo=True,
            verbose=False,
        )

    def set_model_parameters(self, detection_model):
        config_getter = self.config_manager.get
        confidence_threshold = config_getter("confidence_threshold") / 100
        intersection_over_union_threshold = config_getter("iou_threshold") / 100
        agnostic_nms = config_getter("use_agnostic_nms")
        enable_augmentation = config_getter("enable_augmentation")

        (
            detection_model.conf,
            detection_model.iou,
            detection_model.agnostic_nms,
            detection_model.augment,
        ) = (
            confidence_threshold,
            intersection_over_union_threshold,
            agnostic_nms,
            enable_augmentation,
        )
        return detection_model

    def transfer_model_to_device(self, model, device):
        if device == "cpu":
            model.to(device)
            console.info("Transferring model to CPU")
        else:
            console.info("Verifying GPU resources ...")
            try:
                model.to(get_device(verbose=not self.quiet))
                console.info("Transferring model to GPU")
            except Exception as e:
                console.warning(f"Unable to transfer model to GPU due to error: {e}")
                console.info("Transferring model to CPU")
                model.to("cpu")
        return model

    def open_camera(self):
        return cv2.VideoCapture(0)

    def draw_predictions(self, input_frame, predictions):
        rgb_frame = cv2.cvtColor(input_frame, cv2.COLOR_BGR2RGB)
        frame_height, frame_width, _ = rgb_frame.shape
        bytes_per_line = 3 * frame_width

        for prediction_frame in predictions.pandas().xyxy:
            self.process_prediction_frame(
                prediction_frame, rgb_frame, frame_width, frame_height, bytes_per_line
            )

        self.emit_final_image(rgb_frame, frame_width, frame_height, bytes_per_line)

    def process_prediction_frame(
        self, prediction_frame, rgb_frame, frame_width, frame_height, bytes_per_line
    ):
        for detection in prediction_frame.to_numpy():
            self.process_detection(
                detection, rgb_frame, frame_width, frame_height, bytes_per_line
            )

    def process_detection(
        self, detection, rgb_frame, frame_width, frame_height, bytes_per_line
    ):
        x_min, y_min, x_max, y_max, confidence, _, detected_object = detection
        x_min, y_min, x_max, y_max = map(int, [x_min, y_min, x_max, y_max])
        confidence = round(confidence, 2)

        # README my own fault not changing the label during training :)
        if detected_object == "smoking":
            detected_object = "rokok"

        self.draw_label(
            rgb_frame, x_min, y_min, x_max, y_max, detected_object, confidence
        )

        image = QImage(
            rgb_frame.data,
            frame_width,
            frame_height,
            bytes_per_line,
            QImage.Format.Format_RGB888,
        )
        image_type = ImageType(
            image=image,
            name=detected_object,
            confidence=confidence,
            timestamp=datetime.datetime.now().__str__(),
        )

        self.ImageTypeSignal.emit(image_type)
        self.PixmapSignal.emit(QPixmap.fromImage(image))

    def emit_final_image(self, rgb_frame, frame_width, frame_height, bytes_per_line):
        final_image = QImage(
            rgb_frame.data,
            frame_width,
            frame_height,
            bytes_per_line,
            QImage.Format.Format_RGB888,
        )
        self.ImageSignal.emit(final_image)

    def draw_label(self, frame, x_min, y_min, x_max, y_max, name, conf):
        # Define the label text
        text = f"{name} {conf}"

        # Get the size of the text box and find the width and height
        text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, 1)
        width = text_size[0] + 10
        height = text_size[1] + 10

        # Color the label based on the object's name
        bg_color, text_color = color_label(name)

        # Draw rectangle on the frame
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), bg_color, 2)

        # Draw the rectangle for the text background
        cv2.rectangle(
            frame, (x_min - 1, y_min), (x_min + width, y_min - height), bg_color, -1
        )

        # Define the label position
        org = (x_min + 5, y_min - 5)
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL

        # Draw the label text on the frame
        cv2.putText(frame, text, org, font, 0.7, text_color, 1, cv2.LINE_AA)

    def calculate_fps(self, frame_count, start_time):
        frame_count += 1
        elapsed_time = time.time() - start_time
        # calculate the FPS
        fps = frame_count / elapsed_time
        self.FPSSIgnal.emit(f"FPS: {fps:.2f}")


# save frame
def image_write(path, frame):
    cv2.imwrite(path, frame)
