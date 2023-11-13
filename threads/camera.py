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


# class CameraThread(QThread):
#     ImageSignal = Signal(QImage)
#     FPSSIgnal = Signal(str)
#     ClassesSignal = Signal(str)
#     ImageTypeSignal = Signal(ImageType)

#     # TODO: DETECTION SIGNAL
#     PixmapSignal = Signal(QPixmap)

#     def __init__(self, **kwargs):
#         super().__init__()

#         self.kwargs = kwargs
#         self.model_name = self.kwargs.get("model")
#         self.quiet = self.kwargs.get("quiet")
#         self.config_manager = ConfigManager()
#         self.stop_requested = False
#         self.record = VideoRecord()

#     def stop_thread(self, safe: bool = True):
#         try:
#             self.stop_requested = True
#             self.record.end()
#             if safe:
#                 while self.isRunning():
#                     time.sleep(0.1)

#                 self.quit()
#                 self.wait()
#                 console.success("Thread stopped successfully")
#             else:
#                 console.warning("Forcefully terminating the thread")
#                 self.setTerminationEnabled(True)
#                 self.terminate()
#         except Exception as e:
#             console.fatal(f"Error occurred while stopping the thread: {e}")

#     def run(self):
#         cap = self.open_camera()
#         try:
#             model = self.load_and_initialise_model()
#             if not self.quiet:
#                 console.info("Starting detection")

#             self.process_frames(cap, model)
#         finally:
#             cap.release()

#     def load_and_initialise_model(self):
#         loaded_model = self.load_torch_model()
#         model_param = self.set_model_parameters(loaded_model)
#         return self.transfer_model_to_device(model_param, self.kwargs.get("device"))

#     def process_frames(self, video_capture, model):
#         while video_capture.isOpened() and not self.stop_requested:
#             frame_retreive, frame = video_capture.read()
#             if frame_retreive:
#                 prediction = model(frame, size=768)
#                 self.draw_predictions(frame, prediction)

#             self.record.write(frame)

#     def load_torch_model(self):
#         return torch.hub.load(
#             "cache/yolov5",
#             "custom",
#             path=str(self.model_name),
#             source="local",
#             trust_repo=True,
#             verbose=False,
#         )

#     def set_model_parameters(self, detection_model):
#         config_getter = self.config_manager.get
#         params = {
#             "conf": config_getter("confidence_threshold") / 100,
#             "iou": config_getter("iou_threshold") / 100,
#             "agnostic_nms": config_getter("use_agnostic_nms"),
#             "augment": config_getter("enable_augmentation"),
#         }
#         detection_model.__dict__.update(params)
#         return detection_model

#     def transfer_model_to_device(self, model, device):
#         device = device if device == "cpu" else get_device(verbose=not self.quiet)
#         try:
#             model.to(device)
#         except Exception as e:
#             console.warning(f"Unable to transfer model to {device} due to error: {e}")
#             model.to("cpu")
#         console.info(f"Transferring model to {device.upper()}")
#         return model

#     def open_camera(self):
#         return cv2.VideoCapture(0)

#     def draw_predictions(self, input_frame, predictions):
#         rgb_frame = cv2.cvtColor(input_frame, cv2.COLOR_BGR2RGB)
#         frame_height, frame_width, _ = rgb_frame.shape
#         bytes_per_line = 3 * frame_width

#         for prediction_frame in predictions.pandas().xyxy:
#             self.process_prediction_frame(
#                 prediction_frame, rgb_frame, frame_width, frame_height, bytes_per_line
#             )

#         self.emit_final_image(rgb_frame, frame_width, frame_height, bytes_per_line)

#     def process_prediction_frame(
#         self, prediction_frame, rgb_frame, frame_width, frame_height, bytes_per_line
#     ):
#         for detection in prediction_frame.to_numpy():
#             self.process_detection(
#                 detection, rgb_frame, frame_width, frame_height, bytes_per_line
#             )

