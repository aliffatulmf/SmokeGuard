import time
import datetime

import cv2
import torch
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage, QPixmap

from config.model import ModelConfig
from utility.color import color_label
from classtype import ImageType


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
      

    def run(self):
        model = self.load_model()
        cap = self.open_camera()

        self.ClassesSignal.emit(f"Class: {len(model.names)}")
        while cap.isOpened() and not self.stop_requested:
            ret, frame = cap.read()
            dsize = (int(frame.shape[1] * 0.95), int(frame.shape[0] * 0.95))
            frame = cv2.resize(frame, dsize)

            if ret:
                predict = self.perform_inference(model, frame)
                self.draw_predictions(frame, predict)

        cap.release()

    def load_model(self):
        repo = "ultralytics/yolov5"
        repo_model = "custom"
        path = "weights/model.pt"
        device = "cpu"
        
        model = torch.hub.load(repo, repo_model, path=path, trust_repo=True, device=device)
        model.conf = self.model_config.confidence_threshold
        model.iou = self.model_config.iou_threshold
        model.agnostic_nms = self.model_config.use_agnostic_nms
        model.augment = self.model_config.enable_augmentation

        return model

    @staticmethod
    def open_camera():
        return cv2.VideoCapture(0)

    @staticmethod
    def perform_inference(model, frame):
        return model(frame)

    def draw_predictions(self, frame, predict):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, _ = frame.shape
        bytes_per_line = 3 * width

        for df in predict.pandas().xyxy:
            for dt in df.to_numpy():
                # x_min, y_min, x_max, y_max, confidence, class_label, name = dt
                x_min, y_min, x_max, y_max, confidence, _, name = dt
                x_min, y_min, x_max, y_max = map(int, [x_min, y_min, x_max, y_max])
                confidence = round(confidence, 2)

                self.draw_label(frame, x_min, y_min, x_max, y_max, name, confidence)
                
                img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                img_type = ImageType(image=img, name=name, confidence=confidence, timestamp=datetime.datetime.now().__str__())
                self.ImageTypeSignal.emit(img_type)

                self.PixmapSignal.emit(QPixmap.fromImage(img))


        img = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        self.ImageSignal.emit(img)


    
    # TODO: save frame into images folder and add info to images.json
    # @staticmethod
    # def saveFrame(frame, path):
    #     cv2.imwrite(path, frame)

    @staticmethod
    def draw_label(frame, x_min, y_min, x_max, y_max, name, conf):
        text = f"{name} {conf}"
        text_size, _ = cv2.getTextSize(
            text, cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.7, 1
        )
        width = text_size[0] + 10
        height = text_size[1] + 10

        bg_color, text_color = color_label(name)
        cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), bg_color, 2)
        cv2.rectangle(frame, (x_min - 1, y_min), (x_min + width, y_min - height), bg_color, -1)

        org = (x_min + 5, y_min - 5)
        font = cv2.FONT_HERSHEY_COMPLEX_SMALL
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
