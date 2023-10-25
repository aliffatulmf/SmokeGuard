import datetime
import logging
import time

import cv2
import torch
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage, QPixmap

from classtype import ImageType
from config.model import ModelConfig
from utility.color import color_label


class CameraThread(QThread):
    ImageSignal = Signal(QImage)
    FPSSIgnal = Signal(str)
    ClassesSignal = Signal(str)
    ImageTypeSignal = Signal(ImageType)

    # TODO: DETECTION SIGNAL
    PixmapSignal = Signal(QPixmap)

    def __init__(self, parent):
        super().__init__(parent)

        self.model_config = ModelConfig()
        self.stop_requested = False

    def stopThread(self, safe: bool = True, exit: bool = True):
        try:
            self.stop_requested = True

            if exit:
                if safe:
                    while self.isRunning():
                        time.sleep(0.1)

                    self.quit()
                    self.wait()
                else:
                    self.setTerminationEnabled(True)
                    self.terminate()
        except Exception as e:
            logging.error(f"Error occurred while stopping the thread: {e}")

    def run(self):
        model = self.load_model()
        cap = self.open_camera()

        while cap.isOpened() and not self.stop_requested:
            ret, frame = cap.read()
            if ret:
                predict = model(frame, size=640)
                self.draw_predictions(frame, predict)

        cap.release()

    def load_model(self):
        model = torch.hub.load(
            "cache/yolov5",
            "custom",
            path="weights/model.pt",
            source="local",
            trust_repo=True,
        )
        model.conf = self.model_config.confidence_threshold
        model.iou = self.model_config.iou_threshold
        model.agnostic_nms = self.model_config.use_agnostic_nms
        model.augment = self.model_config.enable_augmentation

        return model

    @staticmethod
    def open_camera():
        return cv2.VideoCapture(0)

    def draw_predictions(self, input_frame, predictions):
        rgb_frame = cv2.cvtColor(input_frame, cv2.COLOR_BGR2RGB)

        frame_height, frame_width, _ = rgb_frame.shape
        bytes_per_line = 3 * frame_width

        for prediction_frame in predictions.pandas().xyxy:
            for detection in prediction_frame.to_numpy():
                x_min, y_min, x_max, y_max, confidence, _, detected_object = detection
                x_min, y_min, x_max, y_max = map(int, [x_min, y_min, x_max, y_max])
                confidence = round(confidence, 2)

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