#     def process_detection(
#         self, detection, rgb_frame, frame_width, frame_height, bytes_per_line
#     ):
#         x_min, y_min, x_max, y_max, confidence, _, detected_object = detection
#         x_min, y_min, x_max, y_max = map(int, [x_min, y_min, x_max, y_max])
#         confidence = round(confidence, 2)

#         # README my own fault not changing the label during training :)
#         if detected_object == "smoking":
#             detected_object = "rokok"

#         self.draw_label(
#             rgb_frame, x_min, y_min, x_max, y_max, detected_object, confidence
#         )

#         image = QImage(
#             rgb_frame.data,
#             frame_width,
#             frame_height,
#             bytes_per_line,
#             QImage.Format.Format_RGB888,
#         )
#         image_type = ImageType(
#             image=image,
#             name=detected_object,
#             confidence=confidence,
#             timestamp=datetime.datetime.now().__str__(),
#         )

#         self.ImageTypeSignal.emit(image_type)
#         self.PixmapSignal.emit(QPixmap.fromImage(image))

#         self.record.write(cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR))

#     def emit_final_image(self, rgb_frame, frame_width, frame_height, bytes_per_line):
#         final_image = QImage(
#             rgb_frame.data,
#             frame_width,
#             frame_height,
#             bytes_per_line,
#             QImage.Format.Format_RGB888,
#         )
#         self.ImageSignal.emit(final_image)

#     def draw_label(self, frame, x_min, y_min, x_max, y_max, name, conf):
#         # Define the label text
#         text = f"{name} {conf}"

#         # Get the size of the text box and find the width and height
#         text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, 1)
#         width = text_size[0] + 10
#         height = text_size[1] + 10

#         # Color the label based on the object's name
#         bg_color, text_color = color.get_color(name)

#         # Draw rectangle on the frame
#         cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), bg_color, 2)

#         # Draw the rectangle for the text background
#         cv2.rectangle(
#             frame, (x_min - 1, y_min), (x_min + width, y_min - height), bg_color, -1
#         )

#         # Define the label position
#         org = (x_min + 5, y_min - 5)
#         font = cv2.FONT_HERSHEY_COMPLEX_SMALL

#         # Draw the label text on the frame
#         cv2.putText(frame, text, org, font, 0.7, text_color, 1, cv2.LINE_AA)

#     def calculate_fps(self, frame_count, start_time):
#         frame_count += 1
#         elapsed_time = time.time() - start_time
#         # calculate the FPS
#         fps = frame_count / elapsed_time
#         self.FPSSIgnal.emit(f"FPS: {fps:.2f}")


# save frame
def image_write(path, frame):
    cv2.imwrite(path, frame)


class CameraThread(QThread):
    # send image to main window
    ImageSignal = Signal(QImage)
    # send image to snapshot window
    SnapshotSignal = Signal(ImageType)

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.kwargs = kwargs
        self.model_name = self.kwargs.get("model")
        self.quiet = self.kwargs.get("quiet")
        self.config_manager = ConfigManager()
        self.record = VideoRecord()

        # signal to stop thread
        self.stop_requested = False

        # font
        self.font = cv2.FONT_HERSHEY_COMPLEX_SMALL

    def stop_thread(self, safe: bool = True) -> bool:
        try:
            self.stop_requested = True
            self.record.end()
            if safe:
                while self.isRunning():
                    time.sleep(0.1)
                self.quit()
                self.wait()

                console.success("Thread stopped successfully")
                if not self.isRunning():
                    return True
                return False
            else:
                console.warning("Forcefully terminating the thread")
                self.setTerminationEnabled(True)
                self.terminate()
                if not self.isRunning():
                    return True
                return False
        except Exception as e:
            console.fatal(f"Error occurred while stopping the thread: {e}")

    def run(self) -> None:
        cap = cv2.VideoCapture(0)
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
            self.ImageSignal.emit(qimage)
            # self.record.write(frame)

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

                self.draw_label(
                    frame, x_min, y_min, x_max, y_max, detected_object, confidence
                )

                # qimage = QImage(
                #     rgb_frame.data,
                #     frame_width,
                #     frame_height,
                #     bytes_per_line,
                #     QImage.Format.Format_RGB888,
                # )

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
